
import re
import requests
from pprint import pprint
import os
import json

def paragraphize(verdict):
    out = []
    threshold = 350
    for chunk in verdict.split('. '):
        if out and len(chunk)+len(out[-1]) < threshold:
            out[-1] += ' '+chunk+'. '
        else:
            out.append(chunk+'. ')
    new_verdict =''
    for i in range(0,len(out)):
        new_string = out[i]+"\n\n"
        new_verdict+=new_string
        if i == len(out)-1:
            new_verdict = new_verdict[:-1]
            return new_verdict

def add_space(finder,description):
    try:
        # print(description)
        desc_period_index = re.finditer(finder,description)
        num = re.findall(finder, description)
        num = len(num)
        # print(desc_exclamation_index)
        print("<------ok")
        # print(desc_period_index)
        # print(len(desc_period_index))
        # print(desc)
        # print(len(desc_period_index))
       
        new_desc = ""
        start_index = 0
        for m in desc_period_index:
            if description[m.start()+1]==" ":
                if start_index==num-1:
                    print("ending")
                # if m.start()==desc_period_index[-1]:
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
    cat_url = "https://mindfuelwave.com/wp-json/wp/v2/categories"
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
    url='https://mindfuelwave.com/wp-json/wp/v2/media/hello'
    data = open(imgPath, 'rb').read()

    file_name = 'attachment; filename='+title
    new_type = 'image/'+type
    res = requests.post(url='https://mindfuelwave.com/wp-json/wp/v2/media',
                        data=data,
                        headers={ 'Content-Type':  new_type,'Content-Disposition' : file_name},
                        # headers={ 'Content-Type': 'image/jpg','Content-Disposition' : 'attachment; filename=%s'% fileName},
                        auth=('wpauserd5S2jmuq', 'H1DA pOGr 566a C55Y eolg FDpM'))
    # pp = pprint.PrettyPrinter(indent=4) ## print it pretty. 
    # pp.pprint(res.json()) #this is nice when you need it
    print(res.json())
    newDict=res.json()
    newID= newDict.get('id')
    link = newDict.get('guid').get("rendered")
    # print(newID, link)
    return (newID)

def get_tags(tags, header):
    tag_url = "https://mindfuelwave.com/wp-json/wp/v2/tags"
    # response = requests.get(tag_url , headers=header)
    # res = response.json()
    # pprint(res)
    # print(len(res))
    
    # old_tags = []

    # for i in range(0,len(res)):
    #     old_tags.append(res[i]['name'])

    new_tags = []
    
    for l in range(0,len(tags)):
        tags[l]=tags[l].replace("#","")
        # print(old_tags)
        tag_url_2 = "https://mindfuelwave.com/wp-json/wp/v2/tags?search="+tags[l]
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
