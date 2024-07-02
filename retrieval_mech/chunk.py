import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from extraction import extract_text_from_pdf
import pickle

# Extract text from PDF
pdf_path = './../pdfs/[2024] SGHC 133.pdf'
text = extract_text_from_pdf(pdf_path)

# def split_into_chunks(text, max_length=512):
#     sentences = sent_tokenize(text)
#     chunks = []
#     chunk = ""
#     for sentence in sentences:
#         if len(chunk) + len(sentence) > max_length:
#             chunks.append(chunk)
#             chunk = sentence
#         else:
#             chunk += " " + sentence
#     chunks.append(chunk)
#     return chunks

def split_into_chunks(text, max_length=512, overlap = 50):
    sentences = sent_tokenize(text)
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) > max_length:
            chunks.append(chunk.strip())
            chunk = " ".join(chunk.split()[-overlap:]) + " " + sentence
        else:
            chunk += " " + sentence
    chunks.append(chunk)
    return chunks

chunks = split_into_chunks(text)

with open('chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)
# print("start: ", chunks[1], ":end")

