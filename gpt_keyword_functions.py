from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate

from schemas.title_schemas import title_schemas
from schemas.headings_schemas import headings_schemas
from schemas.intro_schemas import intro_schemas
from schemas.section_schemas import section_schemas
from schemas.rewrite_schemas import rewrite_schemas
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import LLMChain, PromptTemplate
from prompts.templates import template_test_2, template_test_3
import string



def blog(keyword, context, chat, chat2, retriever):
    
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
        input_variables=["input","chat_history"], 
        template=template_test_2,
        partial_variables={"format_instructions": format_instructions},
        # output_parser=output_parser

    )
    prompt2 = PromptTemplate(
        input_variables=["input"], 
        template=template_test_3,
        partial_variables={"format_instructions": format_instructions},
        # output_parser=output_parser

    )
    memory = ConversationBufferMemory(memory_key="chat_history", k=2)

    llm = LLMChain(llm=chat, 
        prompt=prompt,
        memory=memory)
    
    llm2 = LLMChain(llm=chat2, 
        prompt=prompt2)




    title = title_schemas(keyword=keyword, chat=chat, retriever=retriever)

    headings = headings_schemas(keyword=keyword, context=context)

    intro = intro_schemas(keyword=keyword,  
                          llm=llm, 
                          format_instructions=format_instructions,
                          chat=chat,
                          retriever=retriever)
    intro = rewrite_schemas(input=intro, llm=llm2)
        

    content = ''
    count = 0
    content += """<p>"""+intro+"""</p>"""

    for heading in headings['headings_list']:
        new_response = section_schemas(heading=heading,
                                       keyword=keyword,
                                       format_instructions=format_instructions,
                                       llm=llm,
                                       chat=chat,
                                       retriever=retriever)
        new_response = rewrite_schemas(input=new_response, llm=llm2)
        if "I apologize" in new_response or "Final response to human" in new_response or len(new_response)<350:
            count += 1
            pass
        else:
            headings_cap = string.capwords(heading)
            print("adding content")
            content += """<h2>"""+headings_cap+"""</h2>"""
            content += """<p>"""+new_response+"""</p>"""
            count += 1
        if count == len(headings['headings_list'])-1 or count==10:
            print("<----start content")
            print(content)
            print("<----start content end")
            end_content = {}
            end_content['content'] = content
            end_content['title'] = title
            return end_content