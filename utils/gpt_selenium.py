import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent



# op = uc.ChromeOptions()
# op.add_argument(f"user-agent={UserAgent.random}")
# op.add_argument("user-data-dir=./")
# op.add_experimental_option("detach", True)
# op.add_experimental_option("excludeSwitches", ["enable-logging"])
# op.add_argument('ignore-certificate-errors')

# driver = uc.Chrome(chrome_options=op)

    
def openai_login(driver, MAIL,PASSWORD):
    print("Current session is {}".format(driver.session_id))
    driver.execute_script('''window.open("https://chat.openai.com/auth/login","_blank");''') # open page in new tab
    time.sleep(5) # wait until page has loaded
    driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
    driver.close() # close first tab
    driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab

    time.sleep(10)
    inputElements = driver.find_elements(By.TAG_NAME, "button")
    inputElements[0].click()
    time.sleep(3)
    mail = driver.find_elements(By.TAG_NAME,"input")[1]
    mail.send_keys(MAIL)
    time.sleep(4)

    btn = driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div/div/div[1]/div/form/div[2]/button")
    btn.click()

    time.sleep(5)
    password= driver.find_elements(By.TAG_NAME,"input")[2]
    password.send_keys(PASSWORD)

    time.sleep(10)
    btn=driver.find_element(By.XPATH,"/html/body/div[1]/main/section/div/div/div/form/div[3]/button")
    btn.click()

    time.sleep(10)


    btn=driver.find_element(By.XPATH,"//*[contains(text(),'Okay, le')]")
    btn.click()

    time.sleep(10)

    btn=driver.find_element(By.XPATH,"//*[text()='GPT-4']")
    btn.click()



def rephrase_gpt_4(driver, humanize_prompt, text, sec_num):
    while(True):
        time.sleep(10)
        response = get_response_1(humanize_prompt, sec_num, driver)

        time.sleep(20)
        print("<<---- text is start")
        print(text)
        print("<<---- text is end")
        response2 = get_response(text, sec_num, driver)

        time.sleep(30)
        print(response2)
        return response2



def get_response(prompt, sec_num, driver):
    inputElements = driver.find_elements(By.TAG_NAME, "textarea")
    # inputElements[0].send_keys(prompt)
    for i in range(len(prompt)):
        inputElements[0].send_keys(prompt[i])
        time.sleep(1/40)
    # time.sleep(120)
    send = driver.find_element(By.XPATH, "//*[@id='__next']/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/button")
    send.click()
    time.sleep(125) 

    el = driver.find_elements(By.TAG_NAME, "code")
    print("clicking")
    response = el[sec_num].get_attribute('textContent')
    print(response)

    return response

def get_response_1(prompt, sec_num, driver):
    inputElements = driver.find_elements(By.TAG_NAME, "textarea")
    inputElements[0].send_keys(prompt)
    
    time.sleep(10)
    send = driver.find_element(By.XPATH, "//*[@id='__next']/div[1]/div[2]/div/main/div/div[2]/form/div/div[2]/div/button")
    send.click()
    time.sleep(10)

    inputElements = driver.find_elements(By.TAG_NAME, "p")
    time.sleep(5)
    response=inputElements[0].get_attribute('textContent')

    # inputElement = driver.find_element(By.XPATH, "//*[@id='__next']/div[1]/div[2]/div/main/div/div[1]/div/div/div/div[4]/div/div/div[2]/div[1]/div/div")
    # response=inputElement.get_attribute('textContent')
    return response
    


    



      
      

        

