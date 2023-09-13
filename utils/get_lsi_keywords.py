import json
import http.client
import sys
import time, pyperclip
from utils.prompts import humanize_prompt
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

executable_path = "/home/jacobadelman/python3/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

def get_lsi_keywords(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query
        })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
        }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded = json.loads(data.decode("utf-8"))


    op = webdriver.ChromeOptions()
    op.add_extension("./utils/harper.crx")

    driver = webdriver.Chrome(options=op)

    time.sleep(7)
    driver.switch_to.new_window('tab')
    my_link = ''
    for p in range(len(decoded['organic'])):
        if 'amazon' not in decoded['organic'][p]['link']:
            my_link = decoded['organic'][p]['link']
            break

    driver.get(my_link)
    time.sleep(10)
    elements=driver.find_elements(By.TAG_NAME, "body")
    elements[0].send_keys(Keys.CONTROL, 'A')

    time.sleep(25)
    iframe = driver.find_element(By.XPATH, "//iframe[@class='__hrp-frame__iframe']")
    driver.switch_to.frame(iframe)

    time.sleep(4)
    settings = driver.find_element(By.CLASS_NAME, 'CreatorHeader__icon_type_settings')
    settings.click()

    time.sleep(4)
    settings = driver.find_element(By.CLASS_NAME, 'Dropdown__iconAndValue')
    settings.click()

    time.sleep(4)
    driver.find_element(By.XPATH, "//*[text()='OpenAI API key']").click()

    time.sleep(4)
    api_key = driver.find_element(By.CLASS_NAME, "SettingsSectionApiKey__input")
    api_key.send_keys(OPENAI_API_KEY)

    time.sleep(4)
    back_normal = driver.find_element(By.CLASS_NAME, "CreatorHeader__button")
    back_normal.click()


    time.sleep(4)
    txt = driver.find_element(By.CLASS_NAME, 'Input__input')
    text = "/extractandresearchSEOkeywords"
    txt.send_keys(text)

    time.sleep(4)
    txt.send_keys(Keys.ENTER)
    


    time.sleep(5)
    txt2 = driver.find_element(By.TAG_NAME, 'textarea')
    txt2.send_keys("""{{page}} return an html table but without the 'html', 'head' and 'body' tags""")

    time.sleep(4)
    txt2.send_keys(Keys.ENTER)


    time.sleep(50)
    # tb = 'None'
    # try:
    tb = driver.find_element(By.TAG_NAME, 'table').get_attribute('outerHTML')
    # except:
    #     tb = driver.find_element(By.CLASS_NAME, 'markdown-bod').get_attribute('innerText')


    time.sleep(10)
    driver.close()

    return tb