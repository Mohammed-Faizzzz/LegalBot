import fitz  # PyMuPDF
import re

def extract_data(pdf_path):
    """
    Extracts data from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary containing the extracted data. The dictionary has two keys:
            - "Title": The title of the document and parties involved, extracted from the PDF text.
            - "Text": The full text content of the PDF. The text is also cleaned for repeated titles.

    """
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count
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
    last_page = doc.load_page(num_pages - 1)  # Page indexing starts from 0
    first_line = last_page.get_text("text").splitlines()[0]  # Extract the first line of text
    second_line = last_page.get_text("text").splitlines()[2]  # Extract the second line of text
    print(second_line)
    #  if second line is a number, it is a page number and not a party involved
    if second_line.isdigit():
        title = first_line + " " + title
    else:
        title = first_line + " " + second_line + " " + title
        

    # Find the second instance of the title match and remove anything before it
    title_matches = list(title_pattern.finditer(text))
    if len(title_matches) >= 2:
        second_instance_start = title_matches[1].start()
        text = text[second_instance_start:]

        title_to_remove = title_matches[1].group(0)
        text = re.sub(re.escape(title_to_remove) + r'\s*', '', text)

    data = {
        "Title": title,
        "Text": text
    }
    return data

def remove_title(text):
    # Use regular expression to remove [TITLE: ... [YYYY] SGHC XXX]
    cleaned_text = re.sub(r'\[TITLE:.*?\[.*?\] SGHC \d+.*?\]', '', text)
    return cleaned_text

def preprocess_text(text):
    """
    Preprocesses the given text by converting it to lowercase, removing any lines containing "version no",
    and removing any non-alphanumeric characters except spaces.

    Args:
        text (str): The text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """
    text = text.lower()
    text = re.sub(r'^.*version no.*\n?', '', text, flags=re.MULTILINE)
    
    res = "".join([char for char in text if char.isalnum() or char.isspace()])
    return res


pdf_path = "./../pdfs/[2024] SGHC 136.pdf"
data = extract_data(pdf_path)
print(data["Title"])