import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

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
        pass
    else:
        return html
