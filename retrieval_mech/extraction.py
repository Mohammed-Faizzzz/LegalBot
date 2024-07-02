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
