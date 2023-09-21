import requests
from bs4 import BeautifulSoup
import streamlit as st
from tqdm import tqdm
import random
import pandas as pd
import base64

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    # Add more user agents as needed
]

# Function to scrape title from URL with a random user agent
def scrape_title(url):
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        title_elements = soup.find_all('title')
        if title_elements:
            return title_elements[0].get_text()
    return "Title not found"

# Function to create download links
def get_table_download_link(data, filename, text):
    if data is not None:
        # Encode the HTML content as bytes
        data_bytes = data.encode()
        b64 = base64.b64encode(data_bytes).decode()
        return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'
    return ""

# Streamlit UI
st.title("Web Page Title Scraper")

# User input for URLs
user_input = st.text_area("Enter URLs, one per line", height=200)
user_input = user_input.strip().split('\n')

# Display the number of URLs entered
st.write(f"Number of URLs Entered: {len(user_input)}")

# Use a set to keep track of processed URLs
processed_urls = set()

if st.button("Scrape Titles"):
    st.write("Scraping titles...")
    progress_bar = st.progress(0)
    titles = []

    for i, url in enumerate(tqdm(user_input)):
        # Check if the URL ends with "/"
        if url.strip().endswith('/'):
            title = scrape_title(url.strip())
            titles.append((url.strip(), title))
            progress_bar.progress((i + 1) / len(user_input))

    # Display total executed URLs
    st.write(f"Total Executed URLs: {len(processed_urls)}")

    # Create a DataFrame for the results
    df = pd.DataFrame(titles, columns=["URL", "Title"])

    # Show results in a nice table
    st.write("Results:")
    st.write(df)

    # Allow users to download results in HTML and XLSX formats
    st.markdown(f"### Download Results")
    
    # Download as HTML
    html_file = df.to_html(index=False, escape=False)
    st.markdown(get_table_download_link(html_file, "result.html", "Download HTML"), unsafe_allow_html=True)
    
    # Download as XLSX
    excel_file = df.to_excel("result.xlsx", index=False, engine="openpyxl")
    excel_file.seek(0)  # Reset the file pointer to the beginning
    st.markdown(get_table_download_link(excel_file.read(), "result.xlsx", "Download XLSX"), unsafe_allow_html=True)
