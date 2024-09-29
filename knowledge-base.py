import streamlit as st
import requests
from bs4 import BeautifulSoup
import markdownify

# Function to fetch webpage content
def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch {url}: {e}")
        return None

# Function to convert HTML to Markdown
def convert_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body  # We focus on body content for conversion
    if body_content:
        return markdownify.markdownify(str(body_content))
    return ""

# Streamlit app setup
st.title("Markdown Converter")

# Input field for URLs
urls_input = st.text_area("Enter URLs (one per line):")

# Button to run the conversion
if st.button("Run"):
    urls = urls_input.splitlines()
    if not urls:
        st.warning("Please enter at least one URL.")
    else:
        # Output file name
        output_file = "output.txt"
        
        # Open file to write markdown data
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in urls:
                if url.strip():  # Skip empty lines
                    st.write(f"Processing {url}...")
                    html_content = fetch_content(url.strip())
                    if html_content:
                        markdown_data = convert_to_markdown(html_content)
                        file.write(f"Content from: {url}\n\n")
                        file.write(markdown_data)
                        file.write("\n\n---\n\n")  # Add a separator between different URLs
        st.success(f"Markdown data saved to {output_file}")

        # Option to download the file
        with open(output_file, "rb") as file:
            btn = st.download_button(label="Download output.txt", data=file, file_name="output.txt", mime="text/plain")