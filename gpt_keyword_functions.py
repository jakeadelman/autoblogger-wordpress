from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate

from schemas.title_schemas import title_schemas
from schemas.headings_schemas import headings_schemas
from schemas.intro_schemas import intro_schemas
from schemas.section_schemas import section_schemas
from schemas.rewrite_schemas import rewrite_schemas, rewrite_schemas_intro
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import LLMChain, PromptTemplate
from prompts.templates import template_test_7
from selenium import webdriver
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from utils.gpt_selenium import openai_login, rephrase_gpt_4
from utils.prompts import humanize_prompt, humanize_prompt_intro
import json
import string
import time
from utils.paraphraser import main
from utils.functions import paragraphize2
from bs4 import BeautifulSoup as bs
import os
from dotenv import load_dotenv

load_dotenv()

GPT_USERNAME = os.getenv('GPT_USERNAME')
GPT_PASSWORD = os.getenv('GPT_PASSWORD')


def blog(keyword, context, retriever, keyword_table):
    
    blog_section = ResponseSchema(
        name="blog_section",
        description="the blog section"
    )

    section_schemas_json = [
        blog_section
    ]

    output_parser = StructuredOutputParser.from_response_schemas(section_schemas_json)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        input_variables=["input"], 
        template=template_test_7,
        partial_variables={"format_instructions": format_instructions},
        # output_parser=output_parser

    )

    # memory = ConversationBufferMemory(memory_key="chat_history", k=4)

    # llm = LLMChain(llm=chat, 
    #     prompt=prompt,
    #     memory=memory)
    




    title = title_schemas(keyword=keyword, retriever=retriever)

    headings = headings_schemas(keyword=keyword, context=context)

    full_sections_list = []
    intro_dict = {}
    intro = intro_schemas(keyword=keyword,  
                          format_instructions=format_instructions,
                          retriever=retriever,
                          prompt=prompt)
    intro_dict['heading']="intro"
    intro_dict['content']=intro

    full_sections_list.append(intro_dict)



    hp = humanize_prompt.format(table=keyword_table)
    hp = hp.replace("\n","")
    hpi = humanize_prompt_intro.format(table=keyword_table)
    hpi = hpi.replace("\n","")
        

    content = ''
    count = 0
    # content += """<p>"""+intro+"""</p>"""

    for heading in headings['headings_list']:
        headings_cap = string.capwords(heading)
        section_dict = {}
        new_response = section_schemas(heading=heading,
                                       keyword=keyword,
                                       format_instructions=format_instructions,
                                       retriever=retriever,
                                       prompt=prompt)

        section_dict['heading']=headings_cap
        section_dict['content']=new_response

        print("<---- full sections cotent")
        print(section_dict['content'])
        print("<---- full sections cotent")


        if "I apologize" in new_response or "Final response to human" in new_response or len(new_response)<350:
            print("<---- excepting because not long enough")
            print("<---- excepting because not long enough")
            print("<---- excepting because not long enough")
            count += 1
            time.sleep(10)
            pass
        else:
            full_sections_list.append(section_dict)
            count += 1
            time.sleep(10)

        if count == len(headings['headings_list'])-1 or count==20:

            op = uc.ChromeOptions()
            op.add_argument(f"user-agent={UserAgent.random}")
            op.add_argument("user-data-dir=./")
            op.add_experimental_option("detach", True)
            op.add_experimental_option("excludeSwitches", ["enable-logging"])
            op.add_argument('ignore-certificate-errors')
            driver = uc.Chrome(chrome_options=op)

            sec_num=0




            print("<---- full sections list")
            print(full_sections_list)
            print("<---- full sections list")
            full_sections_count = 0
            for sec in full_sections_list:
                full_sections_count+=1
                

                all_tags = []
                soup = bs(sec['content'], "html.parser")
                for tag in soup.find_all():
                    if tag.name=='h3':
                        my_tag = {}
                        my_tag['type'] = 'h3'
                        my_tag['content'] = tag.text.strip()
                        all_tags.append(my_tag)
                    else:
                        my_tag = {}
                        my_tag['type']='p'
                        my_tag['content']=tag.text.strip()
                        all_tags.append(my_tag)

                my_prompt = ''
                if sec['heading']=='intro':
                    openai_login(driver, GPT_USERNAME, GPT_PASSWORD)
                    my_prompt = hpi
                    pass
                else:
                    my_prompt = hp
                    content+="""<h2>"""+sec['heading']+"""</h2>"""

                short_content = ''

                for l in range(len(all_tags)):
                    print("<----all tags")
                    print(all_tags[l])
                    print("<----all tags")
                    if all_tags[0]['type']=='h3' and l==0:

                        # cont = main(3,5,all_tags[l+1]['content'])
                        cont = all_tags[l+1]['content']
                        cont =cont.replace("\n","")
                        short_content="""<p>"""+cont+"""</p>"""
                        # short_content+= """<p>"""+cont+"""</p>"""
                        l+=2
                    elif all_tags[l]['type']=='h3'and l>0:
                        if 'Conclusion' in all_tags[l]['content'] or 'conclusion' in all_tags[l]['content']:
                            pass
                        else:
                            short_content+="""<h3>"""+all_tags[l]['content']+"""</h3>"""
                        l+=1
                    else:

                        # cont = main(3,5,all_tags[l]['content'])
                        cont = all_tags[l]['content']
                        cont =cont.replace("\n","")
                        # cont =cont.replace("\n\n","</p><p>")
                        print("<----- paraphrased content")
                        print(cont)
                        print("<----- paraphrased content")
                        print("<--- l is "+str(l))
                        print(cont)
                        print("<--- l is "+str(l))
                        if len(cont)>50:
                            print("<<---- in p all tags")
                            print(all_tags[l]['content'])
                            print("<<---- in p all tags")
                            short_content+= """<p>"""+cont+"""</p>"""
                            l+=1
                        else:
                            l+=1
                print("<- befor all tags")
                print(all_tags)
                print("<------ short content")
                print(short_content)
                print("<------ short content end")
                if len(short_content)>50:
                    short_content = short_content.replace("\n", "")

                    res_gpt_reworded_content = rephrase_gpt_4(driver, my_prompt,short_content, sec_num)
                    print("<----- gpt reworded start")
                    print(res_gpt_reworded_content)
                    print("<----- gpt reworded end")
                    content+= res_gpt_reworded_content
                    sec_num+=1
                else:
                    short_content+=""

        # if full_sections_count == len(full_sections_list)-1:     
            print("<----start content")
            print(content)
            print("<----start content end")
            end_content = {}
            end_content['content'] = content
            end_content['title'] = title
            driver.close()
            return end_content

                    