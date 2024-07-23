import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
import pickle
import torch

# Load the FAISS index and embeddings
index = faiss.read_index("legal_cases.index")
embeddings = np.load('embeddings.npy')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

# Load QA model and tokenizer
model_path = "./my_qa_model"
qa_model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Create QA pipeline
qa_pipeline = pipeline("text2text-generation", model=qa_model, tokenizer=tokenizer)

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# Modify retrieve_chunks function to use the embedding model
def retrieve_chunks(question, index, chunks, embedding_model, k=5):
    question_embedding = embedding_model.encode([question], show_progress_bar=False)
    _, I = index.search(question_embedding, k)
    return [chunks[i] for i in I[0]]

# Using the query, retrieve relevant chunks and format into input for the QA model
def answer_question(question):
    retrieved_chunks = retrieve_chunks(question, index, chunks, embedding_model)
    context = " ".join(retrieved_chunks)
    input_text = f"question: {question} context: {context}"
    
    # Use the pipeline for generation
    output = qa_pipeline(input_text, max_length=64, num_return_sequences=1)
    
    # The output is a list of dictionaries, we take the first one
    predicted_answer = output[0]['generated_text']
    return predicted_answer

def main():
    print("Enter your query (type 'exit' to quit):")
    while True:
        user_query = input("Query: ")
        if user_query.lower() == 'exit':
            break
        
        # Get the answer from the QA model
        answer = answer_question(user_query)
        
        print(f"Answer: {answer}\n")

if __name__ == "__main__":
    main()