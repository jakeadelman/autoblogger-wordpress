import time, re, sys, random, string, pyperclip
from colorama import Fore, init
from tempmail import EMail
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
init()

def generate_password(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def extract_verify_link(text):
    pattern = r'<a\s+href="([^"]+)"[^>]*>https://undetectable\.ai/verify/\?a=[^<]+</a>'
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    else:
        return None

def main(purpose_choice, readability_choice, article_text):
    try:
        # with open(article_file_path, 'r') as article_file:
        #     article_text = article_file.read()

        # Split the article into chunks of 250 words
        words = article_text.split()
        article_chunks=[]
        # chunk_size = 250
        tot_len = 0
        while tot_len < len(words):
            new_words = []
            numwords=0 
            cut_words = words[tot_len:tot_len+250]
            for word in reversed(cut_words):
                if word[-1] =='.':
                    new_words = cut_words[0:250-numwords]
                    new_words2 = " ".join(new_words)
                    article_chunks.append(new_words2)
                    tot = 250-numwords
                    tot_len+=tot
                    break
                else:
                    numwords+=1

        print("<--- cut end start")
        print(article_chunks)
        print("<--- cut end")
        # time.sleep(50)
        # article_chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        # print(len(article_chunks))
        # print(article_chunks)
        # if not article_chunks:
        #     print(f"{Fore.RED}Your file is empty.")
        #     return

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

        new_text = ""

        while article_chunks:
            
            print("<----- chunk")
            print(article_chunks)
            print("<---- chunk end")
            # Generate temp email
            email = EMail()
            password = generate_password()

            with open('accounts.txt', 'a') as file:
                file.write(f'{email}:{password}\n')

            # Create a new WebDriver instance for each account
            driver = webdriver.Chrome(options=options)

            try:
                driver.get("https://undetectable.ai/login")

                # Click registration button
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vplpzd"]/div[7]/div[2]'))).click()

                # Enter email and password
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/input'))).send_keys(str(email))
                driver.find_element(By.XPATH, '//*[@id="pws"]').send_keys(password)

                # Check terms and conditions and click register
                driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/div[4]/button').click()
                driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/button').click()

                # Wait for the confirmation email to arrive
                msg = email.wait_for_message()

                verify_link = extract_verify_link(msg.body)
                if verify_link:
                    driver.get(verify_link)
                    time.sleep(1)
                    driver.get("https://undetectable.ai")
                else:
                    print(f"{Fore.RED}Verify link not found.")

                purpose = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/div[1]/div[2]/select')
                readability = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/div[1]/div[1]/select')

                select1 = Select(purpose)
                select2 = Select(readability)

                options1 = select1.options
                options2 = select2.options

                if 1 <= purpose_choice <= len(options1) - 1:
                    select1.select_by_index(purpose_choice)

                if 1 <= readability_choice <= len(options2) - 1:
                    select2.select_by_index(readability_choice)

                driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/button').click()
                # driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]').click()
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[3]/div').click()
                # Get the next chunk to submit
                chunk = article_chunks.pop(0)
                if len(chunk)<50:
                    new_text+=chunk
                else:
                    textarea = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/textarea')
                    textarea.clear()
                    textarea.send_keys(chunk)

                    humanize = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/button[2]').click()


                    
                    time.sleep(1)
                    rehumanize = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'cmaYaCaW')))                                                            
                    rehumanize.click()
                    
                    time.sleep(5)
                    paraphrased = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[1]/div[4]/button')))
                    paraphrased.click()

                    time.sleep(3)

                    copied_content = pyperclip.paste()
                    new_text += copied_content
                    # with open('paraphrased.txt', 'a') as new:
                    #     new.write(f'{copied_content}\n')

            except Exception as e:
                print(f"Error during registration: {e}")
            finally:
                driver.quit         
        print(f"Article has been paraphrased successfully.")
        print(new_text)
        return new_text


    except Exception as e:
        print(f"Error during article submission: {e}")

# if __name__ == "__main__":
#     try:
#         main(3, 5, text)
#     except:
#         print(f"{Fore.RED}Aborting ...")
#         sys.exit()
