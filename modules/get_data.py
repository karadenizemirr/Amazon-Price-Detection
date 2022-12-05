from modules import scraper
from multiprocessing import Process, Queue

class GetData(scraper.Scraper):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.procs = []
        self.run()

    def run(self):
        for d in self.data:
            proc = Process(target=self._get_link, args=(d,))
            self.procs.append(proc)
            proc.start()
        

        for proc in self.procs:
            proc.join()
        
        return self.Q.get()