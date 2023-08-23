from langchain.agents import load_tools, Tool
from pydantic import BaseModel, Field, validator
from langchain.agents import initialize_agent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
import json
from functions import paragraphize
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chat_models import ChatOpenAI
from keyword_prompts import my_prompt
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain import LLMChain, PromptTemplate
from templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser



def tag_schemas(context, keyword):
    chat = ChatOpenAI(
        temperature=0.7,
        # model="meta-llama/llama-2-13b-chat",
        model="openai/gpt-3.5-turbo-16k",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
        headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
    )

    temp = """
        Can you give me 3 tags in JSON format using the keys below for this topic: {topic}.


        Strictly follow the following steps:
        1. Search google for {topic}
        2. The tag should be 1 or 2 words long.
        3. Make sure the tags are relevant to the product.

        Format the output as JSON with the following keys:
        tag1
        tag2
        tag3

        Use this context to find the headings:
        {context}
        
        Tags:
        """
    
    tag1 = ResponseSchema(
        name="tag1",
        description="this is first tag"
    )
    tag2 = ResponseSchema(
        name="tag2",
        description="this is second tag"
    )
    tag3 = ResponseSchema(
        name="tag3",
        description="this is third tag"
    )

    tags_schemas = [
        tag1,
        tag2,
        tag3
    ]

    output_parser = StructuredOutputParser.from_response_schemas(tags_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        input_variables=["question"], 
        template=llm_chain_prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    messages = temp.format(
        topic=keyword,
        context=context
    )

    _input = prompt.format(question=messages)

    llm = LLMChain(llm=chat, prompt=prompt, output_parser=output_parser)

    output_dict = llm.run(_input)

    try:
        output_dict =json.loads(output_dict)
    except:
        pass
    print("<----tags")
    print(output_dict)
    print("<----tags end")

    return output_dict



def clean_tags(output_dict):
    output_dict['tag1'] = output_dict['tag1'].lower()
    output_dict['tag2'] = output_dict['tag2'].lower()
    output_dict['tag3'] = output_dict['tag3'].lower()

    output_dict['tag1'] = output_dict['tag1'].replace(" ","")
    output_dict['tag2'] = output_dict['tag2'].replace(" ","")
    output_dict['tag3'] = output_dict['tag3'].replace(" ","")

    output_dict['tag1'] = output_dict['tag1'].replace("-","")
    output_dict['tag2'] = output_dict['tag2'].replace("-","")
    output_dict['tag3'] = output_dict['tag3'].replace("-","")
    return output_dict