import logging
import os
import re
from io import BytesIO
from pprint import pprint

import chardet
import PyPDF2
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googleapiclient.discovery import build
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import tool
import http.client
import json
from playwright.async_api import async_playwright
import time
from utils.serper_main_utils import bprint, gprint, rprint, summarize_text
import asyncio
from utils.serper_utils import get_website_summary

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
OPENAI_API_KEY = "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"
GOOGLE_API_KEY = "AIzaSyA42ThVNx5QQqUrgJ9JbzcDYwKBDGWvmfg"
# GOOGLE_API_KEY = "AIzaSyA7_qBjRBvn9cyHwI-M5_9ygibvH9w_X0w"
# GOOGLE_API_KEY = "AIzaSyA42ThVNx5QQqUrgJ9JbzcDYwKBDGWvmfg"
GOOGLE_CONTEXT_ID = "b1ad2b402da6c4614"
PINECONE_ENV = "asia-southeast1-gcp-free"


def clean_text(text):
    """
    This function takes a text string as input and returns a cleaned version of the text that is more suitable for a language model.

    Parameters:
    text (str): The text to clean.

    Returns:
    str: The cleaned text.
    """
    # Remove leading and trailing whitespace
    text = text.strip()
    # Replace multiple whitespace characters with a single space
    text = re.sub(r"\s+", " ", text)
    # Replace multiple new lines with a single new line
    text = re.sub(r"\n+", "\n", text)
    return text


def get_pdf_text(url):
    """
    This function takes a URL as input and returns the text content of the PDF file at that URL.

    Parameters:
    url (str): The URL of the PDF file.

    Returns:
    str: The text content of the PDF file.
    """
    try:
        bprint(f"Fetching content from {url}")
        response = requests.get(url, timeout=15)
        print(response.status_code)
        # Check if the request was successful
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # logger.warning(f"HTTP error occurred for {url}: {err}")
        print("excepting")
        return None
    except requests.exceptions.RequestException as err:
        # logger.warning(f"Error occurred for {url}: {err}")
        print("excepting2")
        return None

    # Open the PDF file
    file = BytesIO(response.content)
    pdf = PyPDF2.PdfReader(file)

    # Extract the text from each page of the PDF
    text = ""
    for page in pdf.pages:
        text += page.extract_text((0, 90))

    return text


def get_website_text(url):
    """
    This function takes a URL as input and returns the text content of the webpage.

    Parameters:
    url (str): The URL of the webpage.

    Returns:
    str: The text content of the webpage.
    """
    try:
        print(f"Fetching content from {url}")
        response = requests.get(url, timeout=15)
        print(response.status_code)
        # Check if the request was successful
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred for {url}: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error occurred for {url}: {err}")
        return None

    print("headers['Content-Type']: ", response.headers["Content-Type"])
    # Check the Content-Type of the response
    if "application/pdf" in response.headers["Content-Type"]:
        # The URL points to a PDF file
        return get_pdf_text(url)

    # Detect the encoding of the response content
    encoding = chardet.detect(response.content)["encoding"]

    print("url: ", url)
    print("encoding: ", encoding)

    # Decode the content using the detected encoding
    if encoding is None:
        return None

    decoded_content = response.content.decode(encoding)

    # Parse the HTML and extract the text
    soup = BeautifulSoup(decoded_content, "html.parser")
    lines = soup.get_text().splitlines()
    cleaned_lines = [clean_text(line) for line in lines]
    text = " ".join(cleaned_lines)
    pprint(text)

    return text


# async def get_website_summary(url, topic, chat):
#     """
#     This function takes a URL as input and returns the summary content of the webpage.

#     Parameters:
#     url (str): The URL of the webpage.

#     Returns:
#     str: The summary content of the webpage.
#     """
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()

#         try:
#             bprint(f"Fetching content from {url}")
#             response = await page.goto(url)
#             # response = requests.get(url, timeout=15)
#             # retries = 1
#             # max_retries = 5
#             # while retries <= max_retries:
#             #     try:
#             #         response = await page.goto(url)
#             #         print("response successful")
#             #     except:
#             #         print("go to excepted "+str(retries))
#             #         time.sleep(10)
#             #         retries += 1
#             #         continue
#             #     break

#             # pprint(response)
#             content = await page.inner_html('body')
#             # pprint(content)
#             # response = await page.inner_html('body')
#             # Check if the request was successful
#             # response.raise_for_status()
#         except requests.exceptions.HTTPError as err:
#             st.error(f"HTTP error occurred for {url}: {err}... Skipping")
#             return None
#         except requests.exceptions.RequestException as err:
#             st.error(f"Error occurred for {url}: {err}... Skipping")
#             return None

#         logging.debug("headers['Content-Type']: ", await response.header_value("Content-Type"))

#         # Check the Content-Type of the response
#         if "application/pdf" in await response.header_value("Content-Type"):
#             # The URL points to a PDF file
#             text = get_pdf_text(url)
#             cleaned_text = clean_text(text)
#         else:
#             # Detect the encoding of the response content
#             # encoding = chardet.detect(response.content)["encoding"]

#             logging.debug("url: ", url)
#             # logging.debug("encoding: ", encoding)

#             # Decode the content using the detected encoding
#             # if encoding is None:
#             #     return None

#             try:
#                 # decoded_content = response.content.decode(encoding)
#                 decoded_content = content
#             except UnicodeDecodeError:
#                 return None

#             # Parse the HTML and extract the text
#             soup = BeautifulSoup(decoded_content, "html.parser")
#             # print(soup)
#             # print(soup.get_text())
#             cleaned_text = ""
#             for par in soup.find_all('p'):
#                 # print(par.get_text())
#                 cleaned_text += " "+par.get_text()
#             # print(cleaned_text)
#             # print(cleaned_text)
#             # lines = soup.get_text().splitlines()
#             # cleaned_lines = [clean_text(line) for line in lines]
#             # cleaned_text = " ".join(cleaned_lines)
#             # print(cleaned_text)
#         # Summarize the text
#         summary = summarize_text(text=cleaned_text, topic=topic, chat=chat)
#         print("<--- sum")
#         print(summary)
#         print(type(summary))
#         print("<--- sum end")
#         return summary
#         # return summary


def search_google(query, api_key, cx_id, start_index, num_results=10):
    """
    This function takes a search query, API key, and cx id as input and returns a list of URLs from a Google search.

    Parameters:
    query (str): The search query.
    api_key (str): The API key for Google Custom Search JSON API.
    cx_id (str): The cx id for Google Custom Search JSON API.
    num_results (int): The number of search results to return.

    Returns:
    list: A list of URLs from the Google search.
    """
    bprint(f"Searching Google for {query}")
    service = build("customsearch", "v1", developerKey=api_key)
    res = (
        service.cse()
        .list(q=query, cx=cx_id, start=start_index, num=num_results)
        .execute()
    )
    urls = [item["link"] for item in res["items"]]
    return urls


def search_and_extract_web_url(query: str) -> str:
    """Searches the web for the query and extracts relevant texts."""


    num_results = 5
    successful_extractions = 0
    start_index = 1
    # Initialize an empty string to store the entire extracted texts
    web_extracted_texts = ""
    with open("outputs/web_search_texts.txt", "w") as f:
        while successful_extractions < num_results:
            urls = search_google(
                query, GOOGLE_API_KEY, GOOGLE_CONTEXT_ID, start_index, num_results
            )
            for url in urls:
                print()
                print(f"Processing URL {successful_extractions+1} of {num_results}")
                text = get_website_text(url)
                if text is not None:
                    f.write(
                        text + "\n\n"
                    )  # Write the text to the file, followed by two new lines

                    web_extracted_texts += text + "\n\n"

                    print(f"Saved content of URL {successful_extractions+1}")
                    successful_extractions += 1
                    if successful_extractions >= num_results:
                        break
            start_index += 10  # Increase the start index for the next Google search
    print("Finished processing all URLs")
    return web_extracted_texts


# @tool("search")
async def search_and_summarize_web_url(query:str, chat:str) -> str:

    """Searches the web for the query and extracts relevant texts."""
    
    successful_extractions = 0
    start_index = 1
    # Initialize an empty string to store the entire extracted texts
    web_extracted_summaries = ""

    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query
        })
    headers = {
        'X-API-KEY': '2e30a64d6983e351fa8b845a6977fae01cfb8fa5',
        'Content-Type': 'application/json'
        }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded = json.loads(data.decode("utf-8"))

    num_results = len(decoded['organic'])

    while successful_extractions < len(decoded['organic']):
        # urls = search_google(
        #     query, GOOGLE_API_KEY, GOOGLE_CONTEXT_ID, start_index, num_results
        # )

        for url in decoded['organic']:
            try:
                bprint(f"Processing URL {successful_extractions+1}/{num_results}")
                print("url "+url['link'])
                summary = await get_website_summary(url['link'], topic=query, chat=chat)
                # summary = await asyncio.gather(get_website_summary(url['link'], topic=query, chat=chat))
                print("<--- sum in search")
                print(summary)
                print("<--- sum in search end")
                if summary is not None:
                    # Write the text to the file, followed by two new lines
                    web_extracted_summaries += summary + "\n\n"

                    # gprint(f"Saved content of URL {successful_extractions+1}")
                    print("-" * 134)
                    successful_extractions += 1
                    print(successful_extractions)
                    if successful_extractions >= num_results:
                        break
            except:
                successful_extractions += 1
        # Increase the start index for the next Google search
        start_index += 10
    gprint("Finished processing all URLs")
    return web_extracted_summaries


if __name__ == "__main__":
    query = "Pick a ripe watermelon"
    search_and_extract_web_url(query)