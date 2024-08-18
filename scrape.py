import requests
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import fitz  # PyMuPDF
import re
import pickle
from nltk.tokenize import word_tokenize
import nltk
from extraction import extract_data, preprocess_text
from chunk import split_into_chunks

nltk.download('punkt', quiet=True)

def download_and_process_judgment(url, all_chunks):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        downloads_path = os.path.expanduser("~/Downloads")
        files_prev = len(os.listdir(downloads_path))
        print("files_prev: ", files_prev)

        # Try the first button
        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/a[2]"))
            )
            download_button.click()
            time.sleep(30)
        except (TimeoutException, NoSuchElementException):
            print("First button not clickable or not found. Trying second button.")
        
        files = len(os.listdir(downloads_path))
        print("files after first attempt: ", files)

        # If no new file, try the second button
        if files == files_prev:
            try:
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/a[3]"))
                )
                download_button.click()
                time.sleep(30)
            except (TimeoutException, NoSuchElementException):
                print("Second button not clickable or not found. Skipping this URL.")
                return
        
        files = len(os.listdir(downloads_path))
        print("files after second attempt: ", files)

        # Check if a new file was downloaded
        if files > files_prev:
            # Get the downloaded file name
            new_files = sorted(os.listdir(downloads_path), key=lambda x: os.path.getmtime(os.path.join(downloads_path, x)), reverse=True)
            file_path = os.path.join(downloads_path, new_files[0])

            # Process the file
            chunks = process_file(file_path)
            all_chunks.extend(chunks)

            # Delete the file
            os.remove(file_path)
            print(f"Processed and deleted: {file_path}")
        else:
            print("No new file was downloaded.")

    except Exception as e:
        print(f"An error occurred while processing {url}: {str(e)}")

    finally:
        driver.quit()


def process_file(file_path):
    data = extract_data(file_path)
    title = data["Title"]
    text = data["Text"]

    # Preprocess the text
    text = preprocess_text(text)

    # Split the text into chunks and store them
    chunks = split_into_chunks(text, title)
    return chunks

def main():
    all_chunks = []
    for i in range(1, 212):  # From 1 to 211
        url = f"https://www.elitigation.sg/gd/s/2024_SGHC_{i}"
        print(f"Processing: {url}")
        download_and_process_judgment(url, all_chunks)
        time.sleep(2)  # Add a small delay between requests to be polite
        print(f"Total chunks processed and saved: {len(all_chunks)}")

    # Save all chunks
    with open('all_chunks.pkl', 'wb') as f:
        pickle.dump(all_chunks, f)
    
    print(f"Total chunks processed and saved: {len(all_chunks)}")

if __name__ == "__main__":
    main()