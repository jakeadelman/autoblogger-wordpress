from dotenv import load_dotenv
import http.client
import json
from utils.serper_utils import get_website_summary
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI


load_dotenv()

SERPER_API_KEY = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


async def search_and_summarize_web_url(query:str, chat:str) -> str:
    chat = ChatOpenAI(
        temperature=0,
        model_name='gpt-3.5-turbo-16k-0613'
    )

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
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
        }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded = json.loads(data.decode("utf-8"))

    num_results = len(decoded['organic'])

    while successful_extractions < len(decoded['organic']):


        for url in decoded['organic']:
            try:
                print(f"Processing URL {successful_extractions+1}/{num_results}")
                # print("url "+url['link'])
                summary = await get_website_summary(url['link'], topic=query, chat=chat)
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
    print("Finished processing all URLs")
    return web_extracted_summaries
