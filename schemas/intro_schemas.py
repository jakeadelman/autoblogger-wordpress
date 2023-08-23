import json
import re
from langchain.chains import RetrievalQA
from functions import find_nth

def intro_schemas(keyword, llm, format_instructions, chat, retriever):
    qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever)
    print("<----- closest")
    print(qa.run(keyword))
    closest = qa.run(keyword)
    print("<----- closest end")



    temp = """
    Don't add any titles or forword before the introduction.
    Expand on this keyword in 4, 50 word paragraphs for my introduction for my article about "{keyword}".
    Use the context below which is based on real article summaries.
    There should be at least 3 paragraphs. It should be under 300 words.

    Use this context (real article summaries) to create the intro.
    Context: {context}

    Format the output as JSON with the following keys:
    blog_section

    {format_instructions}

    Final Checks:
    Is the entire thing more than 300 words long? If so, shorten it.
    Are any of the paragraphs longer than 50 words? If so, break them up into smaller paragraphs.
    Is there a closing quotation mark for the JSON content? If not, add one.


    Make sure to include the closing curly brackets of the JSON.

    Section:
    """


    messages = temp.format(
        keyword=keyword,
        format_instructions=format_instructions,
        context=closest
    )


    output_dict = llm.run(input=messages)
    print("output intro")
    print(output_dict)
    print("output intro end")
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
                new_response = json.loads(str(res_2), strict=False)
                new_response = new_response['blog_section']
            except:
                if res_2[-2] != '"':
                    new_response = res_2[:-2]+'"'+"}"
                    new_response = json.loads(str(new_response), strict=False)
                    new_response = new_response['blog_section']
        else:
            new_response = res_2
    else:
        new_response = output_dict




    print("<--new res start")
    print(new_response)
    print("<---new res end")
    return new_response
