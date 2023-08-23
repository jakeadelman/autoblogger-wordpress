
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent
import json
from langchain.chat_models import ChatOpenAI
import re
from keyword_prompts import my_prompt, my_prompt_chat
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate
from pydantic import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain import LLMChain, PromptTemplate
from templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from shared import constants

def slug_schemas(keyword, context):
    # chat = ChatOpenAI(
    #     temperature=0,
    #     model_name='gpt-3.5-turbo-16k-0613'
    # )
    chat = ChatOpenAI(
        temperature=0.7,
        # model="meta-llama/llama-2-13b-chat",
        model="openai/gpt-3.5-turbo-16k",
        openai_api_key="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",
        openai_api_base="https://openrouter.ai/api/v1",
        headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
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

    # class Slug(BaseModel):
    #     slug: str = Field(description="this is the 4 to 7 word slug")

    # pydantic_parser = PydanticOutputParser(pydantic_object=Slug)
    # format_instructions = pydantic_parser.get_format_instructions()

    # memory = ConversationBufferWindowMemory(
    #     memory_key='chat_history',
    #     k=3,
    #     return_messages=True
    # )


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

    print("<----slug")
    print(output_dict)
    print("<----slug end")

    try:
        output_dict =json.loads(output_dict)
    except:
        pass

    try:
        output_dict = output_dict['slug']
    except:
        pass

    return output_dict
    # agent = initialize_agent(tools=tools,
    #                         llm=llm,
    #                         agent='structured-chat-zero-shot-react-description',
    #                         verbose=True,
    #                         max_iterations=1,
    #                         memory=memory,
    #                         early_stopping_method="generate",
    #                         output_parser=pydantic_parser,
    #                         handle_parsing_errors="Check your output and make sure it conforms!"
    #                         )

    # # prompt = ChatPromptTemplate.from_template(SLUG_PROMPT)
    # agent.agent.llm_chain.prompt.messages[0].prompt.template = my_prompt
    # # print(agent.agent.llm_chain.prompt.messages[0].prompt.template)
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         SystemMessage(
    #             content=my_prompt
    #         ),
    #         HumanMessagePromptTemplate.from_template(temp),
    #     ]
    # )

    # from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate

    # template = ChatPromptTemplate.from_messages(
    #     [
    #         SystemMessage(
    #             content=my_prompt_chat
    #         ),
    #         HumanMessagePromptTemplate.from_template("{format_messages}"),
    #     ]
    # )

    # agent.agent.llm_chain.prompt.messages[0].prompt.template = prompt.format_messages(format_instructions=format_instructions)
    # _input = prompt.format_messages(topic=keyword, format_instructions=format_instructions)

    # print(_input)
    # # _input = prompt.format_messages(topic=keyword, 
    # #                 format_instructions=format_instructions)

    # output_dict = agent(str(_input))

    # try:
    #     output_dict =json.loads(output_dict)
    # except:
    #     pass

    # try:
    #     output_dict = output_dict['output']
    #     output_dict = json.loads(output_dict)
    #     output_dict = output_dict['action_input']
    #     print(output_dict)
    # except:
    #     pass

    # try:
    #     output_dict= output_dict['slug']
    # except:
    #     pass



    # print("<---slug beg")
    # print(output_dict)
    # print("<---slug end")
    # return output_dict