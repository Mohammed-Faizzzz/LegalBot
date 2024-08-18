import numpy as np
from chunk import chunk_text
import os
from tqdm import tqdm
import faiss
from sentence_transformers import SentenceTransformer

def get_mpnet_embedding(text, model):
    """
    Generates an embedding for a single text chunk using the all-mpnet-base-v2 model.

    Args:
        text (str): A text chunk.
        model (SentenceTransformer): The loaded sentence transformer model.

    Returns:
        numpy.ndarray: The embedding generated for the text chunk.
    """
    embedding = model.encode(text)
    return embedding

def generate_embeddings():
    """
    Generates embeddings for a list of text chunks using all-mpnet-base-v2 model.

    Returns:
        numpy.ndarray: An array of embeddings generated for each text chunk.
    """
    # Load the all-mpnet-base-v2 model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Define the directory containing PDF files
    pdf_dir = './../pdfs'
    pdf_files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]
    
    # Chunk the text from the PDF files
    chunks = chunk_text(pdf_files)

    embeddings = []
    for chunk in tqdm(chunks, desc="Generating embeddings"):
        embedding = get_mpnet_embedding(chunk, model)
        embeddings.append(embedding)

    embeddings = np.array(embeddings)
    np.save('embeddings.npy', embeddings)
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

# Generate embeddings and index them
generate_embeddings()
index_embeddings()
