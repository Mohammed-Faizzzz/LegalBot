import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

from extraction import extract_data, preprocess_text
import pickle
import os
import random
import csv
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def split_into_chunks(text, title, max_length=512, overlap=50):
    """
    Splits the given text into chunks with a specified maximum length and overlap.

    Args:
        text (str): The input text to be split into chunks.
        title (str): The title of the text.
        max_length (int, optional): The maximum length of each chunk. Defaults to 512.
        overlap (int, optional): The number of overlapping words between adjacent chunks. Defaults to 50.

    Returns:
        list: A list of chunks, where each chunk is a string.

    """
    words = word_tokenize(text)
    chunks = []
    chunk = []
    title_words = word_tokenize(f"[TITLE: {title}]")
    title_length = len(title_words)
    
    for i, word in enumerate(words):
        if len(chunk) + 1 > max_length - title_length:
            chunks.append(" ".join(title_words + chunk))
            chunk = words[max(0, i-overlap):i]
        chunk.append(word)
    
    if chunk:
        chunks.append(" ".join(title_words + chunk))
    
    return chunks

def chunk_text(pdf_paths):
    """
    Chunk the text from multiple PDF files into smaller chunks.

    Args:
        pdf_paths (list): A list of file paths to the PDF files.

    Returns:
        list: A list of chunks containing the extracted text from the PDF files.
    """
    all_chunks = []
    for pdf in pdf_paths:
        data = extract_data(pdf)
        title = data["Title"]
        text = data["Text"]

        # Preprocess the text
        text = preprocess_text(text)

        # Split the text into chunks and store them
        chunks = split_into_chunks(text, title)
        all_chunks.extend(chunks)
    
    with open('all_chunks.pkl', 'wb') as f:
        pickle.dump(all_chunks, f)
    
    return all_chunks

