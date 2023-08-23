from gpt_keyword_functions import blog
import argparse
import csv
import requests
import base64
from utils.functions import get_category, get_tags
from langchain.chat_models import ChatOpenAI
from os.path import exists
import csv
from utils.img_to_wp import img_to_wp
import string
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings


from datetime import datetime, date
from schemas.tag_schemas import tag_schemas, clean_tags
from schemas.slug_schemas import slug_schemas
from utils.serper_web_utils import search_and_summarize_web_url
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_BASE = os.getenv('OPENROUTER_API_BASE')
OPENROUTER_MODEL_16K = os.getenv('OPENROUTER_MODEL_16K')
OPENROUTER_REFERRER = os.getenv('OPENROUTER_REFERRER')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL')
WP_APPLICATION_USERNAME = os.getenv('WP_APPLICATION_USERNAME')
WP_APPLICATION_PASSWORD = os.getenv('WP_APPLICATION_PASSWORD')

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


user = WP_APPLICATION_USERNAME
password = WP_APPLICATION_PASSWORD
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
finished_file_path = "./csvs/finished/"+keyword+".csv"


if not exists(finished_file_path):
    with open(finished_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ['keyword','url']
        writer.writerow(field)


chat = ChatOpenAI(
    temperature=0.7,
    model=OPENROUTER_MODEL_16K,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base=OPENROUTER_API_BASE,
    headers={"HTTP-Referer": OPENROUTER_REFERRER},
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

            open('./text/text.txt', 'w').close()
            with open('./text/text.txt', 'w') as f:
                f.write(context)

            

            # retrieval q and a
            loader = TextLoader("./text/text.txt")
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            embeddings = OpenAIEmbeddings()
            db = Chroma.from_documents(texts, embeddings)
            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":5})


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


