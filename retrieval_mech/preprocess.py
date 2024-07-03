import spacy
import random
import re
import pickle

"""
Generates Question Answer pairs for training of QA model from text chunks.
"""

nlp = spacy.load("en_core_web_sm")

def generate_legal_questions(text, title):
    doc = nlp(text)
    questions = []

    # Generic legal questions
    questions.extend([
        f"What is the case {title} about?",
        f"Who were the parties involved in the case {title}?",
        f"What was the main legal issue in {title}?",
        f"What was the court's decision in {title}?",
        f"What was the court's reasoning in {title}?",
        f"What precedents were cited in {title}?",
        f"What were the key arguments presented in {title}?",
    ])

    # Specific questions based on named entities
    parties = set()
    experts = set()
    legal_terms = set()

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            parties.add(ent.text)
            questions.append(f"What role did {ent.text} play in the case {title}?")
        elif ent.label_ == "ORG":
            parties.add(ent.text)
            questions.append(f"What was {ent.text}'s involvement in the case {title}?")

    # Identify potential experts and legal terms
    expert_patterns = r"\b(expert|consultant|specialist)\b"
    legal_term_patterns = r"\b(clause|agreement|contract|award|application|claim|allegation)\b"

    for sent in doc.sents:
        sent_text = sent.text.lower()
        if re.search(expert_patterns, sent_text):
            for token in sent:
                if token.pos_ == "PROPN" and token.text not in experts:
                    experts.add(token.text)
                    questions.append(f"What was {token.text}'s expert opinion in {title}?")
        
        legal_terms_found = re.findall(legal_term_patterns, sent_text)
        for term in legal_terms_found:
            if term not in legal_terms:
                legal_terms.add(term)
                questions.append(f"What does the {term} refer to in {title}?")

    # Questions about parties
    if parties:
        questions.append(f"What were the main arguments of {' and '.join(list(parties)[:2])} in {title}?")

    # Questions about specific legal aspects
    questions.extend([
        f"What evidence was presented in {title}?",
        f"Were there any dissenting opinions in {title}?",
        f"What remedies were sought in {title}?",
        f"What was the procedural history of {title}?",
        f"Were there any jurisdictional issues in {title}?",
    ])

    return list(set(questions))  # Remove any duplicates


def extract_answers(text, question):
    doc = nlp(text)
    
    if question.startswith("Who"):
        return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    elif question.startswith("What"):
        if "is" in question:
            return [chunk.text for chunk in doc.noun_chunks if chunk.text in question]
        else:
            return [sent.text for sent in doc.sents if any(token.pos_ == "VERB" for token in sent)]
    elif question.startswith("When"):
        return [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]
    elif question.startswith("Where"):
        return [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    elif question.startswith("Why"):
        return [sent.text for sent in doc.sents if any(token.text.lower() in ["because", "since", "as"] for token in sent)]
    elif question.startswith("How"):
        return [sent.text for sent in doc.sents if any(token.pos_ in ["VERB", "ADJ"] for token in sent)]
    
    return []

# def create_qa_pairs(max_questions_per_chunk=5):
#     qa_pairs = []
#     for chunk in chunks:
#         print(type(chunk), chunk)
#         text = chunk['Text']
#         title = chunk['metadata']['Title']
#         questions = generate_questions(text, title)
        
#         # Randomly sample questions if there are more than max_questions_per_chunk
#         if len(questions) > max_questions_per_chunk:
#             questions = random.sample(questions, max_questions_per_chunk)
        
#         for question in questions:
#             # answers = extract_answers(text, question)
#             if answers:
#                 qa_pairs.append({
#                     "context": text,
#                     "question": question,
#                     # "answer": answers[0],  # Take the first answer for simplicity
#                     "title": title
#                 })
#     return qa_pairs

# qa_pairs = create_qa_pairs()
# print(f"Generated {len(qa_pairs)} QA pairs.")
# print(qa_pairs[:5])