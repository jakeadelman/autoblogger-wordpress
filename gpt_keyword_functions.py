import os
from langchain.agents import load_tools, Tool
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
# from utils.web_utils import search_and_summarize_web_url
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser
from typing import List
import json
import re

from schemas.title_schemas import title_schemas
from schemas.headings_schemas import headings_schemas
from schemas.intro_schemas import intro_schemas
from schemas.section_schemas import section_schemas
# from schemas.reword_schemas import reword_schemas
from langchain.utilities import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field, validator
from keyword_prompts import my_prompt, conversational_react_description_prompt, my_zero_shot_prompt
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationBufferMemory,ConversationSummaryBufferMemory
from templates import llm_chain_prompt_template, llm_chain_prompt_template_section, template_test
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from langchain.schema import SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.prompts import MessagesPlaceholder
from templates import llm_chain_prompt_template, template_test_2
from shared import constants
import requests
from functions import restImgUL
from img_to_wp import img_to_wp
import string
import openai

# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["SERPER_API_KEY"] = "2e30a64d6983e351fa8b845a6977fae01cfb8fa5"





# keyword = "largest sea animals"


def blog(keyword, context, chat, retriever):
    # openai.api_base = "https://openrouter.ai/api/v1"
    # openai.api_key = "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"

    # chat = ChatOpenAI(
    #     temperature=0,
    #     model_name="anthropic/claude-instant-v1",
    #     headers={"HTTP-Referer": constants.OPENROUTER_REFERRER},
    # )

    
    blog_section = ResponseSchema(
        name="blog_section",
        description="the 5 paragraph blog section"
    )

    section_schemas_json = [
        blog_section
    ]

    output_parser = StructuredOutputParser.from_response_schemas(section_schemas_json)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        # input_variables=["question"], 
        input_variables=["input","chat_history"], 
        template=template_test_2,
        partial_variables={"format_instructions": format_instructions},
        output_parser=output_parser

    )
    memory = ConversationBufferMemory(memory_key="chat_history", k=2)

    llm = LLMChain(llm=chat, 
        prompt=prompt,
        memory=memory)




    title = title_schemas(keyword=keyword, chat=chat, retriever=retriever)

    headings = headings_schemas(keyword=keyword, context=context)

    intro = intro_schemas(keyword=keyword,  
                          llm=llm, 
                          format_instructions=format_instructions,
                          chat=chat,
                          retriever=retriever)
        

    content = ''
    count = 0
    content += """<p>"""+intro+"""</p>"""

    for heading in headings['headings_list']:
        new_response = section_schemas(heading=heading,
                                       keyword=keyword,
                                       context=context,
                                       format_instructions=format_instructions,
                                       llm=llm,
                                       chat=chat,
                                       retriever=retriever)
        if "I apologize" in new_response or "Final response to human" in new_response or len(new_response)<120:
            count += 1
            pass
        else:
            headings_cap = string.capwords(heading)
            print("adding content")
            # new_response = reword_schemas(tools=tools, heading=heading, new_response=new_response)
            content += """<h2>"""+headings_cap+"""</h2>"""
            content += """<p>"""+new_response+"""</p>"""
            count += 1
        if count == len(headings['headings_list'])-1 or count==8:
            print("<----start content")
            print(content)
            print("<----start content end")
            end_content = {}
            end_content['content'] = content
            end_content['title'] = title
            return end_content