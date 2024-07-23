import faiss
import numpy as np
import pickle
import json
import csv
import re
import google.generativeai as genai
import os

def remove_title(text):
    # Use regular expression to remove [TITLE: ... [YYYY] SGHC XXX]
    cleaned_text = re.sub(r'\[TITLE:.*?\[.*?\] SGHC \d+.*?\]', '', text)
    return cleaned_text

# Initialize Gemini API
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

# Load embeddings and index
embeddings = np.load('embeddings.npy')
index = faiss.read_index('legal_cases.index')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

qa_pairs = json.load(open('legal_qa_dataset.json'))

def generate_question_embedding(question):
    model = genai.GenerativeModel('gemini-pro')
    question_embedding = model.embed_content(question)
    return np.array(question_embedding).reshape(1, -1)

def retrieve_chunks(question, index, chunks, top_k=3):
    # Generate embedding for the question
    question_embedding = generate_question_embedding(question)
    
    D, I = index.search(question_embedding, k=top_k)
    
    # Retrieve the top chunks (i.e., best matches)
    retrieved_chunks = [chunks[idx] for idx in I[0]]

    res = ""

    for i in range(len(retrieved_chunks)):
        curr = remove_title(retrieved_chunks[i])
        res += curr + "\n"

    return res

# Process each question-answer pair
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

# Save the T5 formatted data into a JSON file
with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(t5_format_data, f, indent=4)