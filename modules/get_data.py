
from modules import scraper
from bs4 import BeautifulSoup
from modules.bypass import captha_bypass
from multiprocessing import Process, Queue

class DataGenerator(scraper.Scraper):
    def __init__(self, links):
        super().__init__()
        self.links = links
        
        self.run()

    
    def get_link(self,link):
        req = self.session.get(link, headers=self.headers)
        html = BeautifulSoup(req.text, 'lxml')

        if str(html).find("you're not a robot")>0:
            html = captha_bypass.amazon_bypass(link)
        
        print(req.status_code)

    def run(self):
        processes = []

        for link in self.links:
            processes.append(Process(target=self.get_link, args=(link,)))
        
        for process in processes:
            process.start()
        
        for process in processes:
            process.join()
    