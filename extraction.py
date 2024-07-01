import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

pdf_path = './../pdfs/[2024] SGHC 133.pdf'
text = extract_text_from_pdf(pdf_path)
# print(text[:1000])
