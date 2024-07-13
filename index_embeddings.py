import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
import pickle

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks using SentenceTransformer.

    Args:
        chunks (list): A list of text chunks.

    Returns:
        numpy.ndarray: An array of embeddings generated for each text chunk.
    """
    model_name = "all-MiniLM-L6-v2"
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SentenceTransformer(model_name, device=device)
    
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    return embeddings

def index_embeddings():
    """
    Indexes the embeddings using Faiss library with FlatL2 index.

    This function loads the embeddings from 'embeddings.npy' file,
    creates a FlatL2 index using Faiss library, adds the embeddings to the index,
    and saves the index to 'legal_cases.index' file.

    Returns:
        None
    """
    embeddings = np.load('embeddings.npy')
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    # Save the index
    faiss.write_index(index, 'legal_cases.index')
    print(f"Indexed {index.ntotal} vectors of dimension {d}")

# Assuming chunks are already loaded and preprocessed elsewhere in your code
chunks = pickle.load(open('all_chunks.pkl', 'rb'))
embeddings = generate_embeddings(chunks)
np.save('embeddings.npy', embeddings)
index_embeddings()
