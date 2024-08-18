import numpy as np
import faiss
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pickle
import torch
import torch.nn.functional as F
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import re
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

def clean_title(title):
    # Remove '[ TITLE : ' from the beginning and ']' from the end
    cleaned = title.replace('[ TITLE : ', '').rstrip(']')
    # Remove any leading/trailing whitespace
    return cleaned.strip()

# Load environment variables
load_dotenv()

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

# Load the all-mpnet-base-v2 model
embedding_model = SentenceTransformer('all-mpnet-base-v2')

def generate_question_embedding(question, model):
    """
    Generates an embedding for a question using the all-mpnet-base-v2 model.

    Args:
        question (str): The question text.

    Returns:
        numpy.ndarray: The embedding generated for the question.
    """
    embedding = model.encode(question)
    embedding_array = np.array(embedding).reshape(1, -1)
    print(f"Question embedding dimensions: {embedding_array.shape}")
    return embedding_array

def retrieve_chunks(question, index, chunks, top_k=3):
    """
    Retrieves the most relevant text chunks for a given question.

    Args:
        question (str): The question text.
        index (faiss.Index): The FAISS index of the embeddings.
        chunks (list): List of text chunks.
        top_k (int): Number of top chunks to retrieve.

    Returns:
        str: A string containing the retrieved chunks concatenated.
    """
    question_embedding = generate_question_embedding(question, embedding_model)
    D, I = index.search(question_embedding, top_k)
    retrieved_chunks = [chunks[idx] for idx in I[0]]
    return " ".join(retrieved_chunks)

def answer_question(question, confidence_threshold=0.1):
    """
    Answers a question by retrieving relevant chunks and using a QA model to generate an answer.

    Args:
        question (str): The question text.
        confidence_threshold (float): Threshold for confidence below which the answer may not be reliable.

    Returns:
        dict: A dictionary containing the predicted answer and confidence.
    """
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
    app.run(host="0.0.0.0", port=8080)
