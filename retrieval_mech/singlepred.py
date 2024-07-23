import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
import pickle
import torch
import sys
import os

# Adjust paths for resources
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Load the FAISS index and embeddings
index = faiss.read_index(os.path.join(project_root, "legal_cases.index"))
embeddings = np.load(os.path.join(project_root, 'embeddings.npy'))
with open(os.path.join(project_root, 'all_chunks.pkl'), 'rb') as f:
    chunks = pickle.load(f)

# Load QA model and tokenizer
model_path = os.path.join(current_dir, "my_qa_model")
qa_model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Create QA pipeline
qa_pipeline = pipeline("text2text-generation", model=qa_model, tokenizer=tokenizer, device=device)

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

def retrieve_chunks(question, index, chunks, embedding_model, k=5):
    question_embedding = embedding_model.encode([question], show_progress_bar=False)
    _, I = index.search(question_embedding, k)
    return [chunks[i] for i in I[0]]

def answer_question(question):
    retrieved_chunks = retrieve_chunks(question, index, chunks, embedding_model)
    context = " ".join(retrieved_chunks)
    input_text = f"question: {question} context: {context}"
    
    output = qa_pipeline(input_text, max_length=64, num_return_sequences=1)
    
    predicted_answer = output[0]['generated_text']
    return predicted_answer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a question as an argument.")
        sys.exit(1)
    
    question = sys.argv[1]
    print(f"Processing question: {question}")
    answer = answer_question(question)
    print(f"Answer: {answer}")



#     import sys
# import os
# from sentence_transformers import SentenceTransformer
# import torch
# from transformers import AutoModelForQuestionAnswering, AutoTokenizer
# import faiss
# import numpy as np
# import pickle
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Adjust paths for resources
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)

# def load_resources():
#     logger.info("Loading resources...")
#     qa_model = AutoModelForQuestionAnswering.from_pretrained(os.path.join(current_dir, "my_qa_model"))
#     tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_dir, "my_qa_model"))
#     embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#     index = faiss.read_index(os.path.join(project_root, 'legal_cases.index'))
#     with open(os.path.join(project_root, 'all_chunks.pkl'), 'rb') as f:
#         chunks = pickle.load(f)
#     logger.info("Resources loaded successfully.")
#     return qa_model, tokenizer, embedding_model, index, chunks

# def retrieve_context(question, embedding_model, index, chunks, top_k=5):
#     logger.info(f"Retrieving context for question: {question}")
#     question_embedding = embedding_model.encode([question], show_progress_bar=False)
#     D, I = index.search(question_embedding, k=top_k)
#     retrieved_chunks = [chunks[idx] for idx in I[0]]
#     return " ".join(retrieved_chunks)

# def answer_question(question, qa_model, tokenizer, embedding_model, index, chunks):
#     logger.info(f"Generating answer for question: {question}")
#     context = retrieve_context(question, embedding_model, index, chunks)
    
#     # Truncate the context to fit within the model's maximum sequence length
#     max_length = 512  # This is typically the max length for BERT-based models
#     inputs = tokenizer(question, context, truncation=True, max_length=max_length, return_tensors="pt")
    
#     with torch.no_grad():
#         outputs = qa_model(**inputs)
    
#     answer_start = torch.argmax(outputs.start_logits)
#     answer_end = torch.argmax(outputs.end_logits) + 1
#     answer = tokenizer.decode(inputs.input_ids[0][answer_start:answer_end])
    
#     return answer

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         question = "What constitutes a breach of contract?"
#     else:
#         question = sys.argv[1]
    
#     try:
#         print(f"Processing question: {question}")
#         qa_model, tokenizer, embedding_model, index, chunks = load_resources()
#         answer = answer_question(question, qa_model, tokenizer, embedding_model, index, chunks)
#         print(f"Answer: {answer}")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         logger.exception("Detailed error information:")