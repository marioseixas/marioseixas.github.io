---
categories:
  - Code
tags:
  - linux
  - scripts
comment: 'https://github.com/Wazzabeee/copy-spotter'
info: aberto.
date: '2024-06-01'
type: post
layout: post
published: true
slug: copy-spotter-ordered
title: 'Ordering "Copy Spotter" results'

---

```python
import base64
import email
from bs4 import BeautifulSoup
import pandas as pd

# Path to the .mhtml file
mhtml_file_path = "<!-- INSERT PATH -->"
output_file_path = "<!-- INSERT PATH -->"

# Function to extract HTML content from .mhtml file
def extract_html_from_mhtml(file_path):
    with open(file_path, 'rb') as file:
        mhtml_content = file.read()

    # Parse the mhtml content
    msg = email.message_from_bytes(mhtml_content)

    # Find the HTML part
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload(decode=True)
            return html_content.decode('utf-8')

    return None

# Function to parse HTML and extract table data
def parse_html_table(html_content):
    soup = BeautifulSoup(html_content, 'html5lib')
    table = soup.find('table')
    return pd.read_html(str(table))[0]

# Function to process and sort the table data
def process_and_sort_table(df):
    # Extract the document names from the first row and column
    document_names = df.iloc[0, 1:].tolist()
    df = df.iloc[1:, 1:]
    df.columns = document_names
    df.index = document_names

    # Melt the DataFrame to get pairs and their similarity scores
    melted_df = df.reset_index().melt(id_vars='index', var_name='Document Pair', value_name='Similarity Score')
    melted_df.columns = ['Document 1', 'Document 2', 'Similarity Score']

    # Drop NaN values and convert similarity scores to numeric
    melted_df = melted_df.dropna()
    melted_df['Similarity Score'] = pd.to_numeric(melted_df['Similarity Score'], errors='coerce')

    # Sort the DataFrame by similarity scores
    sorted_df = melted_df.sort_values(by='Similarity Score', ascending=False)
    return sorted_df

# Function to write the sorted pairs to a text file
def write_sorted_pairs_to_file(sorted_df, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for index, row in sorted_df.iterrows():
            file.write(f"Pair: {row['Document 1']} - {row['Document 2']}, Similarity Score: {row['Similarity Score']}\n")

# Main script execution
html_content = extract_html_from_mhtml(mhtml_file_path)
if html_content:
    df = parse_html_table(html_content)
    sorted_df = process_and_sort_table(df)
    write_sorted_pairs_to_file(sorted_df, output_file_path)
    print(f"Sorted pairs have been written to {output_file_path}")
else:
    print("No HTML content found in the .mhtml file.")
```
