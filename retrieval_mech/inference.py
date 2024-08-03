import numpy as np
import faiss
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pickle
import torch
import torch.nn.functional as F
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import re
from extraction import clean_title
import boto3
import io
import functools
import tempfile
import shutil

app = Flask(__name__)


# Set up S3 client
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
bucket_name = os.getenv('S3_BUCKET_NAME')

# Load files from S3 (with caching)
@functools.lru_cache(maxsize=1)
def load_from_s3(key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return obj['Body'].read()

@functools.lru_cache(maxsize=1)
def get_index():
    index_bytes = load_from_s3('legal_cases.index')
    return faiss.deserialize_index(index_bytes)

@functools.lru_cache(maxsize=1)
def get_embeddings():
    embeddings_bytes = load_from_s3('embeddings.npy')
    return np.load(io.BytesIO(embeddings_bytes))

@functools.lru_cache(maxsize=1)
def get_chunks():
    chunks_bytes = load_from_s3('all_chunks.pkl')
    return pickle.loads(chunks_bytes)

@functools.lru_cache(maxsize=1)
def get_model():
    temp_dir = tempfile.mkdtemp()
    try:
        # List all objects in the my_qa_model folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='my_qa_model/')
        
        # Download each file in the folder
        for obj in response.get('Contents', []):
            if obj['Key'].endswith('/'):  # Skip directories
                continue
            file_name = os.path.basename(obj['Key'])
            local_file_path = os.path.join(temp_dir, file_name)
            s3.download_file(bucket_name, obj['Key'], local_file_path)
        
        # Load the model from the temporary directory
        model = AutoModelForSeq2SeqLM.from_pretrained(temp_dir)
        return model
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)

# Load resources
index = get_index()
embeddings = get_embeddings()
chunks = get_chunks()
model = get_model()
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")

# Configure Gemini API
genai.configure(api_key=os.getenv('API_KEY'))

# Load the FAISS index and embeddings
index = faiss.read_index("legal_cases.index")
embeddings = np.load('embeddings.npy')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

# Load QA model and tokenizer
model_path = "./my_qa_model"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

def generate_question_embedding(question):
    model = "models/text-embedding-004"
    result = genai.embed_content(
        model=model,
        content=question,
        task_type="retrieval_document",
        title="Embedding of question"
    )
    embedding = result['embedding']
    embedding_array = np.array(embedding).reshape(1, -1)
    print(f"Question embedding dimensions: {embedding_array.shape}")
    return embedding_array

def retrieve_chunks(question, index, chunks, top_k=3):
    question_embedding = generate_question_embedding(question)
    D, I = index.search(question_embedding, top_k)
    retrieved_chunks = [chunks[idx] for idx in I[0]]
    return " ".join(retrieved_chunks)

def answer_question(question, confidence_threshold=0.1):
    # Retrieve relevant chunks
    context = retrieve_chunks(question, index, chunks)
    title_pattern = r'\[ TITLE : .*?\[.*?\] SGHC \d+.*?\ ]'
    titles = re.findall(title_pattern, context)
    context = re.sub(title_pattern, '', context)

    # remove duplicate titles
    titles = list(set(titles))
    titles = list(set(clean_title(title) for title in titles))

    references = " You may find the following cases useful: " + ", ".join(titles) if titles else " No references found."
    
    # Prepare input
    input_text = f"question: {question} context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate answer
    model.eval()
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=64, num_return_sequences=1, output_scores=True, return_dict_in_generate=True)

    # Decode the generated answer
    predicted_answer = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
    if predicted_answer == "":
        predicted_answer = "I apologise - I can't seem to find an answer."

    # Calculate confidence score
    scores = torch.stack(outputs.scores, dim=1)
    log_probs = F.log_softmax(scores, dim=-1)
    token_log_probs = torch.gather(log_probs, -1, outputs.sequences[:, 1:].unsqueeze(-1)).squeeze(-1)
    sequence_log_prob = token_log_probs.sum(dim=-1)
    confidence = torch.exp(sequence_log_prob / outputs.sequences.shape[1]).item()

    # Return the result
    result = {
        'predicted_answer': predicted_answer + " " + references if confidence > confidence_threshold else 
        predicted_answer + " However, the confidence is below the threshold, and the answer may not be reliable." + references,
        'confidence': confidence,
    }

    return result

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.json
    question = data.get('query')
    result = answer_question(question)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)