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
    text = re.sub(r'^.*version no.*\n?', '', text, flags= re.MULTILINE)
    
    res = "".join([char for char in text if char.isalnum() or char.isspace()])
    return res


def split_into_chunks(text, title, max_length=512, overlap=50):
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

# # Example usage
# pdf_path = "./../pdfs/[2024] SGHC 145.pdf"
# data = extract_data(pdf_path)
# title = data["Title"]
# text = data["Text"]
# text = preprocess_text(text)
# chunks = split_into_chunks(text, title)

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
    text = preprocess_text(text)

    # Split the text into chunks and store them
    chunks = split_into_chunks(text, title)
    all_chunks.extend(chunks)
    # print(len(all_chunks))
    # print length of longest chunk
    # print("Max:", max([len(chunk) for chunk in chunks]))
    # print(all_chunks[:5])

with open('all_chunks.pkl', 'wb') as f:
    pickle.dump(all_chunks, f)
