import numpy as np
import faiss
import google.generativeai as genai
import os
import pickle
from tqdm import tqdm

# Load environment variables and configure Gemini API
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

def get_gemini_embedding(text):
    """
    Generates an embedding for a single text chunk using Gemini API.

    Args:
        text (str): A text chunk.

    Returns:
        numpy.ndarray: The embedding generated for the text chunk.
    """
    model = genai.GenerativeModel('gemini-pro')
    embedding = model.embed_content(text)
    return np.array(embedding)

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks using Gemini API.

    Args:
        chunks (list): A list of text chunks.

    Returns:
        numpy.ndarray: An array of embeddings generated for each text chunk.
    """
    embeddings = []
    for chunk in tqdm(chunks, desc="Generating embeddings"):
        embedding = get_gemini_embedding(chunk)
        embeddings.append(embedding)
    return np.array(embeddings)

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

# Main execution
chunks = pickle.load(open('all_chunks.pkl', 'rb'))
embeddings = generate_embeddings(chunks)
np.save('embeddings.npy', embeddings)
index_embeddings()