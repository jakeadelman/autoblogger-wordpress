import logging
import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from shared import constants

from prompts import REWRITE_PROMPT, SUMMARIZE_PROMPT

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
OPENAI_API_KEY = "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"
GOOGLE_API_KEY = "AIzaSyA42ThVNx5QQqUrgJ9JbzcDYwKBDGWvmfg"
# GOOGLE_API_KEY = "AIzaSyA7_qBjRBvn9cyHwI-M5_9ygibvH9w_X0w"
# GOOGLE_API_KEY = "AIzaSyA42ThVNx5QQqUrgJ9JbzcDYwKBDGWvmfg"
GOOGLE_CONTEXT_ID = "b1ad2b402da6c4614"
PINECONE_ENV = "asia-southeast1-gcp-free"


def rprint(text):
    """Prints text in red.

    :param text: the text to print
    """
    print(f"<span style='color:red'>{text}</span>")


def bprint(text):
    """Prints text in blue.

    :param text: the text to print
    """
    print(f"<span style='color:blue'>{text}</span>")


def gprint(text):
    """Prints text in green.

    :param text: the text to print
    """
    print(f"<span style='color:green'>{text}</span>")


def generate_final_blog(entire_draft, TOPIC_PROMPT, OPENAI_API_KEY):
    """
    This function refines the generated blog and saves the final blog in a markdown file.

    Parameters:
    entire_draft (str): The entire draft of the blog.
    TOPIC_PROMPT (str): The topic prompt for the blog.
    OPENAI_API_KEY (str): The OpenAI API key.

    Returns:
    None
    """
    refine_llm = ChatOpenAI(
        model_name="gpt-4-0613",
        temperature=0.5,
        openai_api_key=OPENAI_API_KEY,
    )

    prompt = PromptTemplate.from_template(REWRITE_PROMPT)
    refine_llm_chain = LLMChain(llm=refine_llm, prompt=prompt)

    final_blog = refine_llm_chain(
        inputs={"generated_blog": entire_draft, "TOPIC_PROMPT": TOPIC_PROMPT},
        return_only_outputs=True,
    )

    # Save the blog in a markdown file
    with open("outputs/blog.md", "w") as f:
        f.write(final_blog["text"])

    return final_blog["text"]


def split_outline_prompt(OUTLINE_PROMPT):
    """
    This function splits the OUTLINE_PROMPT into headers and blog sections.

    Parameters:
    OUTLINE_PROMPT (str): The outline prompt for the blog.

    Returns:
    headers (list): The headers of the blog sections.
    blog_sections (list): The blog sections.
    """
    headers = []
    for text in OUTLINE_PROMPT.split("\n"):
        if text.startswith("#"):
            headers.append(text.split("#")[1].strip())
    logging.debug("headers: ", headers)

    blog_sections = OUTLINE_PROMPT.split("\n\n")

    return headers, blog_sections


def combine_drafts(directory):
    """
    This function combines all the markdown generated blogs into one file.

    Parameters:
    directory (str): The directory where the drafts are stored.

    Returns:
    entire_draft (str): The entire draft of the blog.
    """
    # Define the name of the output file
    output_file = directory + "complete_draft.md"

    # Get a list of all draft files
    draft_files = [
        f for f in os.listdir(directory) if f.startswith("draft_") and f.endswith(".md")
    ]

    # Sort the files by their number to maintain the order
    draft_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

    # Initialize an empty string to store the entire draft
    entire_draft = ""

    # Open the output file in write mode
    with open(output_file, "w") as outfile:
        # Iterate over each draft file
        for filename in draft_files:
            # Open the draft file in read mode
            with open(directory + filename, "r") as infile:
                # Read the contents of the draft file
                contents = infile.read()

                # Write the contents of the draft file to the output file
                outfile.write(contents)

                # Add the contents of the draft file to the entire draft string
                entire_draft += contents

                # Add a newline to separate the contents of different draft files
                outfile.write("\n\n")
                entire_draft += "\n\n"

    gprint(f"All drafts have been combined into {output_file}.")
    return entire_draft


def summarize_text(text: str, topic: str, chat ) -> str:

    PROMPT = PromptTemplate(template=SUMMARIZE_PROMPT, input_variables=["text","topic"])
    # llm = ChatOpenAI(
    #     model_name="gpt-3.5-turbo-16k-0613",
    #     # max_tokens=15000,
    #     openai_api_key=OPENAI_API_KEY,
    #     temperature=0,
    # )
    # chat = ChatOpenAI(
    #     temperature=0.7,
    #     # model="meta-llama/llama-2-13b-chat",
    #     model="anthropic/claude-instant-v1",
    #     openai_api_key="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",
    #     openai_api_base="https://openrouter.ai/api/v1",
    #     headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
    # )
    summarize_chain = LLMChain(llm=chat, prompt=PROMPT)

    # Truncate text if larger than 12500 words
    if len(text.split()) > 3000:
        rprint("Truncating text to 3000 words")
        # text = text.split()[:1000]
        text = " ".join(text.split()[:3000])
        # text = text[:15000]
        # print(text)

    # Summarize the text
    # print(text)
    print(len(text.split()))
    try:
        summary = summarize_chain.run(text=text, topic=topic)
        # print(summary)
    except Exception as e:
        print("exception")
        # st.error(e)
        # st.error(f"Number of words: {len(text.split())}")
        return None

    return summary