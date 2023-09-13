import time, re, sys, random, string, pyperclip
from colorama import Fore, init
from tempmail import EMail
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from cookies import cookies
init()





def openai_auto():

    while True:
        try:
            # Initialize the WebDriver
            user_agent = UserAgent()
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--log-level=3")
            options.add_argument('--no-proxy-server')
            options.add_argument("--incognito")
            options.add_argument(f"user-agent={user_agent.random}")
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

            prefs = {"profile.default_content_setting_values.notifications": 2}
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=options)
            # for cook in cookies:
            #     driver.add_cookie({"name" : cook['name'], "value" : cook['value']})
                

            driver.get("https://chat.openai.com/auth/login")

            time.sleep(15)
            # WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log in')]"))).click()
            driver.find_element(By.XPATH, "//*[contains(text(), 'Log in')]").click()
            time.sleep(10)

            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/section/div/div/div/div[4]/form[2]/button'))).click()
            time.sleep(10)

            WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, 'WBW9sf'))).click()                                                         
            time.sleep(10)
            

        except:
            pass

openai_auto()