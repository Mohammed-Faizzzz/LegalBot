import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from extraction import extract_data
import pickle
import os

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
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) > max_length:
            chunks.append(f"[TITLE: {title}] " + chunk.strip())
            chunk = " ".join(chunk.split()[-overlap:]) + " " + sentence
        else:
            chunk += " " + sentence
    chunks.append(f"[TITLE: {title}] " + chunk.strip())
    return chunks



"""
Iterate over all pdf files, extract their title and text, then chunk them. Store ALL chunks
in a single pickle file.

"""
pdf_dir = './../pdfs'
pdf_files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]

all_chunks = []

for pdf in pdf_files:
    print(f"Processing: {pdf}")
    data = extract_data(pdf)
    title = data["Title"]
    text = data["Text"]
    chunks = split_into_chunks(text, title)
    all_chunks.extend(chunks)

with open('all_chunks.pkl', 'wb') as f:
    pickle.dump(all_chunks, f)

print(f"Total chunks processed: {len(all_chunks)}")
