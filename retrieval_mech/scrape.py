# import requests
# from bs4 import BeautifulSoup
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import fitz  # PyMuPDF
# import re
# import pickle
# from nltk.tokenize import word_tokenize
# import nltk
# from extraction import extract_data, preprocess_text
# from chunk import split_into_chunks

# nltk.download('punkt', quiet=True)

# def download_and_process_judgment(url, all_chunks):
#     driver = webdriver.Chrome()
#     driver.get(url)

#     try:
#         downloads_path = os.path.expanduser("~/Downloads")
#         files_prev = len(os.listdir(downloads_path))
#         print("files_prev: ", files_prev)

#         # Try the first button
#         try:
#             download_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/a[2]"))
#             )
#             download_button.click()
#             time.sleep(30)
#         except (TimeoutException):
#             print("First button not clickable or not found. Trying second button.")
        
#         files = len(os.listdir(downloads_path))
#         print("files after first attempt: ", files)

#         # If no new file, try the second button
#         if files == files_prev:
#             try:
#                 download_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/a[3]"))
#                 )
#                 download_button.click()
#                 time.sleep(30)
#             except (TimeoutException):
#                 print("Second button not clickable or not found. Skipping this URL.")
#                 return
        
#         files = len(os.listdir(downloads_path))
#         print("files after second attempt: ", files)

#         # Check if a new file was downloaded
#         if files > files_prev:
#             # Get the downloaded file name
#             new_files = sorted(os.listdir(downloads_path), key=lambda x: os.path.getmtime(os.path.join(downloads_path, x)), reverse=True)
#             file_path = os.path.join(downloads_path, new_files[0])

#             # Process the file
#             chunks = process_file(file_path)
#             all_chunks.extend(chunks)

#             # Delete the file
#             os.remove(file_path)
#             print(f"Processed and deleted: {file_path}")
#         else:
#             print("No new file was downloaded.")

#     except Exception as e:
#         print(f"An error occurred while processing {url}: {str(e)}")

#     finally:
#         driver.quit()


# def process_file(file_path):
#     data = extract_data(file_path)
#     title = data["Title"]
#     text = data["Text"]

#     # Preprocess the text
#     text = preprocess_text(text)

#     # Split the text into chunks and store them
#     chunks = split_into_chunks(text, title)
#     return chunks

# def main():
#     all_chunks = []
#     for i in range(1, 192):  # From 1 to 191
#         url = f"https://www.elitigation.sg/gd/s/2024_SGHC_{i}"
#         print(f"Processing: {url}")
#         download_and_process_judgment(url, all_chunks)
#         time.sleep(2)  # Add a small delay between requests to be polite
#         print(f"Total chunks processed and saved: {len(all_chunks)}")

#     # Save all chunks
#     with open('all_chunks.pkl', 'wb') as f:
#         pickle.dump(all_chunks, f)
    
#     print(f"Total chunks processed and saved: {len(all_chunks)}")

# if __name__ == "__main__":
#     main()


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

def download_and_process_judgment(url, all_chunks, log_file):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        downloads_path = os.path.expanduser("~/Downloads")
        files_prev = len(os.listdir(downloads_path))

        # Try the first button
        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/a[2]"))
            )
            download_button.click()
            time.sleep(30)
        except (TimeoutException):
            print("First button not clickable or not found. Trying second button.")
        
        files = len(os.listdir(downloads_path))

        # If no new file, try the second button
        if files == files_prev:
            try:
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/nav/a[3]"))
                )
                download_button.click()
                time.sleep(30)
            except (TimeoutException):
                print("Second button not clickable or not found. Skipping this URL.")
                return
        
        files = len(os.listdir(downloads_path))

        # Check if a new file was downloaded
        if files > files_prev:
            # Get the downloaded file name
            new_files = sorted(os.listdir(downloads_path), key=lambda x: os.path.getmtime(os.path.join(downloads_path, x)), reverse=True)
            file_path = os.path.join(downloads_path, new_files[0])

            # Process the file
            chunks = process_file(file_path)
            all_chunks.extend(chunks)

            # Log the processed file
            log_message = f"Processed and added to all_chunks.pkl: {file_path} (URL: {url})\n"
            print(log_message.strip())
            log_file.write(log_message)

            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print("No new file was downloaded.")

    except Exception as e:
        error_message = f"An error occurred while processing {url}: {str(e)}\n"
        print(error_message.strip())
        log_file.write(error_message)

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

def check_page_exists(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return 'Page Not Found' not in soup.get_text()
    except requests.RequestException:
        return False

def main():
    all_chunks = []
    log_file_path = 'processed_files_log.txt'
    
    with open(log_file_path, 'w') as log_file:
        for year in range(2000, 2025):  # From 2000 to 2024
            i = 1
            consecutive_not_found = 0
            while consecutive_not_found < 5:  # Stop after 5 consecutive "not found" pages
                url = f"https://www.elitigation.sg/gd/s/{year}_SGHC_{i}"
                print(f"Checking: {url}")
                if check_page_exists(url):
                    print(f"Processing: {url}")
                    download_and_process_judgment(url, all_chunks, log_file)
                    consecutive_not_found = 0
                else:
                    print(f"Page not found: {url}")
                    log_file.write(f"Page not found: {url}\n")
                    consecutive_not_found += 1
                time.sleep(2)  # Add a small delay between requests to be polite
                i += 1
            print(f"Finished processing year {year}")
            log_file.write(f"Finished processing year {year}\n")

        # Save all chunks
        with open('all_chunks.pkl', 'wb') as f:
            pickle.dump(all_chunks, f)
        
        final_message = f"Total chunks processed and saved: {len(all_chunks)}\n"
        print(final_message.strip())
        log_file.write(final_message)

    print(f"Log file saved to: {log_file_path}")

if __name__ == "__main__":
    main()