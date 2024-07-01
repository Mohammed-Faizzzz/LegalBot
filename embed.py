import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from extraction import extract_text_from_pdf
from chunk import split_into_chunks

# Extract text from PDF
pdf_path = './../pdfs/[2024] SGHC 133.pdf'
text = extract_text_from_pdf(pdf_path)
chunks = split_into_chunks(text)

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors='pt', max_length=512, truncation=True, padding=True)
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        embeddings.append(embedding)
    return embeddings

embeddings = generate_embeddings(chunks)
embeddings = np.vstack(embeddings)  # Shape: (num_chunks, embedding_dim)

np.save('embeddings.npy', embeddings)