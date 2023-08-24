import json
import re
from langchain.chains import RetrievalQA
from utils.functions import find_nth, remove_extra_heading, add_json_characters



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



        # print("<---output dict1")
        # print("<----- for "+heading)
        # print(output_dict)
        # print("<---output dict2")

        print(heading+r"\n\n" in output_dict)
        output_dict = remove_extra_heading(output_dict, heading)
        result = re.findall(r'{([^{]*?)}', str(output_dict))

        if len(result)>0:
            print("length of result is "+str(len(result)))
            try:
                t_res = result[0].strip().replace('“',"'")
                t_res = t_res.replace('"',"'")
                nth=find_nth(t_res, "'",3)
                nth_text = t_res[nth+1:]
                res_2 = add_json_characters(nth_text)
            except:
                print("res2 second")
                pass
        else:
            stripped_output = output_dict.replace("{","")
            stripped_output = stripped_output.strip()
            if stripped_output.startswith('"blog_section":'):
                t_res = stripped_output.replace('"',"'")
                nth=find_nth(t_res, "'",3)
                nth_text = t_res[nth+1:]
                res_2 = add_json_characters(nth_text)
            else:
                test_res = '{"blog_section": "'+stripped_output.replace('"',"'")
                period_index = test_res.rfind(".") + 1
                res_2 = test_res[:period_index]+'"}'

        if "I apologize" not in str(res_2):
            print("is not in string")
            try:
                new_response = json.loads(str(res_2), strict=False)
                new_response = new_response['blog_section']
            except:
                new_response = res_2
        else:
            new_response = res_2



        print("<---section start")
        print("section for "+heading)
        print(new_response)
        print("<---section end")
        return new_response