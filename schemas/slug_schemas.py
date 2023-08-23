
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import json
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain import LLMChain, PromptTemplate
from templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import os
from dotenv import load_dotenv


load_dotenv()

OPENROUTER_MODEL_16K = os.getenv('OPENROUTER_MODEL_16K')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_API_BASE = os.getenv('OPENROUTER_API_BASE')
OPENROUTER_REFERRER = os.getenv('OPENROUTER_REFERRER')


def slug_schemas(keyword, context):
    chat = ChatOpenAI(
        temperature=0.7,
        model=OPENROUTER_MODEL_16K,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=OPENROUTER_API_BASE,
        headers={"HTTP-Referer": OPENROUTER_REFERRER},
    )

    temp = """
    Can you give me a 4-7 word-long slug delineated with hyphens for my article on {topic}.

    Strictly follow the following steps:
    1. Make sure it is 4 to 7 words long.
    2. Make sure all words are lowercase.
    3. Never search the same thing on google twice.

    {format_instructions}

    Use this context to make up the slug:
    {context}

    Slug:
    """

    slug = ResponseSchema(
        name="slug",
        description="this is the slug"
    )

    slug_schemas = [
        slug
    ]

    output_parser = StructuredOutputParser.from_response_schemas(slug_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        input_variables=["question"], 
        template=llm_chain_prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    messages = temp.format(
        topic=keyword,
        format_instructions=format_instructions,
        context=context
    )

    _input = prompt.format(question=messages)

    llm = LLMChain(llm=chat, prompt=prompt, output_parser=output_parser)

    output_dict = llm.run(_input)

    # print("<----slug")
    # print(output_dict)
    # print("<----slug end")

    try:
        output_dict =json.loads(output_dict)
    except:
        pass

    try:
        output_dict = output_dict['slug']
    except:
        pass

    return output_dict