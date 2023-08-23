from langchain.agents import load_tools, Tool
from pydantic import BaseModel, Field, validator
from langchain.agents import initialize_agent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
import json
from langchain.chat_models import ChatOpenAI
# from functions import paragraphize
from keyword_prompts import my_prompt, conversational_react_description_prompt, my_zero_shot_prompt
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import PromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from templates import llm_chain_prompt_template, template_test_2
from langchain import LLMChain, PromptTemplate
from shared import constants
import re
from langchain.output_parsers import RetryWithErrorOutputParser
from langchain.chains import RetrievalQA



def section_schemas(context, heading, keyword, llm, chat, format_instructions, retriever):
        # closest = db.similarity_search(heading)
        # print("<----- closest")
        # print(closest[0].page_content)
       
        qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever)
        print("<----- closest")
        print(qa.run(heading))
        closest = qa.run(heading)
        print("<----- closest end")



        temp = """
        Write 6, 50 word paragraphs for my blog section for my article about "{keyword}".
        Use the context below (real article summaries)
        Keyword: "{heading}"
        
        Separate each paragraph with "\\n\n".
        There should be at least 5 paragraphs.

        Use this context (real article summaries) to create the intro.
        Context: {context}

        Format the output as JSON with the following keys:
        blog_section

        {format_instructions}

        Final Checks:
        Are any of the paragraphs longer than 80 words? If so, break them up into smaller paragraphs.
        Is the entire thing under 250 words? If so, lengthen it.
        Are any of the paragraphs not separated with "\\n\n"? If so, add "\\n\n".
        Is there a closing quotation mark for the JSON content? If not, add one.

        
        Make sure to include the opening and closing brackets of the JSON.

        Section:
        """
      
        messages = temp.format(
            format_instructions=format_instructions,
            # larger_keyword=keyword,
            keyword=keyword,
            heading=heading,
            context=closest
        )
        # temp = """
        # Answer in english. Response should be around 350 words long.
        # You are an expert blog writer. You should not make up any facts. Everything you write about should be in the context below.
        # Nothing is fictional. The context is based on real articles.
        # Write 6, 50 word paragraphs of my section about "{heading}" using the context below.

        # Context: {context}
        # """
        # messages = temp.format(
        #     heading=heading,
        #     context=context
        # )
        output_dict = llm.run(input=messages)



        print("<---output dict1")
        print("<----- for "+heading)
        print(output_dict)
        print("<---output dict2")

        result = re.findall(r'{([^{]*?)}', str(output_dict))

        if len(result)>0:
            try:
                try:
                    t_res = result[0].replace('“',"'")
                    t_res = t_res.replace('"',"'")
                    test_res = '{"blog_section": "'+t_res[19:]
                    print("<--test res start")
                    period_index = test_res.rfind(".") + 1
                    res_2 = test_res[:period_index]+'"}'
                except:
                    t_res = t_res.replace('"',"'")
                    test_res = '{"blog_section": "'+t_res[19:]
                    print("<--test res start")
                    period_index = test_res.rfind(".") + 1
                    res_2 = test_res[:period_index]+'"}'
            except:
                res_2 = output_dict
                print("res2 second")


            if "I apologize" not in str(res_2):
                print("is not in string")
                try:
                    print("<--- json loads start")
                    # newe = str(res_2).replace("\n","")
                    print(type(res_2))
                    print(res_2)
                    new_response = json.loads(str(res_2), strict=False)
                    print("<--- json loads middle")
                    new_response = new_response['blog_section']
                    print("<--- json loads end")
                except:
                    new_response = res_2
                    # new_response = res_2
                    # try:
                    #     if res_2[-2] != '"':
                    #         new_response = res_2[:-2]+'"'+"}"
                    #         new_response = json.loads(str(new_response), strict=False)
                    #         new_response = new_response['blog_section']
                    #     else:
                    #         pass
                    # except:
                    #     new_response = res_2
            else:
                new_response = res_2
        else:
            new_response = output_dict



        if new_response.startswith(heading+": ") or new_response.startswith(heading.title()+": "):
            heading_len = len(heading)+1
            new_response = new_response[heading_len:]
        
        if new_response.startswith(heading+" ") or new_response.startswith(heading.title()+" "):
            heading_len = len(heading)+1
            new_response = new_response[heading_len:]

        if new_response.startswith(heading+"\n") or new_response.startswith(heading.title()+" "):
            heading_len = len(heading)+2
            new_response = new_response[heading_len:]

        print("<---section start")
        print("section for "+heading)
        print(new_response)
        print("<---section end")
        return new_response