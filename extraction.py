import fitz  # PyMuPDF
import re

def extract_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Extract Title
    title_pattern = re.compile(r"\[\d{4}\] SGHC \d+")
    title_match = title_pattern.search(text)
    title = title_match.group(0) if title_match else "Title not found"

    # Extract Category
    # Extract Parties Involved

    data = {
        "Title": title,
        "Text": text
    }
    return data

# pdf_path = "./../pdfs/[2024] SGHC 133.pdf"
# data = extract_data(pdf_path)
# print(data["Title"])