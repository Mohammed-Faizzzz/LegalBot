import faiss
import numpy as np
import pickle
import json
import csv
import google.generativeai as genai
import os
from extraction import remove_title

# Load environment variables and configure Gemini API
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

# Load the embeddings, index, chunks, and QA pairs
embeddings = np.load('embeddings.npy')
index = faiss.read_index('legal_cases.index')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

def generate_question_embedding(question):
    model = genai.GenerativeModel('gemini-pro')
    question_embedding = model.embed_content(question)
    return np.array(question_embedding).reshape(1, -1)

def retrieve_chunks(question, index, chunks, top_k=3):
    question_embedding = generate_question_embedding(question)
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
        retrieved_chunks = retrieve_chunks(question, index, chunks)

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
