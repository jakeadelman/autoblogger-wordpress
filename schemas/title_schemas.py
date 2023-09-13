import json
from langchain import LLMChain, PromptTemplate
from prompts.templates import llm_chain_prompt_template
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI


def title_schemas(keyword, retriever):
    chat = ChatOpenAI(
        temperature=0,
        model_name='gpt-3.5-turbo-16k-0613'
    )


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

    # llm = LLMChain(llm=chat, prompt=prompt)
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
