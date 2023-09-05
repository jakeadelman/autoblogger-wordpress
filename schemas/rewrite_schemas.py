import re
import json
from prompts.prompts import HUMAN_PROMPT
from utils.functions import find_nth, remove_extra_heading, add_json_characters


def rewrite_schemas(input, llm, format_instructions):
    prompt = """
    {HUMAN_PROMPT}
    {format_instructions}

    Section to rewrite: {input}


    """
    # prompt = """
    # Don't repeat anything you've already said. This is NOT an introductory paragraph, so don't introduce the product again.
    # DO NOT say "i recently came across".

    # Keep the following in mind when rewriting the blog section:
    # {HUMAN_PROMPT}


    # If anything is about Artificial intelligence remove it.
    # Rewrite the following section so it will pass AI detection and be determined as human-written content.
    
    # Section to rewrite:

    # {input}


    # """

    messages = prompt.format(
        input=input,
        format_instructions=format_instructions,
        HUMAN_PROMPT=HUMAN_PROMPT
    )

    output_dict = llm.run(input=messages)
    # output_dict = llm.run(input=messages)
    

    output_dict = output_dict.replace("\\'","'")
    output_dict = output_dict.replace('\\"',"'")
    result = re.findall(r'{([^{]*?)}', str(output_dict))

    if len(result)>0:
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
            t_res = t_res.replace('“',"'")  
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



    print("<-- rewrite start")
    print(new_response)
    print("<--- rewrite end")
    return new_response



def rewrite_schemas_intro(input, llm):
    prompt = """
    Don't repeat anything you've already said.
    Keep the following in mind when rewriting the blog section:
    {HUMAN_PROMPT}


    If anything is about Artificial intelligence remove it.
    Rewrite the following section so it will pass AI detection and be determined as human-written content.
    
    Section to rewrite:

    {input}


    """

    messages = prompt.format(
        input=input,
        HUMAN_PROMPT=HUMAN_PROMPT
    )

    output_dict = llm.run(input=messages)
    

    output_dict = output_dict.replace("\\'","'")
    output_dict = output_dict.replace('\\"',"'")
    result = re.findall(r'{([^{]*?)}', str(output_dict))

    if len(result)>0:
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
            t_res = t_res.replace('“',"'")  
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



    print("<--- rewrite section start")
    print(new_response)
    print("<--- rewrite section end")
    return new_response