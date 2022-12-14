import requests
import re
import numpy as np
import pandas as pd
import queue
from rich.console import Console
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from modules.bypass import captha_bypass
from modules import file_operations

class Scraper:
    def __init__(self):
        self.console = Console()
        self.session = requests.Session()
        self.Q = queue.Queue()
        self.ua = UserAgent(browsers=['edge', 'chrome'])
        self.headers = {
            "User-Agent": self.ua.random,
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1'
        }
        self.base_url = "https://www.amazon.com"
    
    def create_link(self, asin = []):
        craete_link = []

        with self.console.status('[cyan]Creating link.[/cyan]') as status:
            for a in asin:
                craete_link.append(f"{self.base_url}/dp/{a}".strip())
            self.console.log('Cretead links.')
        return craete_link

    def _get_link(self, link):
        req = self.session.get(link, headers=self.headers)
        html = BeautifulSoup(req.text , 'lxml')

        if req.text.find("you're not a robot") > 0:
            html = captha_bypass.amazon_bypass(link=link)
        
        title = self.get_title(html)
        price = self.get_price(html)
        status = self.get_status(html)

        self.Q.put({
            "Usa Price": str(price).strip(),
            "Title": str(title).strip(),
            "Status": str(status).strip(),
            "Link": link,
        })

    def get_title(self, soup):
        try:
            title = soup.find('span', {'id': 'productTitle'}).text
        except:
            title = "null"
        
        return title
    
    def get_price(self, soup):
        class_name = ['a-price a-text-price', 'a-size-mini olpWrapper', 'a-price', 'a-size-mini olpMessageWrapper', 'a-price aok-align-center']
        for c in class_name:
            if len(soup.findAll('span', {'class': c})) > 0:
                price = soup.findAll('span', {'class': c})[0].text
                parse_price = re.search(r'\$(.*)\$|\$(.*)', price).group(0).replace('$', '')
                
                return parse_price
    
    def get_status(self, soup):

        if str(soup).find('Currently unavailable.') > 0:
            status = "Currently unavailable."
        elif str(soup).find("Sorry! We couldn't find that page.") > 1:
            status = "Product Not Found"
        elif str(soup).find("Temporarily out of stock.")> 1:
            status = "Temporarily out of stock."
        else: 
            status = 'Product Found'
        return status

    def merge_df(self, df1, df2):
        merge = [df1, df2]
        df = pd.concat(merge, axis=1)

        return df
    
    def data_info(self):
        df = file_operations.open_file()

        df = df[:200]
        df['Usa Price'].replace('None',np.nan, inplace=True)   
        # All Null Values
        all_null = df.isnull().sum()
        print('\n\n')
        self.console.print('All null values')
        self.console.print(all_null)

        # Diffrence
        difference = len(df) - df['Usa Price'].isna().sum()
        A = len(df)
        B = difference
        percent = abs((B - A) / B) * 100
        self.console.print(f'Total Detect Price: {difference} Percent: {"%.2f" % percent}')
