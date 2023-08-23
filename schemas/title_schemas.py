from langchain.agents import load_tools, Tool
from pydantic import BaseModel, Field, validator
from langchain.agents import initialize_agent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
import json
from langchain.chat_models import ChatOpenAI
from keyword_prompts import my_prompt, my_zero_shot_prompt
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain import LLMChain, PromptTemplate
from templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import RetrievalQA


def title_schemas(keyword, chat, retriever):

    # chat = ChatOpenAI(
    #     temperature=0.7,
    #     # model="meta-llama/llama-2-13b-chat",
    #     model="openai/gpt-3.5-turbo-16k",
    #     openai_api_key="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",
    #     openai_api_base="https://openrouter.ai/api/v1",
    #     headers={"HTTP-Referer": "https://github.com/alexanderatallah/openrouter-streamlit"},
    # )

    qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever)
    print("<----- closest")
    print(qa.run(keyword))
    closest = qa.run(keyword)
    print("<----- closest end")



    temp = """
    DON'T GIVE ME MULTIPLE TITLES. Include the exact topic in the title. Include exactly: "{topic}"
    Can i get a title for my article about this topic: {topic}
    Only output the title in JSON format. The title should be between 45 and 65 characters long.
    The title should not be about a list.
    
    Format the output as JSON with the following keys:
    title

    {format_instructions}

    Use this context to make up a title:
    {context}

    Title:
    """

    title = ResponseSchema(
        name="title",
        description="this is the title"
    )

    title_schemas = [
        title
    ]

    output_parser = StructuredOutputParser.from_response_schemas(title_schemas)
    format_instructions = output_parser.get_format_instructions()


    prompt = PromptTemplate(
        input_variables=["question"], 
        template=llm_chain_prompt_template,
        partial_variables={"format_instructions": format_instructions}
    )

    messages = temp.format(
        topic=keyword,
        format_instructions=format_instructions,
        context=closest
    )

    _input = prompt.format(question=messages)

    llm = LLMChain(llm=chat, prompt=prompt, output_parser=output_parser)

    output_dict = llm.run(_input)

    print("<----title")
    print(output_dict)
    print("<----title end")

    try:
        output_dict =json.loads(output_dict)
    except:
        pass

    try:
        output_dict = output_dict['title']
    except:
        pass

    return output_dict

    # agent = initialize_agent(tools,
    #                         llm,
    #                         agent='zero-shot-react-description',
    #                         # agent='structured-chat-zero-shot-react-description',
    #                         verbose=True,
    #                         max_iterations=3,
    #                         memory=memory,
    #                         early_stopping_method="generate",
    #                         output_parser=pydantic_parser,
    #                         handle_parsing_errors="Check your output and make sure it conforms!"
    #                         )

    # temp = """
    # DON'T GIVE ME MULTIPLE TITLES. Include the exact topic in the title.
    # Can you give me a title based on the search data you find. 
    # Make sure to include the the exact topic in the title. Only output the one title. 
    # If you have multiple title options, output the first one.
    # Topic: {topic}
    # Search google only once for: {topic}
    
    # Format the output as JSON with the following keys:
    # title

    # Following these format instructions: {format_instructions}

    # Title:
    # """
    # agent.agent.llm_chain.prompt.messages[0].prompt.template = my_zero_shot_prompt


    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         SystemMessage(
    #             content=my_prompt
    #         ),
    #         HumanMessagePromptTemplate.from_template(temp),
    #     ]
    # )

    # ques = """
    #     {keyword}
    # """
    # question_new = ques.format(keyword=keyword)
    # agent.agent.llm_chain.prompt.template = my_zero_shot_prompt


    # _input = temp.format(topic=keyword, 
    #                 format_instructions=format_instructions)

    # output_dict= agent(str(_input))
    # try:
    #     output_dict =json.loads(output_dict)
    # except:
    #     pass

    # print(output_dict.keys())
    # try:
    #     output_dict = output_dict['output']
    #     output_dict = json.loads(output_dict)
    #     output_dict = output_dict['action_input']
    #     print(output_dict)
    # except:
    #     pass

    # try:
    #     output_dict= output_dict['title']
    # except:
    #     pass

    # print("<----title")
    # print(output_dict)
    # print("<----title end")
    # return output_dict