import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import json
import csv
import torch

# Initialize SentenceTransformer model
model_name = "all-MiniLM-L6-v2"

# Check for GPU or CPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = SentenceTransformer(model_name, device=device)

embeddings = np.load('embeddings.npy')
index = faiss.read_index('legal_cases.index')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

qa_pairs = json.load(open('legal_qa_dataset.json'))

def generate_question_embedding(question, model):
    question_embedding = model.encode([question], show_progress_bar=False)
    return question_embedding

def retrieve_chunks(question, index, chunks, model, top_k=5):
    # Generate embedding for the question
    question_embedding = generate_question_embedding(question, model)
    
    D, I = index.search(question_embedding, k=top_k)
    print(I[0])
    
    # Retrieve the top chunks (i.e., best matches)
    retrieved_chunks = [chunks[idx] for idx in I[0]]
    return retrieved_chunks

# Process each question-answer pair
for pair in qa_pairs:
    question = pair['question']
    retrieved_chunks = retrieve_chunks(question, index, chunks, model)
    pair['context'] = retrieved_chunks

# Save the updated qa_pairs into a CSV file
with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['question', 'answer', 'context'])
    writer.writeheader()
    for pair in qa_pairs:
        writer.writerow({
            'question': pair['question'],
            'answer': pair['answer'],
            'context': pair['context']
        })

# Save the updated qa_pairs into a JSON file
with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(qa_pairs, f, indent=4)
