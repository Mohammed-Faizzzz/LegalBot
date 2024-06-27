# !pip install fitz
# !pip install pymupdf
# !pip install transformers

import fitz  # PyMuPDF
import re
import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForCausalLM, AdamW
from torch.cuda.amp import GradScaler, autocast

# Convert PDF to tensor
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
            tokens = tokenizer(text, truncation=True, return_tensors='pt')['input_ids'].squeeze()
            start = 0
            while start < len(tokens):
                end = min(start + max_length, len(tokens))
                chunk = tokens[start:end]
                if len(chunk) > 0:  # Ensure there is content in the chunk
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
model_name = 'meta-llama/Meta-Llama-3-8B'
tokenizer = AutoTokenizer.from_pretrained(model_name)
max_length = 512
overlap_length = 50  # Define the overlap length
dataset = TextDataset(titles, texts, tokenizer, max_length, overlap_length)

# Ensure the device is set correctly
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Clear CUDA memory
torch.cuda.empty_cache()

# Initialize the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Move the model to the appropriate device
model.to(device)

# Initialize the optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)
scaler = GradScaler()

# Training loop with mixed precision
num_epochs = 3
accumulation_steps = 8
batch_size = 1
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

for epoch in range(num_epochs):
    print(f"Epoch {epoch + 1}")
    model.train()
    epoch_loss = 0
    optimizer.zero_grad()

    for i, batch in enumerate(dataloader):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        with autocast():
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss = loss / accumulation_steps

        scaler.scale(loss).backward()

        if (i + 1) % accumulation_steps == 0:
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()

        epoch_loss += loss.item()

        # Clear up memory after each batch
        del input_ids, attention_mask, labels, outputs
        torch.cuda.empty_cache()

    print(f"Epoch {epoch + 1} completed with average loss: {epoch_loss / len(dataloader)}")


# Set the model to evaluation mode
model.eval()

# Disable gradient calculation
torch.no_grad()

# Example input text for inference
input_text = "[2024] SGHC 136: Trust in the PAP has been shattered. PM Lee has recently said that"

# Tokenize the input text
input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
attention_mask = torch.ones(input_ids.shape, device=device)  # Create attention mask

# Disable gradient calculation
with torch.no_grad():
    # Generate text
    output = model.generate(
        input_ids, 
        attention_mask=attention_mask,
        max_length=100, 
        num_return_sequences=1, 
        no_repeat_ngram_size=2, 
        early_stopping=True,
        pad_token_id=tokenizer.eos_token_id  # Set pad_token_id to eos_token_id
    )

# Decode the output tokens to text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

print("Generated text:", generated_text)
