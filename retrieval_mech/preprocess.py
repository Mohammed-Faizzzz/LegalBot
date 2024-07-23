import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer

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

# Tokenize the dataset
model_checkpoint = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def preprocess_function(examples):
    inputs = [inp.strip() for inp in examples["input"]]
    targets = [t.strip() for t in examples["target"]]
    
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
    return model_inputs

# Apply the preprocessing function
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Remove the original columns
columns_to_remove = dataset['train'].column_names
tokenized_dataset = tokenized_dataset.remove_columns(columns_to_remove)

# Save the tokenized dataset
tokenized_dataset.save_to_disk("tokenized_dataset_t5")