from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer, AutoTokenizer
from datasets import load_from_disk
from sentence_transformers import SentenceTransformer
import torch

# Load the SentenceTransformer model for embeddings
embedding_model_name = "all-MiniLM-L6-v2"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
embedding_model = SentenceTransformer(embedding_model_name, device=device)

# Load the QA model for fine-tuning
qa_model_checkpoint = "distilbert-base-uncased-distilled-squad"
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(qa_model_checkpoint)

# Load the tokenized dataset from disk
tokenized_dataset = load_from_disk("tokenized_dataset")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    dataloader_num_workers=4,
    dataloader_prefetch_factor=4,
)

# Initialize the Trainer
trainer = Trainer(
    model=qa_model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
)

def main():
    trainer.train()
    trainer.save_model("./my_qa_model")

if __name__ == '__main__':
    main()
