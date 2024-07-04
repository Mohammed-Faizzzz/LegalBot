import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import pickle

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

embeddings = np.load('embeddings.npy')
index = faiss.read_index('legal_cases.index')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

def generate_question_embedding(question, tokenizer, model):
    inputs = tokenizer(question, return_tensors='pt', max_length=512, truncation=True, padding=True)
    outputs = model(**inputs)
    question_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return question_embedding

def retrieve_chunks(question, index, chunks, tokenizer, model, top_k=5):
    # Generate embedding for the question
    question_embedding = generate_question_embedding(question, tokenizer, model)
    
    D, I = index.search(question_embedding, k=top_k)
    print(I[0])
    
    # Retrieve the top chunks (i.e best matches)
    retrieved_chunks = [chunks[idx] for idx in I[0]]
    return retrieved_chunks

question = "What are the key considerations for varying or rescinding a maintenance order when the paying spouse retires and claims changed financial circumstances, particularly in cases involving elderly parties?"
retrieved_chunks = retrieve_chunks(question, index, chunks, tokenizer, model)

print(f"Question: {question}")
print(f"Retrieved Chunks: {retrieved_chunks}")
# for i, chunk in enumerate(retrieved_chunks):
#     print(f"\nRetrieved Chunk {i + 1}: {chunk}")
