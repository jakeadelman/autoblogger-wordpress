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
from pprint import pprint

from datetime import datetime, date
from schemas.tag_schemas import tag_schemas, clean_tags
from schemas.slug_schemas import slug_schemas
from utils.serper_web_utils import search_and_summarize_web_url
import asyncio
import os
from utils.get_lsi_keywords import get_lsi_keywords

from random import *
from dotenv import load_dotenv

load_dotenv()

WP_APPLICATION_USERNAME = os.getenv('WP_APPLICATION_USERNAME')
WP_POSTS = os.getenv('WP_POSTS')
WP_BASE = os.getenv('WP_BASE')
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
    temperature=0,
    model_name='gpt-3.5-turbo-16k-0613'
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

            keyword_table = get_lsi_keywords(query=specific_keyword)
            print("<---- lsi")
            print(keyword_table)
            print("<---- lsi")

            context = asyncio.run(search_and_summarize_web_url(specific_keyword,chat))

            rando = randint(1,100000)
            rand_name = "text-"+str(rando)
            rand_path = './text/'+rand_name+'.txt'
            open(rand_path, 'w').close()
            with open(rand_path, 'w') as f:
                f.write(context)

            

            # retrieval q and a
            loader = TextLoader(rand_path)
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)
            embeddings = OpenAIEmbeddings()
            db = Chroma.from_documents(texts, embeddings)
            retriever = db.as_retriever(search_type="mmr", search_kwargs={"k":20})


            print("<----specific keyword")
            print(specific_keyword)
            print("<----specific keyword end")
            
            slug = slug_schemas(context=context, keyword=specific_keyword)
            print("<--- slug")
            print(slug)
            print("<--- slug end")

            json_tags = tag_schemas(context=context, keyword=specific_keyword)
            print("<--- json tags")
            print(json_tags)
            print("<--- json tags")

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
            print("<---- starting content")
            content = blog(keyword=specific_keyword, context=context, retriever=retriever, keyword_table=keyword_table)
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
                'status'   : 'draft', 
                'content'  : blog_content,
                'categories': category_id,
                'tags': new_tags,
                'date'  : today_date,
                'featured_media':img_id,
                # 'meta_box':{
                #     'bk_post_layout_standard':'single-2'
                # }
            }
            url = WP_POSTS
            pprint(post)
            response = requests.post(url , headers=header, json=post)
            response_json = response.json()
            pprint("<------ res json")
            pprint(response.json())
            print(response.status_code)
            pprint("<------ res json")
            if response.status_code == 201:
                with open(finished_file_path, 'a') as f:
                    my_slug = WP_BASE +response_json['slug']
                    field_names = ['keyword','url']     
                    my_writer = csv.writer(f)
                    my_writer.writerow([specific_keyword,my_slug])
                    f.close()
                    os.remove(rand_path)
                    print("file added to finished posts csv")


