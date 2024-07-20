import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, T5ForConditionalGeneration
from sentence_transformers import SentenceTransformer
import torch

# Load your data
df = pd.read_csv('dataset.csv')

# select only the first 200 rows for demonstration
df = df.head(200)

# Convert to Hugging Face Dataset
dataset = Dataset.from_pandas(df)

# Split the dataset
dataset = dataset.train_test_split(test_size=0.2)

# Save the dataset
dataset.save_to_disk("dataset")

# Initialize SentenceTransformer for context embeddings
embedding_model_name = "all-MiniLM-L6-v2"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
embedding_model = SentenceTransformer(embedding_model_name, device=device)

# Generate embeddings for the context
def generate_context_embeddings(contexts, model):
    return model.encode(contexts, show_progress_bar=True, convert_to_numpy=True)

# Tokenize the dataset with context embeddings
model_checkpoint = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def preprocess_function(examples):
    inputs = [inp.strip() for inp in examples["input"]]
    targets = [t.strip() for t in examples["target"]]
    
    # Assuming the input format is already "question: ... context: ..."
    # If not, you might need to modify this part
    
    # Extract contexts (everything after "context: ")
    contexts = [inp.split("context: ", 1)[1] if "context: " in inp else "" for inp in inputs]
    
    # Generate embeddings for the contexts
    context_embeddings = generate_context_embeddings(contexts, embedding_model)
    
    model_inputs = tokenizer(
        inputs,
        max_length=512,
        padding="max_length",
        truncation=True,
    )
    
    # Tokenize targets (answers)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets,
            max_length=128,
            padding="max_length",
            truncation=True,
        )

    model_inputs["labels"] = labels["input_ids"]
    model_inputs["context_embeddings"] = context_embeddings.tolist()  # Add context embeddings to the inputs
    return model_inputs

# Apply the preprocessing function without removing columns
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Now, remove the original columns
columns_to_remove = dataset['train'].column_names
tokenized_dataset = tokenized_dataset.remove_columns(columns_to_remove)

# Save the tokenized dataset
tokenized_dataset.save_to_disk("tokenized_dataset_t5")