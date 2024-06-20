import fitz  # PyMuPDF
import re
import pandas as pd

def extract_pdf_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    print(text[:1000])
    
    # Extract Title
    title_pattern = re.compile(r"\[\d{4}\] SGHC \d+")
    title_match = title_pattern.search(text)
    title = title_match.group(0) if title_match else "Title not found"
    
    # Extract Parties Involved
    parties_pattern = re.compile(r"\[\d{4}\] SGHC \d+.*?Between(.*?)JUDGMENT", re.DOTALL)
    parties_match = parties_pattern.search(text)
    parties = parties_match.group(1).strip() if parties_match else "Parties not found"
    print(parties)
    # Extract Classification
    pattern = r"JUDGMENT.*?(\[.*?\])"
    
    # Search for all matches in the text
    matches = re.findall(pattern, text, re.DOTALL)
    
    # Extract the enclosed information from each match
    extracted_info = []
    for match in matches:
        # Find all bracketed parts within each match
        individual_infos = re.findall(r"\[.*?\]", match)
        extracted_info.extend(individual_infos)
    classification = ", ".join(extracted_info)
    
    print(classification)

    # Extract Date
    date_pattern = re.compile(r"Version No \d+: (\d{2} \w+ \d{4})")
    date_match = date_pattern.search(text)
    date = date_match.group(1) if date_match else "Date not found"
    
    # Extract Other Info
    other_info_pattern = re.compile(r"General Division of the High Court — Originating Claim No \d+ of \d+ \((.+?)\)\s+Kwek Mean Luck J\s+(\d{1,2} \w+, \d{1,2}, \d{4})", re.DOTALL)
    other_info_match = other_info_pattern.search(text)
    if other_info_match:
        court_type = "General Division of the High Court"
        judge = other_info_match.group(1).strip()
        judgment_dates = other_info_match.group(2).strip()
        other_info = f"Court Type: {court_type}, Judge: {judge}, Judgment Dates: {judgment_dates}"
    else:
        other_info = "Other info not found"
    
    # Extract Paragraphs
    paragraphs_pattern = re.compile(r"(\d+)\s+([\s\S]*?)(?=\n\d+\s+|\Z)", re.MULTILINE)
    paragraphs = paragraphs_pattern.findall(text)
    
    # Organize data
    initial_data = {
        "Title": title,
        "Parties Involved": parties,
        "Classification": classification,
        "Date": date,
        "Other Info": other_info
    }
    
    # Create DataFrames
    initial_df = pd.DataFrame([initial_data])
    paragraph_data = []
    
    for num, para in paragraphs:
        paragraph_data.append({
            "Title": title,
            # "Subtitle": subtitle,
            "Paragraph": f"Para {num}\n{para.strip()}"
        })
    
    paragraphs_df = pd.DataFrame(paragraph_data)
    
    # Save to CSV
    initial_df.to_csv("initial_data.csv", index=False)
    paragraphs_df.to_csv("paragraphs_data.csv", index=False)

    return initial_df, paragraphs_df

# Use the function
pdf_path = "pdfs/[2024] SGHC 135.pdf"
initial_df, paragraphs_df = extract_pdf_data(pdf_path)
print("Initial Data:")
print(initial_df)
# print("\nParagraphs Data:")
# print(paragraphs_df)
