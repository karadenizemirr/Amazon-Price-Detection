import requests
import re
import pandas as pd
from multiprocessing import Process, Queue
from rich.console import Console
from fake_useragent import UserAgent
from threading import Thread
from bs4 import BeautifulSoup
from modules.bypass import captha_bypass
from rich.progress import Progress


class Scraper:
    def __init__(self):
        self.console = Console()
        self.session = requests.Session()
        self.Q = Queue()
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

    def get_link(self, links = []):
        data = []
        processes = []
        for l in links:
            processes.append(Process(target=self._get_link, args=(l,)))
        
        with Progress() as progress:
            pbar = progress.add_task('[yellow]Started modules..[/yellow]', total=len(processes))
            for process in processes:
                process.start()
                progress.update(pbar, advance=1)
        
        with Progress() as progress:
            pbar = progress.add_task('Get detail..', total=len(processes))
            for process in processes:
                process.join()
                data.append(self.Q.get())
                progress.update(pbar, advance=1)
        
        self.console.log('\nGet detail operations end.\n', style="bold green")
        df = pd.DataFrame(data)
        return df

    def get_title(self, soup):
        try:
            title = soup.find('span', {'id': 'productTitle'}).text
        except:
            title = "null"
        
        return title
    
    def get_price(self, soup):
        class_name = ['a-price a-text-price', 'a-size-mini olpWrapper', 'a-price', 'a-size-mini olpMessageWrapper']
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
        else: 
            status = 'Product Found'
        return status

    def merge_df(self, df1, df2):
        merge = [df1, df2]
        df = pd.concat(merge, axis=1)

        return df
