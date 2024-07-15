from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from datasets import load_from_disk
import torch
# from evaluate import load
import numpy as np
import collections
import torch.nn.functional as F

# Load model and tokenizer
model_path = "./my_qa_model"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load dataset
dataset = load_from_disk("dataset")
tokenized_dataset = load_from_disk("tokenized_dataset")
test_dataset = tokenized_dataset["test"]


def get_predictions(model, dataset, tokenizer, confidence_threshold=0.1):
    model.eval()
    predictions = []
    
    for item in dataset:
        # The inputs are already tokenized, so we just need to convert to tensors
        inputs = {
            'input_ids': torch.tensor([item['input_ids']]),
            'attention_mask': torch.tensor([item['attention_mask']])
        }
        
        # Get the model output
        with torch.no_grad():
            outputs = model(**inputs)
        
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits
        
        # Get the most likely beginning and end of the answer
        answer_start = torch.argmax(start_logits)
        answer_end = torch.argmax(end_logits)
        
        # Calculate confidence scores
        start_probs = F.softmax(start_logits, dim=1)
        end_probs = F.softmax(end_logits, dim=1)
        start_confidence = start_probs.max().item()
        end_confidence = end_probs.max().item()
        overall_confidence = start_confidence * end_confidence
        
        # Get top 5 start and end positions
        top_5_starts = torch.topk(start_probs, 5, dim=1)
        top_5_ends = torch.topk(end_probs, 5, dim=1)
        
        # Convert the token indices to actual text
        predicted_answer = tokenizer.decode(item['input_ids'][answer_start:answer_end+1])
        
        # Decode the full input to get the question and context
        full_text = tokenizer.decode(item['input_ids'])
        
        # Split the full text into question and context
        # Assuming the format is: [CLS] Question [SEP] Context [SEP]
        split_text = full_text.split('[SEP]')
        question = split_text[0].replace('[CLS]', '').strip()
        context = split_text[1].strip() if len(split_text) > 1 else ''
        
        # Get the actual answer
        actual_answer = tokenizer.decode(item['input_ids'][item['start_positions']:item['end_positions']+1])
        
        prediction = {
            'question': question,
            'context': context,  # first 100 chars of context
            'predicted_answer': predicted_answer if overall_confidence > confidence_threshold else "Unable to find an answer",
            'actual_answer': actual_answer,
            'confidence': overall_confidence,
            'start_confidence': start_confidence,
            'end_confidence': end_confidence,
            'top_5_starts': [(pos.item(), prob.item()) for pos, prob in zip(top_5_starts.indices[0], top_5_starts.values[0])],
            'top_5_ends': [(pos.item(), prob.item()) for pos, prob in zip(top_5_ends.indices[0], top_5_ends.values[0])],
        }
        
        predictions.append(prediction)
    
    return predictions

# Use the function
test_predictions = get_predictions(model, test_dataset, tokenizer)

# Print detailed results
for i, pred in enumerate(test_predictions[:5]):  # Print first 5 predictions
    print(f"Prediction {i+1}:")
    print(f"Question: {pred['question']}")
    print(f"Context: {pred['context']}")
    print(f"Predicted Answer: {pred['predicted_answer']}")
    print(f"Actual Answer: {pred['actual_answer']}")
    print(f"Overall Confidence: {pred['confidence']:.4f}")
    print(f"Start Confidence: {pred['start_confidence']:.4f}")
    print(f"End Confidence: {pred['end_confidence']:.4f}")
    print("Top 5 start positions (position, probability):")
    for pos, prob in pred['top_5_starts']:
        print(f"  {pos}: {prob:.4f}")
    print("Top 5 end positions (position, probability):")
    for pos, prob in pred['top_5_ends']:
        print(f"  {pos}: {prob:.4f}")
    print("---")

# Calculate and print average confidence
avg_confidence = sum(pred['confidence'] for pred in test_predictions) / len(test_predictions)
print(f"\nAverage confidence: {avg_confidence:.4f}")