
import re
import requests
import os
from dotenv import load_dotenv
import nltk
import signal


load_dotenv()

WP_MEDIA = os.getenv('WP_MEDIA')
WP_APPLICATION_USERNAME = os.getenv('WP_APPLICATION_USERNAME')
WP_APPLICATION_PASSWORD = os.getenv('WP_APPLICATION_PASSWORD')
WP_CATEGORIES = os.getenv('WP_CATEGORIES')
WP_TAGS = os.getenv('WP_TAGS')

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
    heading_w_newline = heading+r"\n\n"
    heading_w_newline_and_colon = heading+r":\n\n"
    print("<-- in functions")
    print(heading_w_newline in nth_text)
    print("<-- in functions end")
    if heading_w_newline in nth_text:
        nth_text = nth_text.replace(heading_w_newline, "")
    elif heading_w_newline_and_colon in nth_text:
        nth_text = nth_text.replace(heading_w_newline_and_colon, "")
    else:
        print("passing")
        pass

    return str(nth_text)

def add_json_characters(nth_text_shortened):
    test_res = '{"blog_section": "'+nth_text_shortened
    period_index = test_res.rfind(".") + 1
    res_2 = test_res[:period_index]+'</p>"}'
    return res_2

def add_json_characters_intro(nth_text_shortened):
    test_res = '{"blog_section": "'+nth_text_shortened
    period_index = test_res.rfind(".") + 1
    res_2 = test_res[:period_index]+'"}'
    return res_2

def paragraphize3(input):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_tokenizer.tokenize(input)
    print(sentences)
    # sentences = sent_tokenizer.tokenize(input)
    sentences = [sent.capitalize() for sent in sentences]

    end = ''
    for senti in sentences:
        end = end+senti+" "

    return end


def paragraphize2(input):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_tokenizer.tokenize(input)
    print(sentences)
    # sentences = sent_tokenizer.tokenize(input)
    sentences = [sent.capitalize() for sent in sentences]

    par1 = ''
    par2 = ''
    par3 = ''
    par4 =''
    par5 =''
    par6 =''
    par7 = ''
    par8 = ''
    par9 = ''
    par10 = ''
    par11 = ''
    par12 = ''
    par13 = ''
    par14 = ''
    par15 = ''

    for senti in sentences:
        full_len = len(par1)+len(par2)+len(par3)+len(par4)+len(par5)+len(par6)+len(par7)+len(par8)+len(par9)+len(par10)+len(par11)+len(par12)+len(par13)+len(par14)+len(par15)
        if full_len< 250:
            par1 = par1+senti+" "
        elif full_len<500:
            par2 = par2+senti+" "
        elif full_len<750:
            par3 = par3+senti+" "
        elif full_len<1000:
            par4 = par4+senti+" "
        elif full_len<1250:
            par5 = par5+senti+" "
        elif full_len<1500:
            par6 = par6+senti+" "
        elif full_len<1750:
            par7 = par7+senti+" "
        elif full_len<2000:
            par8 = par8+senti+" "
        elif full_len<2250:
            par9 = par9+senti+" "
        elif full_len<2500:
            par10 = par10+senti+" "
        elif full_len<2750:
            par11 = par11+senti+" "
        elif full_len<3000:
            par12 = par12+senti+" "
        elif full_len<3250:
            par13 = par13+senti+" "
        elif full_len<3500:
            par14 = par14+senti+" "
        else:
            par15 = par15+senti+" "
    
    new_sentences =''
    if par2=='':
        new_sentences = par1
    elif par3=='':
        new_sentences = par1+"\n\n"+par2
    elif par4=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3
    elif par5=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4
    elif par6=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5
    elif par7=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7
    elif par8=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8
    elif par9=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9
    elif par10 =='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9+"\n\n"+par10
    elif par11=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9+"\n\n"+par10+"\n\n"+par11
    elif par12=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9+"\n\n"+par10+"\n\n"+par11+"\n\n"+par12
    elif par13=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9+"\n\n"+par10+"\n\n"+par11+"\n\n"+par12+"\n\n"+par13
    elif par14=='':
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9+"\n\n"+par10+"\n\n"+par11+"\n\n"+par12+"\n\n"+par13+"\n\n"+par14
    else:
        new_sentences=par1+"\n\n"+par2+"\n\n"+par3+"\n\n"+par4+"\n\n"+par5+"\n\n"+par6+"\n\n"+par7+"\n\n"+par8+"\n\n"+par9+"\n\n"+par10+"\n\n"+par11+"\n\n"+par12+"\n\n"+par13+"\n\n"+par14+"\n\n"+par15

    return new_sentences


class Timeout():
  """Timeout class using ALARM signal"""
  class Timeout(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    signal.alarm(0) # disable alarm

  def raise_timeout(self, *args):
    raise Timeout.Timeout()