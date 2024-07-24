import numpy as np
from chunk import chunk_text
import os
import google.generativeai as genai
from tqdm import tqdm
import faiss
from dotenv import load_dotenv

# Load environment variables and configure Gemini API
load_dotenv() 
API_KEY = os.getenv('API_KEY')
if API_KEY is None:
    raise ValueError("API_KEY environment variable is not set")
genai.configure(api_key=API_KEY)

def get_gemini_embedding(text):
    """
    Generates an embedding for a single text chunk using Gemini API.

    Args:
        text (str): A text chunk.

    Returns:
        numpy.ndarray: The embedding generated for the text chunk.
    """
    model = "models/text-embedding-004"
    result = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document",
        title="Embedding of text chunk"
    )
    embedding = result['embedding']
    return np.array(embedding)

def generate_embeddings():
    """
    Generates embeddings for a list of text chunks using Gemini API.

    Returns:
        numpy.ndarray: An array of embeddings generated for each text chunk.
    """
    pdf_dir = './../pdfs'
    pdf_files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]
    chunks = chunk_text(pdf_files)

    embeddings = []
    for chunk in tqdm(chunks, desc="Generating embeddings"):
        embedding = get_gemini_embedding(chunk)
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


generate_embeddings()
index_embeddings()