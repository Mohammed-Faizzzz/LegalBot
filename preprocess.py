import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer

df = pd.read_csv('dataset.csv')
df = df.head(200)
dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2)
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

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Remove the original columns
columns_to_remove = dataset['train'].column_names
tokenized_dataset = tokenized_dataset.remove_columns(columns_to_remove)

tokenized_dataset.save_to_disk("tokenized_dataset_t5")