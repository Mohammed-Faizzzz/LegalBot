from transformers import AutoModelForSeq2SeqLM, TrainingArguments, Trainer, AutoTokenizer, EarlyStoppingCallback
from datasets import load_from_disk
import torch

# ignore and do not display warnings
import warnings
warnings.filterwarnings("ignore")

# Load the QA model for fine-tuning
qa_model_checkpoint = "t5-base"
qa_model = AutoModelForSeq2SeqLM.from_pretrained(qa_model_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(qa_model_checkpoint)

# Load the tokenized dataset from disk
tokenized_dataset = load_from_disk("tokenized_dataset_t5")

early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=3)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=10,
    weight_decay=0.1,
    warmup_steps=100,
    use_cpu=True,
    gradient_accumulation_steps=4,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    dataloader_num_workers=4,  # Ensure num_workers is greater than 0 for multiprocessing
    dataloader_prefetch_factor=2,
)

# Initialize the Trainer
trainer = Trainer(
    model=qa_model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    callbacks=[early_stopping_callback],
)

def main():
    trainer.train()
    trainer.save_model("./my_qa_model")

if __name__ == '__main__':
    main()