import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from extraction import extract_data
import pickle
import os

def split_into_chunks(text, title, max_length=512, overlap=50):
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

# Extract text from PDF
pdf_dir = './../pdfs'

# List all PDF files in the directory
pdf_files = [os.path.join(pdf_dir, file) for file in os.listdir(pdf_dir) if file.endswith('.pdf')]

all_chunks = []

for pdf in pdf_files:
    print(f"Processing: {pdf}")
    data = extract_data(pdf)
    title = data["Title"]
    text = data["Text"]
    chunks = split_into_chunks(text, title)
    all_chunks.extend(chunks)

# Save all chunks to a single pickle file
with open('all_chunks.pkl', 'wb') as f:
    pickle.dump(all_chunks, f)

print(f"Total chunks processed: {len(all_chunks)}")
print("Sample chunk: ", all_chunks[1][:500])