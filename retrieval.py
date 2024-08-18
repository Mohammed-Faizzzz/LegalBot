import faiss
import numpy as np
import pickle
import csv
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from extraction import remove_title

# Load environment variables
load_dotenv()

# Load the embeddings, index, chunks, and QA pairs
embeddings = np.load('embeddings.npy')
index = faiss.read_index('legal_cases.index')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

# Load the all-mpnet-base-v2 model
model = SentenceTransformer('all-mpnet-base-v2')

def generate_question_embedding(question, model):
    """
    Generates an embedding for a question using the all-mpnet-base-v2 model.

    Args:
        question (str): The question text.

    Returns:
        numpy.ndarray: The embedding generated for the question.
    """
    embedding = model.encode(question)
    return np.array(embedding).reshape(1, -1)

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
    question_embedding = generate_question_embedding(question, model)
    D, I = index.search(question_embedding, k=top_k)
    retrieved_chunks = [chunks[idx] for idx in I[0]]
    return " ".join(retrieved_chunks)

def process_qa_pairs(qa_pairs):
    """
    Processes a list of QA pairs and formats them for T5 model training.

    Args:
        qa_pairs (list): A list of dictionaries with 'question' and 'answer'.

    Returns:
        None
    """
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

# Example usage (if you have qa_pairs data available)
# process_qa_pairs(qa_pairs)
