import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# Define a list of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    # Add more user agents as needed
]

# Streamlit UI
st.title("Web Title Scraper")

# User input for URLs
st.write("Enter the URLs you want to scrape (separated by line breaks):")
user_input = st.text_area("Input URLs", "")

# Function to get title from URL
def get_title_from_url(url):
    try:
        # Choose a random user agent from the list
        user_agent = random.choice(user_agents)

        # Set the User-Agent header in the request
        headers = {
            'User-Agent': user_agent
        }

        # Send an HTTP GET request to the URL with the selected user agent
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the title tag within the HTML
            title_tag = soup.find('title')

            # Extract the text from the title tag
            if title_tag:
                title = title_tag.text
                return title
            else:
                # If title tag is not found, find the h1 tag
                h1_tag = soup.find('h1')
                if h1_tag:
                    title = h1_tag.text
                    return title
                else:
                    return "Title not found"
        else:
            return f'Failed to retrieve the web page from {url}.'
    except Exception as e:
        return f'An error occurred while processing {url}: {str(e)}'

# Process user input and display titles
if st.button("Scrape Titles"):
    urls = user_input.split("\n")
    for url in urls:
        title = get_title_from_url(url.strip())
        st.write(f'Title of {url}: {title}')
