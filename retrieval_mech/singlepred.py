import sys
import os
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import faiss
import numpy as np
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adjust paths for resources
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

def load_resources():
    logger.info("Loading resources...")
    qa_model = AutoModelForQuestionAnswering.from_pretrained(os.path.join(current_dir, "my_qa_model"))
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_dir, "my_qa_model"))
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index(os.path.join(project_root, 'legal_cases.index'))
    with open(os.path.join(project_root, 'all_chunks.pkl'), 'rb') as f:
        chunks = pickle.load(f)
    logger.info("Resources loaded successfully.")
    return qa_model, tokenizer, embedding_model, index, chunks

def retrieve_context(question, embedding_model, index, chunks, top_k=5):
    logger.info(f"Retrieving context for question: {question}")
    question_embedding = embedding_model.encode([question], show_progress_bar=False)
    D, I = index.search(question_embedding, k=top_k)
    retrieved_chunks = [chunks[idx] for idx in I[0]]
    return " ".join(retrieved_chunks)

def answer_question(question, qa_model, tokenizer, embedding_model, index, chunks):
    logger.info(f"Generating answer for question: {question}")
    context = retrieve_context(question, embedding_model, index, chunks)
    
    # Truncate the context to fit within the model's maximum sequence length
    max_length = 512  # This is typically the max length for BERT-based models
    inputs = tokenizer(question, context, truncation=True, max_length=max_length, return_tensors="pt")
    
    with torch.no_grad():
        outputs = qa_model(**inputs)
    
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.decode(inputs.input_ids[0][answer_start:answer_end])
    
    return answer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        question = "What constitutes a breach of contract?"
    else:
        question = sys.argv[1]
    
    try:
        print(f"Processing question: {question}")
        qa_model, tokenizer, embedding_model, index, chunks = load_resources()
        answer = answer_question(question, qa_model, tokenizer, embedding_model, index, chunks)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logger.exception("Detailed error information:")