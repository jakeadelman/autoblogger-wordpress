import json
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from prompts.templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


def headings_schemas(keyword, context):
    chat = ChatOpenAI(
        temperature=0,
        model_name='gpt-3.5-turbo-16k-0613'
    )

    temp = """
    Make sure there is opening and closing quotation marks and curly brackets.
    Make sure there is only 1 headings_list.
    Can you come up with 7 to 10 different headings for my article on {keyword}.
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