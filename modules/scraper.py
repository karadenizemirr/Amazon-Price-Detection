import time
import re
import pandas as pd
from amazoncaptcha import AmazonCaptcha
from bs4 import BeautifulSoup
from rich.console import Console
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper:
    def __init__(self):
        self.product_link_path = "data/links.txt"
        self.base_url = "https://amazon.com"
        self.console = Console()
        
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
        
    def create_link(self, ansi =[]):
        product_links = []

        with self.console.status('[cyan]Creating link..Please wait..[/cyan]') as status:
            start_time = time.perf_counter()
            for a in ansi:
                product_links.append(f'{self.base_url}/dp/{a}')
            stop_time = time.perf_counter()

            self.console.log(f'Created link..Total time: {stop_time - start_time:.4f}', style="bold green")
        
        return product_links

    def get_data(self, links):
        create_data = []
        counter = 0
        with self.console.status('[cyan]Creating data..[/cyan]') as status:
            for link in links:
                counter += 1
                self.driver.get(link)
                page_source = BeautifulSoup(self.driver.page_source, 'lxml')

                if str(page_source).find("you're not a robot") > 0:
                    # Bypass
                    image = page_source.find('div', {'class': 'a-row a-text-center'}).img['src']
                    solution = AmazonCaptcha.fromlink(image).solve()
                    self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/input').send_keys(solution)
                    self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button').click()
                    page_source = BeautifulSoup(self.driver.page_source, 'lxml')
                    self.console.log(f'Index: {counter} Checking: {link} System blocked', style="bold red")
                self.console.log(f'Index: {counter} Cheking: {link}', style="bold green")

                title = self.get_title(page_source)
                status = self.get_status(page_source)
                price = self.get_price(page_source)
                
                create_data.append({
                    "USA Price": price,
                    "Name": title,
                    "Link": link,
                    "Status": status
                })
            self.console.log('Created data', style="bold green")
        df = pd.DataFrame(create_data)
        return df

    def get_title(self, source):
        try:
            title = source.find('span', {'id': 'productTitle'}).text
        except:
            title = "null"
        
        return title
    
    def get_status(self,source):
        source = str(source)

        if source.find('Currently unavailable') > 0:
            status = "Currently unavailable"
        elif source.find("Sorry! We couldn't find that page") > 0:
            status = "Product Not Found"
        elif source.find('Temporarily out of stock.') > 0:
            status = "Temporarily out of stock."
        else:
            status = "Product Found"
        return status
    
    def get_price(self, source):
        class_name = ['a-size-mini olpMessageWrapper', 'a-price', 'a-size-mini olpWrapper']
        
        for c in class_name:
            price = source.find('span', {'class': c})
            
            if price != None:
                return str(re.findall(r"'([0-9].*)'", str(re.findall(r'\$(.*)\$|\$(.*)', price.text)[0]))[0]).replace("', '", "")
        pass
    
    def data_merge(self,df1, df2):
        frames = [df1, df2]
        merge_df = pd.concat(frames, axis=1)
        return merge_df
    

    def data_info(self, data):
        self.console.print("\nAll Null Values")
        null_value = data.isna().sum()
        self.console.print(null_value)
        print('\n')
        usa_price_null = data['USA Price'].isna().sum()
        self.console.print(f'USA Price is Null: {usa_price_null}')
        print('\n')
        detect_value = len(data) - usa_price_null
        self.console.print(f'Detect Price: {detect_value}')
        print('\n')
        percent_detect = abs((usa_price_null - len(data)) / usa_price_null) * 100
        self.console.print(f'Detect Price Percent: %{"%.2f" % percent_detect}\n')