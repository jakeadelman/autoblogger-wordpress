from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from langchain import LLMChain, PromptTemplate
from prompts import SUMMARIZE_PROMPT


def summarize_text(text: str, topic: str, chat ) -> str:

    PROMPT = PromptTemplate(template=SUMMARIZE_PROMPT, input_variables=["text","topic"])
    summarize_chain = LLMChain(llm=chat, prompt=PROMPT)

    # Truncate text if larger than 12500 words
    if len(text.split()) > 3000:
        print("Truncating text to 3000 words")
        text = " ".join(text.split()[:3000])

    # Summarize the text
    print(len(text.split()))
    try:
        summary = summarize_chain.run(text=text, topic=topic)
    except Exception as e:
        print("exception")
        return None

    return summary

async def get_website_summary(url, topic, chat):
    """
    This function takes a URL as input and returns the summary content of the webpage.

    Parameters:
    url (str): The URL of the webpage.

    Returns:
    str: The summary content of the webpage.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            print(f"Fetching content from {url}")
            await page.goto(url)
            decoded_content = await page.inner_html('body')
        except:
            print("exception")
        await browser.close()
        soup = BeautifulSoup(decoded_content, "html.parser")
        cleaned_text = ""
        for par in soup.find_all('p'):
            cleaned_text += " "+par.get_text()
        # Summarize the text
        summary = summarize_text(text=cleaned_text, topic=topic, chat=chat)
        return summary
