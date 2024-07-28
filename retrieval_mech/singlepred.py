import numpy as np
import faiss
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import pickle
import torch
import torch.nn.functional as F
from retrieval import retrieve_chunks
import sys
import os

print("Script started")
print(f"Current working directory: {os.getcwd()}")

# Adjust paths for resources
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")

# Load the FAISS index and embeddings
index_path = os.path.join(project_root, "legal_cases.index")
embeddings_path = os.path.join(project_root, 'embeddings.npy')
chunks_path = os.path.join(project_root, 'all_chunks.pkl')

print(f"Loading index from: {index_path}")
index = faiss.read_index(index_path)
print(f"Loading embeddings from: {embeddings_path}")
embeddings = np.load(embeddings_path)
print(f"Loading chunks from: {chunks_path}")
with open(chunks_path, 'rb') as f:
    chunks = pickle.load(f)

# Load QA model and tokenizer
model_path = os.path.join(current_dir, "my_qa_model")
print(f"Loading model from: {model_path}")
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")
model.to(device)

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

def answer_question(question, confidence_threshold=0.1):
    print(f"Received question: {question}")
    # Retrieve relevant chunks
    context = retrieve_chunks(question, index, chunks, embedding_model)
    
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
        predicted_answer = "Unable to find an answer"

    # Calculate confidence score
    scores = torch.stack(outputs.scores, dim=1)
    log_probs = F.log_softmax(scores, dim=-1)
    token_log_probs = torch.gather(log_probs, -1, outputs.sequences[:, 1:].unsqueeze(-1)).squeeze(-1)
    sequence_log_prob = token_log_probs.sum(dim=-1)
    confidence = torch.exp(sequence_log_prob / outputs.sequences.shape[1]).item()

    # Return the result
    result = {
        'predicted_answer': predicted_answer if confidence > confidence_threshold else "Unable to find an answer",
        'confidence': confidence,
    }

    print(f"Generated answer: {result['predicted_answer']}")
    print(f"Confidence: {result['confidence']:.4f}")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a question as an argument.")
        sys.exit(1)
    
    question = sys.argv[1]
    result = answer_question(question)
    print(f"Final Answer: {result['predicted_answer']}")
    print(f"Confidence: {result['confidence']:.4f}")