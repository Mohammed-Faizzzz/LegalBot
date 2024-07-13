import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from extraction import extract_data
from chunk import split_into_chunks
import pickle

chunks = pickle.load(open('all_chunks.pkl', 'rb'))

# Use a SentenceTransformer model
model_name = "all-MiniLM-L6-v2"

# Check for GPU or CPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = SentenceTransformer(model_name, device=device)

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks using SentenceTransformer.

    Args:
        chunks (list): A list of text chunks.

    Returns:
        numpy.ndarray: An array of embeddings generated for each text chunk.
    """
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    return embeddings

embeddings = generate_embeddings(chunks)
embeddings = np.vstack(embeddings)  # Shape: (num_chunks, embedding_dim)

np.save('embeddings.npy', embeddings)
