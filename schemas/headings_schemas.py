from langchain.agents import load_tools, Tool
from pydantic import BaseModel, Field, validator
from langchain.agents import initialize_agent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
import json
from typing import List
import re
from langchain.chat_models import ChatOpenAI
from keyword_prompts import my_prompt, my_zero_shot_prompt
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain import LLMChain, PromptTemplate
from templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser



def headings_schemas(keyword, context):
    chat = ChatOpenAI(
        temperature=0.7,
        model="openai/gpt-3.5-turbo-16k",
        # model="meta-llama/llama-2-13b-chat",
        # model="anthropic/claude-instant-v1",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
        headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
    )

    temp = """
    Make sure there is opening and closing quotation marks and curly brackets.
    Make sure there is only 1 headings_list.
    Can you come up with 11 to 17 different headings for my article on {keyword}.
    DO NOT give the output as a numbered list. Make sure it is in JSON format.
    Make sure they are on the topic of {keyword}

    Format the output as JSON with the following keys:
    headings_list

    {format_instructions}

    Final Checks:
    Are there more than 10 headings? If not, add more based on the context below.
    Make sure there is opening and closing quotation marks and curly brackets.

    Use this context to find the headings:
    {context}

    
    Headings:
    """

    headings_list = ResponseSchema(
        name="headings_list",
        description="this is the python list of headings"
    )

    headings_schemas = [
        headings_list
    ]

    output_parser = StructuredOutputParser.from_response_schemas(headings_schemas)
    format_instructions = output_parser.get_format_instructions()
    # class HeadingsList(BaseModel):
    #     headings_list: List[str] = Field(description="python list of the 10 headings")

    # pydantic_parser = PydanticOutputParser(pydantic_object=HeadingsList)
    # format_instructions = pydantic_parser.get_format_instructions()

    prompt = PromptTemplate(
        input_variables=["question"], 
        template=llm_chain_prompt_template,
        partial_variables={"format_instructions": format_instructions},
        output_parser=output_parser
    )

    messages = temp.format(
        keyword=keyword,
        format_instructions=format_instructions,
        context=context
    )

    _input = prompt.format(question=messages)

    llm = LLMChain(llm=chat, prompt=prompt)

    output_dict = llm.run(_input)


    try:
        output_dict=output_dict.replace("```json","")
        output_dict=output_dict.replace("```","")
    except:
        pass

    try:
        output_dict =json.loads(output_dict)
    except:
        pass


    print("<----headings")
    print(output_dict)
    print("<----headings end")


    return output_dict