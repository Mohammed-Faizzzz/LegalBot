import fitz  # PyMuPDF
import re

def extract_data(pdf_path):
    """
    Extracts data from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary containing the extracted data. The dictionary has two keys:
            - "Title": The title of the document, extracted from the PDF text.
            - "Text": The full text content of the PDF.

    """
    doc = fitz.open(pdf_path)
    text = ""
    first_page = doc[0]

    for page in doc:
        text += page.get_text()

    # Extract Title
    title_pattern = re.compile(r"\[\d{4}\] SGHC \d+")
    title_match = title_pattern.search(text)
    title = title_match.group(0) if title_match else "Title not found"

    # Extract Category
    first_page_text = first_page.get_text()
    pad = len("JUDGMENT")
    judgment_start = first_page_text.find("JUDGMENT")
    if judgment_start == -1:
        judgment_start = first_page_text.find("GROUNDS OF DECISION")
        pad = len("GROUNDS OF DECISION")
    version_start = first_page_text.find("Version")
    category = first_page_text[judgment_start + pad: version_start]

    # Extract Parties Involved
    pattern = re.compile(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*\s+v\s+[A-Za-z]+(?:\s[A-Za-z]+)*\b')
    
    # Find all matches in the text
    matches = pattern.findall(text)
    
    print(matches)

    data = {
        "Title": title,
        "Text": text
    }
    return data

# Example usage
pdf_path = "./../pdfs/[2024] SGHC 131.pdf"
data = extract_data(pdf_path)
