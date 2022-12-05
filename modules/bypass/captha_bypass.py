import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from amazoncaptcha import AmazonCaptcha

# Create Driver and Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
chrome_driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
chrome_driver.delete_all_cookies()

def amazon_bypass(link=None):
    chrome_driver.get(link)
    html = BeautifulSoup(chrome_driver.page_source, 'lxml')
    
    if str(html).find("you're not a robot") > 0:
        # Bypass Captha
        _input = '//*[@id="captchacharacters"]'
        _button = '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button'
        _image = '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img'

        image = chrome_driver.find_element(By.XPATH, _image).get_attribute('src')
        c_text = AmazonCaptcha.fromlink(image)
        
        #input
        chrome_driver.find_element(By.XPATH, _input).send_keys(c_text)
        # click
        chrome_driver.find_element(By.XPATH, _button).click()

        pass
    else:
        chrome_driver.close()
        return html
