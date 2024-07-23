import numpy as np
import pickle
import os
import google.generativeai as genai
from tqdm import tqdm

# Load environment variables and configure Gemini API
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

# Load chunks
chunks = pickle.load(open('all_chunks.pkl', 'rb'))

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

# Generate embeddings
embeddings = generate_embeddings(chunks)

# Save embeddings
np.save('embeddings.npy', embeddings)