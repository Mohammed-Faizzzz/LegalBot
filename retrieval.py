import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import json
import csv
import torch
from extraction import remove_title

# Load the SentenceTransformer model
model_name = "all-MiniLM-L6-v2"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = SentenceTransformer(model_name, device=device)

# Load the embeddings, index, chunks, and QA pairs
embeddings = np.load('embeddings.npy')
index = faiss.read_index('legal_cases.index')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

def generate_question_embedding(question, model):
    question_embedding = model.encode([question], show_progress_bar=False)
    return question_embedding

def retrieve_chunks(question, index, chunks, model, top_k=3):
    question_embedding = generate_question_embedding(question, model)
    D, I = index.search(question_embedding, k=top_k)
    retrieved_chunks = [chunks[idx] for idx in I[0]]

    res = ""

    for i in range(len(retrieved_chunks)):
        curr = remove_title(retrieved_chunks[i])
        res += curr + "\n"

    return res

def process_qa_pairs(qa_pairs):
    t5_format_data = []
    for pair in qa_pairs:
        question = pair['question']
        answer = pair['answer']
        retrieved_chunks = retrieve_chunks(question, index, chunks, model)

        # Format for T5
        input_text = f"question: {question} context: {retrieved_chunks}"
        t5_format_data.append({
            'input': input_text,
            'target': answer
        })

    # Save the T5 formatted data into a CSV file
    with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['input', 'target'])
        writer.writeheader()
        for item in t5_format_data:
            writer.writerow(item)

    # # Save the T5 formatted data into a JSON file
    # with open('dataset.json', 'w', encoding='utf-8') as f:
    #     json.dump(t5_format_data, f, indent=4)