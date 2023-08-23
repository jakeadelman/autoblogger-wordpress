import json
import re
from langchain.chains import RetrievalQA
from functions import find_nth



def section_schemas(heading, keyword, llm, chat, format_instructions, retriever):

        qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever)
        print("<----- closest")
        print(qa.run(heading))
        closest = qa.run(heading)
        print("<----- closest end")



        temp = """
        Remember to have the closing quotation marks and closing curly bracket for the JSON.
        Write 6, 50 word paragraphs for my blog section for my article about "{keyword}".
        Use the context below (real article summaries)
        Keyword: "{heading}"
        
        There should be at least 5 paragraphs.

        Use this context (real article summaries) to create the intro.
        Context: {context}

        Format the output as JSON with the following keys:
        blog_section

        {format_instructions}

        Final Checks:
        Do not say 'Sure!'
        Don't have any headings in the blog section.
        Are any of the paragraphs longer than 80 words? If so, break them up into smaller paragraphs.
        Is the entire thing under 250 words? If so, lengthen it.
        Is there a closing quotation mark for the JSON content? If not, add one.

        
        Make sure to include the opening and closing brackets of the JSON.

        Section:
        """
      
        messages = temp.format(
            format_instructions=format_instructions,
            keyword=keyword,
            heading=heading,
            context=closest
        )

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
                    nth=find_nth(t_res, "'",3)
                    test_res = '{"blog_section": "'+t_res[nth+1:]
                    print("<--test res start")
                    period_index = test_res.rfind(".") + 1
                    res_2 = test_res[:period_index]+'"}'
                except:
                    t_res = t_res.replace('"',"'")
                    nth=find_nth(t_res, "'",3)
                    test_res = '{"blog_section": "'+t_res[nth+1:]
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