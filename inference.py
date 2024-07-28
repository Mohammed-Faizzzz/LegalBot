import numpy as np
import faiss
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import pickle
import torch
import torch.nn.functional as F
from retrieval import retrieve_chunks
import re
from extraction import clean_title

# Load the FAISS index and embeddings
index = faiss.read_index("legal_cases.index")
embeddings = np.load('embeddings.npy')
with open('all_chunks.pkl', 'rb') as f:
    chunks = pickle.load(f)

# Load QA model and tokenizer
model_path = "./my_qa_model"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

def answer_question(question, confidence_threshold=0.1):
    # Retrieve relevant chunks
    context = retrieve_chunks(question, index, chunks, embedding_model)
    title_pattern = r'\[ TITLE : .*?\[.*?\] SGHC \d+.*?\ ]'
    titles = re.findall(title_pattern, context)
    context = re.sub(title_pattern, '', context)

    # remove duplicate titles
    titles = list(set(titles))
    titles = list(set(clean_title(title) for title in titles))

    references = " You may find the following cases useful: " + ", ".join(titles) if titles else " No references found."
    
    # Prepare input
    input_text = f"question: {question} context: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Generate answer
    model.eval()
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=64, num_return_sequences=1, output_scores=True, return_dict_in_generate=True)

    # Decode the generated answer
    predicted_answer = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
    if predicted_answer == "":
        predicted_answer = "Unable to find an answer."

    # Calculate confidence score
    scores = torch.stack(outputs.scores, dim=1)
    log_probs = F.log_softmax(scores, dim=-1)
    token_log_probs = torch.gather(log_probs, -1, outputs.sequences[:, 1:].unsqueeze(-1)).squeeze(-1)
    sequence_log_prob = token_log_probs.sum(dim=-1)
    confidence = torch.exp(sequence_log_prob / outputs.sequences.shape[1]).item()

    # Return the result
    result = {
        'predicted_answer': predicted_answer + " " + references if confidence > confidence_threshold else 
        predicted_answer + " However, the confidence is below the threshold, and the answer may not be reliable." + references,
        'confidence': confidence,
    }

    return result

def main():
    print("Enter your query (type 'exit' to quit):")
    while True:
        user_query = input("Query: ")
        if user_query.lower() == 'exit':
            break
        
        # Get the answer from the QA model
        result = answer_question(user_query)
        
        print(f"Answer: {result['predicted_answer']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print()

if __name__ == "__main__":
    main()