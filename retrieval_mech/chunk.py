import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

from extraction import extract_data
import pickle
import os
import random
import csv
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # print(words)
    
    return ' '.join(words)

# Apply preprocessing
chunk = "Your text chunk here."
cleaned_chunk = preprocess_text(chunk)


def split_into_chunks(text, title, max_length=512, overlap=50):
    """
    Splits the given text into chunks based on the maximum length and overlap.

    Args:
        text (str): The input text to be split into chunks.
        title (str): The title of the text.
        max_length (int, optional): The maximum length of each chunk. Defaults to 512.
        overlap (int, optional): The number of words to overlap between chunks. Defaults to 50.

    Returns:
        list: A list of chunks, where each chunk is a string.
    """
    sentences = sent_tokenize(text)
    chunks = []
    chunk = []
    chunk_length = 0
    
    for sentence in sentences:
        sentence_tokens = word_tokenize(sentence)
        sentence_length = len(sentence_tokens)
        
        if chunk_length + sentence_length > max_length:
            chunks.append(f"[TITLE: {title}] " + " ".join(chunk).strip())
            chunk = chunk[-overlap:] + sentence_tokens
            chunk_length = len(chunk)
        else:
            chunk.extend(sentence_tokens)
            chunk_length += sentence_length
    
    if chunk:
        chunks.append(f"[TITLE: {title}] " + " ".join(chunk).strip())
    
    return chunks



"""
Iterate over all pdf files, extract their title and text, then chunk them. Store ALL chunks
in a single pickle file.

"""
pdf_dir = './../pdfs'
pdf_files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]

all_chunks = []

all_qns = []

for pdf in pdf_files:
    # print(f"Processing: {pdf}")
    data = extract_data(pdf)
    title = data["Title"]
    text = data["Text"]

    # Preprocess the text
    # cleaned_text = preprocess_text(text)

    # Split the text into chunks and store them
    chunks = split_into_chunks(text, title)
    all_chunks.extend(chunks)
    # print(all_chunks[:5])

with open('all_chunks.pkl', 'wb') as f:
    pickle.dump(all_chunks, f)
