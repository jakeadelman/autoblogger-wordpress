from gpt_keyword_functions import blog
import argparse
import csv
import requests
import base64
from functions import get_category
from langchain.agents import load_tools, Tool
# from utils.web_utils import search_and_summarize_web_url
from langchain.chat_models import ChatOpenAI
from functions import get_tags
from os.path import exists
import csv
# from utils.web_utils import search_and_summarize_web_url
from img_to_wp import img_to_wp
import string
import json
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings


from datetime import datetime, date
from schemas.tag_schemas import tag_schemas, clean_tags
from schemas.slug_schemas import slug_schemas
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from shared import constants
from langchain.prompts import PromptTemplate
from templates import llm_chain_prompt_template, template_test_2
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationBufferMemory,ConversationSummaryBufferMemory
from langchain import LLMChain
from utils.serper_web_utils import search_and_summarize_web_url
import asyncio
from test_chroma import text
import os

os.environ["OPENAI_API_KEY"] = "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"



user = "wpauserd5S2jmuq"
password = "H1DA pOGr 566a C55Y eolg FDpM"
credentials = user + ':' + password
token = base64.b64encode(credentials.encode())
header = {'Authorization': 'Basic ' + token.decode('utf-8')}

parser = argparse.ArgumentParser(
    description="Get keyword and category"
)

parser.add_argument("-k","--keyword", help="This is the keyword.", type=str, required=True)
parser.add_argument("-c","--category", help="This is the category.", type=str, required=True)
args = parser.parse_args()
keyword = args.keyword
category = args.category

filepath = "./csvs/"+keyword+".csv"
print(filepath)
finished_file_path = "./csvs/finished/"+keyword+".csv"


# tools = [
#         Tool(
#             name = "Intermediate Answer",
#             func=search_and_summarize_web_url,
#             description="google search"
#         )
#     ]

tools = [
        Tool(
            name = "Search Google",
            func=search_and_summarize_web_url,
            description="useful for getting up to date information"
        )
    ]

if not exists(finished_file_path):
    with open(finished_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ['keyword','url']
        writer.writerow(field)

# chat = ChatOpenAI(
#     temperature=0.7,
#     model_name="gpt-3.5-turbo-16k",
#     # model="anthropic/claude-instant-v1",
#     # model="meta-llama/llama-2-13b-chat",
#     openai_api_key="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",
#     # openai_api_base="https://openrouter.ai/api/v1",
#     # headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
# )
chat = ChatOpenAI(
    temperature=0.7,
    # model="meta-llama/llama-2-13b-chat",
    model="openai/gpt-3.5-turbo-16k",
    openai_api_key="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",
    openai_api_base="https://openrouter.ai/api/v1",
    headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
)


with open(filepath, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # csv_reader = csv_file.read()
    line_count = 0
    for row in csv_reader:
        # print(row.keys())
        if_exists = False
        specific_keyword = row["Keyword"]
        with open(finished_file_path, mode='r') as finished_file:
            finished_reader = csv.DictReader(finished_file)
            for finished_row in finished_reader:
                if finished_row['keyword']==specific_keyword:
                    if_exists=True
        
        if if_exists == False:


            context = asyncio.run(search_and_summarize_web_url(specific_keyword,chat))
            # print(context)
            open('text.txt', 'w').close()
            with open('text.txt', 'w') as f:
                f.write(context)

            

            # retrieval q and a
            loader = TextLoader("./text.txt")
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            embeddings = OpenAIEmbeddings()
            db = Chroma.from_documents(texts, embeddings)
            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":5})


            # context = search_and_summarize_web_url(specific_keyword)
            # print("<--- context start")
            # print(context)
            # print("<--- context end")
            print("<----specific keyword")
            print(specific_keyword)
            print("<----specific keyword end")
            slug = slug_schemas(context=context, keyword=specific_keyword)
            print("<--- slug")
            print(slug)
            print("<--- slug end")
            json_tags = tag_schemas(context=context, keyword=specific_keyword)
            print(json_tags)

            img_id = 0
            img_id = img_to_wp(query=json_tags['tag1'], keyword=specific_keyword)
            if img_id == False:
                img_id = img_to_wp(query=json_tags['tag2'], keyword=specific_keyword)
                if img_id == False:
                    img_id = img_to_wp(query=json_tags['tag3'], keyword=specific_keyword)
                    if img_id == False:
                        img_id = img_to_wp(query=specific_keyword, keyword=specific_keyword)
                    else:
                        pass
                else:
                    pass
            else:
                pass


            cleand_json_tags_1 = clean_tags(json_tags)
            # print(json_tags)
            tags_list = []
            tags_list.append(cleand_json_tags_1['tag1'])   
            tags_list.append(cleand_json_tags_1['tag2'])   
            tags_list.append(cleand_json_tags_1['tag3'])   
            new_tags = get_tags(tags_list, header)
            content = blog(keyword=specific_keyword, context=context, chat=chat, retriever=retriever)
            title = content['title']
            blog_content = content['content']

            today_date = datetime.today().strftime('%Y-%m-%dT%X')
            today_date = str(today_date)

            category_id = get_category(category,header=header)

            new_keyword = specific_keyword.replace(" ", "-")
            print(json_tags)
            # print(title)
            

            title_capwords = string.capwords(title)

            post = {
                'slug' : slug,
                'title' : title_capwords,
                'status'   : 'publish', 
                'content'  : blog_content,
                'categories': category_id,
                'tags': new_tags,
                'date'  : today_date,
                'featured_media':img_id,
                'meta_box':{
                    'bk_post_layout_standard':'single-2'
                }
            }
            url = "https://mindfuelwave.com/wp-json/wp/v2/posts"

            response = requests.post(url , headers=header, json=post)
            response_json = response.json()
            if response.status_code == 201:
                with open(finished_file_path, 'a') as f:
                    my_slug = "https://mindfuelwave.com/"+response_json['slug']
                    field_names = ['keyword','url']     
                    my_writer = csv.writer(f)
                    my_writer.writerow([specific_keyword,my_slug])
                    f.close()
                    print("file added to finished posts csv")


