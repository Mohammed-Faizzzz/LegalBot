from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
import torch
# from evaluate import load
import numpy as np
import collections
import torch.nn.functional as F

# Load model and tokenizer
model_path = "./my_qa_model"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load dataset
tokenized_dataset = load_from_disk("tokenized_dataset_t5")
test_dataset = tokenized_dataset["test"]

def get_predictions(model, dataset, tokenizer, confidence_threshold=0.1):
    model.eval()
    predictions = []
    
    for item in dataset:
        # The input is already tokenized, so we just need to convert to tensors
        inputs = {
            'input_ids': torch.tensor([item['input_ids']]),
            'attention_mask': torch.tensor([item['attention_mask']])
        }
        
        # Get the model output
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=64, num_return_sequences=1, output_scores=True, return_dict_in_generate=True)
        
        # Decode the generated answer
        predicted_answer = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
        
        # Calculate confidence score (using the mean of log probabilities)
        scores = torch.stack(outputs.scores, dim=1)
        log_probs = F.log_softmax(scores, dim=-1)
        token_log_probs = torch.gather(log_probs, -1, outputs.sequences[:, 1:].unsqueeze(-1)).squeeze(-1)
        sequence_log_prob = token_log_probs.sum(dim=-1)
        confidence = torch.exp(sequence_log_prob / outputs.sequences.shape[1]).item()
        
        # Decode the full input to get the question and context
        full_text = tokenizer.decode(item['input_ids'])
        
        # Split the full text into question and context
        # Assuming the format is: "question: [QUESTION] context: [CONTEXT]"
        split_text = full_text.split('context:')
        question = split_text[0].replace('question:', '').strip()
        context = split_text[1].strip() if len(split_text) > 1 else ''
        
        prediction = {
            'question': question,
            'context': context[:100],  # first 100 chars of context
            'predicted_answer': predicted_answer if confidence > confidence_threshold else "Unable to find an answer",
            'actual_answer': tokenizer.decode(item['labels'], skip_special_tokens=True),
            'confidence': confidence,
        }
        
        predictions.append(prediction)
    
    return predictions

# Use the function
test_predictions = get_predictions(model, test_dataset, tokenizer)

# Print detailed results
for i, pred in enumerate(test_predictions[:5]):  # Print first 5 predictions
    print(f"Prediction {i+1}:")
    print(f"Question: {pred['question']}")
    print(f"Predicted Answer: {pred['predicted_answer']}")
    print(f"Actual Answer: {pred['actual_answer']}")
    print(f"Confidence: {pred['confidence']:.4f}")
    print("---")

# Calculate and print average confidence
avg_confidence = sum(pred['confidence'] for pred in test_predictions) / len(test_predictions)
print(f"\nAverage confidence: {avg_confidence:.4f}")