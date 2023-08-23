import requests
from functions import restImgUL
import os
from pyunsplash import PyUnsplash
import random
import shutil
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')


def img_to_wp(query, keyword):
  print(query + ","+keyword)
  lower_keyword = keyword.lower()
  lower_keyword = lower_keyword.replace(" ","-")

  pu = PyUnsplash(api_key=UNSPLASH_API_KEY)

  search = pu.search(type_="photos", query=query)

  link = ''
  print("<---- starting img download")
  try:
    count = 0
    for entry in search.entries:
      count+=1
      print("<-------")
      print(" in here "+query)
      link = entry.link_download
      print(link)
      print("<-------")
      rand = random.randint(0, 1000)
      rand_name = lower_keyword+"-"+str(rand)
      print("<-----img name "+rand_name)
      response = requests.get(link, stream=True)
      file_name = "./images/"+rand_name+".jpeg"
      if response.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
      else:
        print('Image Couldn\'t be retrieved')

      img_similar_id = restImgUL(file_name, type="jpeg", title=rand_name)
      os.remove(file_name)  
      return img_similar_id
    if count==0:
      print("False 1")
      return(False)
  except:
    print("FALSE")
    return(False)

