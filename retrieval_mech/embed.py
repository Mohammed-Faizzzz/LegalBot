import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from extraction import extract_data
from chunk import split_into_chunks
import pickle

chunks = pickle.load(open('all_chunks.pkl', 'rb'))

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks.

    Args:
        chunks (list): A list of text chunks.

    Returns:
        list: A list of embeddings generated for each text chunk.
    """
    embeddings = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors='pt', max_length=512, truncation=True, padding=True)
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        embeddings.append(embedding)
    return embeddings

embeddings = generate_embeddings(chunks)
embeddings = np.vstack(embeddings)  # Shape: (num_chunks, embedding_dim)

np.save('embeddings.npy', embeddings)