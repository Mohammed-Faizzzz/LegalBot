import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from chunk import chunk_text
import os

def generate_embeddings():
    """
    Generates embeddings for a list of text chunks using SentenceTransformer.

    Args:
        chunks (list): A list of text chunks.

    Returns:
        numpy.ndarray: An array of embeddings generated for each text chunk.
    """
    pdf_dir = './../pdfs'
    pdf_files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]
    chunks = chunk_text(pdf_files)

    model_name = "all-MiniLM-L6-v2"
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SentenceTransformer(model_name, device=device)

    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    embeddings = np.vstack(embeddings)  # Shape: (num_chunks, embedding_dim)
    np.save('embeddings.npy', embeddings)
    return embeddings
