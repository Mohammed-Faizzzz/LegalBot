import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch

# Load your data
df = pd.read_csv('dataset.csv')

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
model_checkpoint = "distilbert-base-uncased-distilled-squad"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def preprocess_function(examples):
    questions = [q.strip() for q in examples["question"]]
    contexts = [c.strip() for c in examples["context"]]
    
    # Generate embeddings for the contexts
    context_embeddings = generate_context_embeddings(contexts, embedding_model)
    
    inputs = tokenizer(
        questions,
        contexts,
        max_length=384,
        truncation="only_second",
        return_offsets_mapping=True,
        padding="max_length",
    )

    offset_mapping = inputs.pop("offset_mapping")
    answers = examples["answer"]
    start_positions = []
    end_positions = []

    for i, offset in enumerate(offset_mapping):
        answer = answers[i]
        start_char = contexts[i].find(answer)
        end_char = start_char + len(answer)
        sequence_ids = inputs.sequence_ids(i)

        # Find the start and end of the context
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # If the answer is not fully inside the context, label is (0, 0)
        if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            # Otherwise it's the start and end token positions
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char:
                idx += 1
            start_positions.append(idx - 1)

            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char:
                idx -= 1
            end_positions.append(idx + 1)

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    inputs["context_embeddings"] = context_embeddings.tolist()  # Add context embeddings to the inputs
    return inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

# Save the tokenized dataset
tokenized_dataset.save_to_disk("tokenized_dataset")
