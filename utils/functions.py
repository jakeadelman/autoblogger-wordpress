
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

WP_MEDIA = os.getenv('WP_MEDIA')
WP_APPLICATION_USERNAME = os.getenv('WP_APPLICATION_USERNAME')
WP_APPLICATION_PASSWORD = os.getenv('WP_APPLICATION_PASSWORD')
WP_CATEGORIES = os.getenv('WP_CATEGORIES')
WP_TAGS = os.getenv('WP_TAGS')

# def paragraphize(verdict):
#     out = []
#     threshold = 350
#     for chunk in verdict.split('. '):
#         if out and len(chunk)+len(out[-1]) < threshold:
#             out[-1] += ' '+chunk+'. '
#         else:
#             out.append(chunk+'. ')
#     new_verdict =''
#     for i in range(0,len(out)):
#         new_string = out[i]+"\n\n"
#         new_verdict+=new_string
#         if i == len(out)-1:
#             new_verdict = new_verdict[:-1]
#             return new_verdict

def add_space(finder,description):
    try:
        desc_period_index = re.finditer(finder,description)
        num = re.findall(finder, description)
        num = len(num)
        print("<------ok")
       
        new_desc = ""
        start_index = 0
        for m in desc_period_index:
            if description[m.start()+1]==" ":
                if start_index==num-1:
                    print("ending")
                    return new_desc
                else:
                    start_index= m.start()+1
            else:
                if start_index==num-1:
                    print("ending")
                    return new_desc
                else:
                    first_part = description[start_index:m.start()]
                    new_first = first_part + " "
                    new_desc+= new_first
                    start_index = m.start()+1
    except:
        return

def get_category(category,header):
    cat_url = WP_CATEGORIES
    response = requests.get(cat_url , headers=header)
    res = response.json()

    cat_name_amp = category.replace("&","&amp;")

    cat_id = 0
    categories = []
    shortened_cat_name = category.replace("&","")
    shortened_cat_name = shortened_cat_name.replace("  ", " ")
    cat_slug = shortened_cat_name.replace(" ","-")

    for i in range(0,len(res)):
        categories.append(res[i]['name'])

    if cat_name_amp in categories:

        new_cat_url = cat_url +"?slug="+cat_slug
        cat_res = requests.get(new_cat_url, headers=header)
        cat_json = cat_res.json()
        print('exists')
        return cat_json[0]['id']

    else:
        post = {
            'name' : category
        }
        cat_res = requests.post(cat_url , headers=header, json=post)
        new_cat_url = cat_url +"?slug="+cat_slug
        cat_res = requests.get(new_cat_url, headers=header)
        cat_json = cat_res.json()
        print("doesn't exist")
        return cat_json[0]['id']

def restImgUL(imgPath, type, title):
    data = open(imgPath, 'rb').read()

    file_name = 'attachment; filename='+title
    new_type = 'image/'+type
    res = requests.post(url=WP_MEDIA,
                        data=data,
                        headers={ 'Content-Type':  new_type,'Content-Disposition' : file_name},
                        auth=(WP_APPLICATION_USERNAME, WP_APPLICATION_PASSWORD))
    print(res.json())
    newDict=res.json()
    newID= newDict.get('id')
    link = newDict.get('guid').get("rendered")
    return (newID)


def get_tags(tags, header):
    tag_url = WP_TAGS
    new_tags = []
    
    for l in range(0,len(tags)):
        tags[l]=tags[l].replace("#","")
        tag_url_2 = WP_TAGS+"?search="+tags[l]
        response = requests.get(tag_url_2 , headers=header)
        res = response.json()
        
        old_tags = []

        for i in range(0,len(res)):
            old_tags.append(res[i]['name'])

        print("searching for "+tags[l])
        if tags[l] in old_tags:
            print("found tag "+tags[l]+" in "+ str(old_tags))
            new_tag_url = tag_url + "?slug="+ tags[l]
            tag_res = requests.get(new_tag_url, headers=header)
            tag_json = tag_res.json()
            new_tags.append(tag_json[0]['id'])
            if l == len(tags)-1:
                print(new_tags)
                return new_tags
        else:
            post = {
                'name' : tags[l]
            }
            print("did not find tag "+tags[l]+" in "+str(old_tags))
            tag_res = requests.post(tag_url , headers=header, json=post)
            new_tag_url = tag_url +"?slug="+tags[l]
            tag_res = requests.get(new_tag_url, headers=header)
            tag_json = tag_res.json()
            new_tags.append(tag_json[0]['id'])
            if l == len(tags)-1:
                print(new_tags)
                return new_tags

def replace_features_nouns(input):
    input['features_title_schema_1'] = input['features_title_schema_1'].replace("Our", "Their")
    input['features_title_schema_1'] = input['features_title_schema_1'].replace("our", "their")
    input['features_title_schema_1'] = input['features_title_schema_1'].replace("We've", "They've")
    input['features_title_schema_1'] = input['features_title_schema_1'].replace("we've", "they've")
    input['features_title_schema_1'] = input['features_title_schema_1'].replace("We", "They")
    input['features_title_schema_1'] = input['features_title_schema_1'].replace("we", "they") 

    input['features_description_schema_1'] = input['features_description_schema_1'].replace("Our", "Their")
    input['features_description_schema_1'] = input['features_description_schema_1'].replace("our", "their")
    input['features_description_schema_1'] = input['features_description_schema_1'].replace("We've", "They've")
    input['features_description_schema_1'] = input['features_description_schema_1'].replace("we've", "they've")
    input['features_description_schema_1'] = input['features_description_schema_1'].replace("We", "They")
    input['features_description_schema_1'] = input['features_description_schema_1'].replace("we", "they") 

    input['features_title_schema_2'] = input['features_title_schema_2'].replace("Our", "Their")
    input['features_title_schema_2'] = input['features_title_schema_2'].replace("our", "their")
    input['features_title_schema_2'] = input['features_title_schema_2'].replace("We've", "They've")
    input['features_title_schema_2'] = input['features_title_schema_2'].replace("we've", "they've")
    input['features_title_schema_2'] = input['features_title_schema_2'].replace("We", "They")
    input['features_title_schema_2'] = input['features_title_schema_2'].replace("we", "they") 

    input['features_description_schema_2'] = input['features_description_schema_2'].replace("Our", "Their")
    input['features_description_schema_2'] = input['features_description_schema_2'].replace("our", "their")
    input['features_description_schema_2'] = input['features_description_schema_2'].replace("We've", "They've")
    input['features_description_schema_2'] = input['features_description_schema_2'].replace("we've", "they've")
    input['features_description_schema_2'] = input['features_description_schema_2'].replace("We", "They")
    input['features_description_schema_2'] = input['features_description_schema_2'].replace("we", "they") 

    input['features_title_schema_3'] = input['features_title_schema_3'].replace("Our", "Their")
    input['features_title_schema_3'] = input['features_title_schema_3'].replace("our", "their")
    input['features_title_schema_3'] = input['features_title_schema_3'].replace("We've", "They've")
    input['features_title_schema_3'] = input['features_title_schema_3'].replace("we've", "they've")
    input['features_title_schema_3'] = input['features_title_schema_3'].replace("We", "They")
    input['features_title_schema_3'] = input['features_title_schema_3'].replace("we", "they") 

    input['features_description_schema_3'] = input['features_description_schema_3'].replace("Our", "Their")
    input['features_description_schema_3'] = input['features_description_schema_3'].replace("our", "their")
    input['features_description_schema_3'] = input['features_description_schema_3'].replace("We've", "They've")
    input['features_description_schema_3'] = input['features_description_schema_3'].replace("we've", "they've")
    input['features_description_schema_3'] = input['features_description_schema_3'].replace("We", "They")
    input['features_description_schema_3'] = input['features_description_schema_3'].replace("we", "they") 

    input['features_title_schema_4'] = input['features_title_schema_4'].replace("Our", "Their")
    input['features_title_schema_4'] = input['features_title_schema_4'].replace("our", "their")
    input['features_title_schema_4'] = input['features_title_schema_4'].replace("We've", "They've")
    input['features_title_schema_4'] = input['features_title_schema_4'].replace("we've", "they've")
    input['features_title_schema_4'] = input['features_title_schema_4'].replace("We", "They")
    input['features_title_schema_4'] = input['features_title_schema_4'].replace("we", "they") 

    input['features_description_schema_4'] = input['features_description_schema_4'].replace("Our", "Their")
    input['features_description_schema_4'] = input['features_description_schema_4'].replace("our", "their")
    input['features_description_schema_4'] = input['features_description_schema_4'].replace("We've", "They've")
    input['features_description_schema_4'] = input['features_description_schema_4'].replace("we've", "they've")
    input['features_description_schema_4'] = input['features_description_schema_4'].replace("We", "They")
    input['features_description_schema_4'] = input['features_description_schema_4'].replace("we", "they") 

    input['features_title_schema_5'] = input['features_title_schema_5'].replace("Our", "Their")
    input['features_title_schema_5'] = input['features_title_schema_5'].replace("our", "their")
    input['features_title_schema_5'] = input['features_title_schema_5'].replace("We've", "They've")
    input['features_title_schema_5'] = input['features_title_schema_5'].replace("we've", "they've")
    input['features_title_schema_5'] = input['features_title_schema_5'].replace("We", "They")
    input['features_title_schema_5'] = input['features_title_schema_5'].replace("we", "they") 

    input['features_description_schema_5'] = input['features_description_schema_5'].replace("Our", "Their")
    input['features_description_schema_5'] = input['features_description_schema_5'].replace("our", "their")
    input['features_description_schema_5'] = input['features_description_schema_5'].replace("We've", "They've")
    input['features_description_schema_5'] = input['features_description_schema_5'].replace("we've", "they've")
    input['features_description_schema_5'] = input['features_description_schema_5'].replace("We", "They")
    input['features_description_schema_5'] = input['features_description_schema_5'].replace("we", "they")

    return input 


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def remove_extra_heading(nth_text, heading):
    heading_w_newline = heading+"\n\n" 
    heading_w_newline_and_colon = heading+":\n\n" 
    if heading_w_newline in nth_text:
        nth_text_shortened = nth_text.replace(heading_w_newline, "")
    elif heading_w_newline_and_colon in nth_text:
        nth_text_shortened = nth_text.replace(heading_w_newline_and_colon, "")
    else:
        nth_text_shortened = nth_text

    return nth_text_shortened

def add_json_characters(nth_text_shortened):
    test_res = '{"blog_section": "'+nth_text_shortened
    period_index = test_res.rfind(".") + 1
    res_2 = test_res[:period_index]+'"}'
    return res_2