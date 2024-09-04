import zipfile
import re
import os

def extract_and_clean_txt_files(zip_file_path, output_file_path):
    # Regular expression patterns to match English words, URLs, HTML tags, special characters, and non-Hindi characters
    english_pattern = re.compile(r'[a-zA-Z]+')   # Matches English words
    url_pattern = re.compile(r'http[s]?://\S+|://\S+')  # Matches URLs
    html_tags_pattern = re.compile(r'<[^>]+>|{{[^}]+}}|\[\[|\]\]|\|')  # Matches HTML/XML tags, templates, and wiki markup
    special_char_pattern = re.compile(r'[^\u0900-\u097F\s]')  # Matches any non-Hindi characters and special symbols
    extra_whitespace_pattern = re.compile(r'\s+')  # Matches extra whitespace

    # String to hold the cleaned text
    cleaned_text = ""

    print("Starting extraction from ZIP file...")

    # Extract and process files from the ZIP folder
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('.txt'):
                print(f"Processing file: {file_name}")
                with zip_ref.open(file_name) as file:
                    content = file.read().decode('utf-8')

                    # Remove unwanted patterns
                    content_no_english = english_pattern.sub('', content)
                    content_no_urls = url_pattern.sub('', content_no_english)
                    content_no_html = html_tags_pattern.sub('', content_no_urls)
                    content_no_special = special_char_pattern.sub('', content_no_html)

                    # Clean up extra whitespace and newlines
                    content_cleaned = extra_whitespace_pattern.sub(' ', content_no_special).strip()

                    # Add cleaned content to the final text
                    cleaned_text += content_cleaned + "\n"

    print("All files processed. Writing to output file...")

    # Write the cleaned text to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)

    print(f"Process completed! Cleaned text saved to {output_file_path}")

# Provide the path to your ZIP file and the output file name
zip_file_path = 'hindi_wiki_aug24.zip'
output_file_path = 'cleaned_text.txt'

# Call the function to extract, clean, and save the text files
extract_and_clean_txt_files(zip_file_path, output_file_path)
