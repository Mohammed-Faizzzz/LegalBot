from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch
import torch.nn.functional as F
import sys

# Load model and tokenizer
model_path = "./my_qa_model"
model = AutoModelForQuestionAnswering.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

def get_single_prediction(model, tokenizer, question, context, confidence_threshold=0.1):
    model.eval()
    
    # Tokenize input
    inputs = tokenizer.encode_plus(question, context, return_tensors='pt')
    
    # Get model output
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
    predicted_answer = tokenizer.decode(inputs['input_ids'][0][answer_start:answer_end+1])
    
    prediction = {
        'question': question,
        'context': context,
        'predicted_answer': predicted_answer if overall_confidence > confidence_threshold else "Unable to find an answer",
        'confidence': overall_confidence,
        'start_confidence': start_confidence,
        'end_confidence': end_confidence,
        'top_5_starts': [(pos.item(), prob.item()) for pos, prob in zip(top_5_starts.indices[0], top_5_starts.values[0])],
        'top_5_ends': [(pos.item(), prob.item()) for pos, prob in zip(top_5_ends.indices[0], top_5_ends.values[0])],
    }
    
    return prediction

if __name__ == "__main__":
    # Example usage
    question = sys.argv[1]
    context = "The court has ruled that the case is to be dismissed due to lack of evidence."

    prediction = get_single_prediction(model, tokenizer, question, context)

    # Print detailed result
    print(f"Question: {prediction['question']}")
    print(f"Context: {prediction['context']}")
    print(f"Predicted Answer: {prediction['predicted_answer']}")
    print(f"Overall Confidence: {prediction['confidence']:.4f}")
    print(f"Start Confidence: {prediction['start_confidence']:.4f}")
    print(f"End Confidence: {prediction['end_confidence']:.4f}")
    print("Top 5 start positions (position, probability):")
    for pos, prob in prediction['top_5_starts']:
        print(f"  {pos}: {prob:.4f}")
    print("Top 5 end positions (position, probability):")
    for pos, prob in prediction['top_5_ends']:
        print(f"  {pos}: {prob:.4f}")
