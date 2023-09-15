from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import time
import os
from dotenv import load_dotenv

load_dotenv()

GPT_USERNAME = os.getenv('GPT_USERNAME')
GPT_PASSWORD = os.getenv('GPT_PASSWORD')

op = uc.ChromeOptions()
op.add_argument("--headless")
op.add_argument(f"user-agent={UserAgent.random}")
op.add_argument("user-data-dir=./")

op.add_experimental_option("detach", True)
op.add_experimental_option("excludeSwitches", ["enable-logging"])
op.add_argument('ignore-certificate-errors')

driver = uc.Chrome(chrome_options=op)


driver.execute_script('''window.open("https://chat.openai.com/auth/login","_blank");''') # open page in new tab
time.sleep(5) # wait until page has loaded
driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
driver.close() # close first tab
driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab

time.sleep(10000000)