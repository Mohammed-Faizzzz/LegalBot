import fitz  # PyMuPDF
import re
import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW

def extract_pdf_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    # Extract Title
    title_pattern = re.compile(r"\[\d{4}\] SGHC \d+")
    title_match = title_pattern.search(text)
    title = title_match.group(0) if title_match else "Title not found"

    data = {
        "Title": title,
        "Text": text
    }
    return data

def process_multiple_pdfs(pdf_folder):
    all_data = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            data = extract_pdf_data(pdf_path)
            all_data.append(data)
    
    df = pd.DataFrame(all_data)
    
    # Save the extracted data to a CSV file
    df.to_csv('extracted_data.csv', index=False)
    return df

pdf_folder = "pdfs"
df = process_multiple_pdfs(pdf_folder)
# print(df)

# Load the dataset
titles = df['Title'].tolist()
texts = df['Text'].tolist()

# Define custom dataset
class TextDataset(Dataset):
    def __init__(self, titles, texts, tokenizer, max_length, overlap_length):
        self.examples = []
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.overlap_length = overlap_length

        # Preprocess each text to split into overlapping chunks and associate with titles
        for title, text in zip(titles, texts):
            tokens = tokenizer(text, truncation=False, return_tensors='pt')['input_ids'].squeeze()
            start = 0
            while start < len(tokens):
                end = min(start + max_length, len(tokens))
                chunk = tokens[start:end]
                self.examples.append((title, chunk))
                start += max_length - overlap_length

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        title, chunk = self.examples[idx]

        # Padding if necessary
        padding_length = self.max_length - chunk.size(0)
        if padding_length > 0:
            chunk = torch.cat([chunk, torch.zeros(padding_length, dtype=torch.long)])

        attention_mask = torch.ones(chunk.size(0), dtype=torch.long)
        attention_mask[chunk == 0] = 0  # Set attention mask to 0 where there's padding

        return {
            'title': title,
            'input_ids': chunk,
            'attention_mask': attention_mask,
            'labels': chunk
        }

# Initialize tokenizer and dataset
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
max_length = 512
overlap_length = 50  # Define the overlap length
dataset = TextDataset(titles, texts, tokenizer, max_length, overlap_length)

# Example of how to access the dataset
for data in dataset:
    print(f"Title: {data['title']}")
    print(f"Input IDs: {data['input_ids']}")
    print(f"Attention Mask: {data['attention_mask']}")
    print(f"Labels: {data['labels']}")
    break  # Remove this break to print all data

# Create DataLoader
batch_size = 4
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize model
model = GPT2LMHeadModel.from_pretrained('gpt2-medium')

# Move model to GPU if available
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Set up the optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)

# Training loop
num_epochs = 3
model.train()

for epoch in range(num_epochs):
    for batch in dataloader:
        optimizer.zero_grad()
        
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        
        optimizer.step()

    print(f"Epoch {epoch + 1} completed with loss: {loss.item()}")
