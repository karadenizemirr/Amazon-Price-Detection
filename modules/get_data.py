import pandas as pd
from modules import scraper
from multiprocessing import Process, Queue
from rich.progress import Progress

class GetData(scraper.Scraper):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.procs = []
        self.run()

    def run(self):
        create_new_data = []

        with Progress() as progress:
            pbar = progress.add_task('[blue]Start modules..[/blue]', total=len(self.data))
            for d in self.data:
                proc = Process(target=self._get_link, args=(d,))
                self.procs.append(proc)
                proc.start()
                create_new_data.append(self.Q.get())
                progress.update(pbar, advance=1)
        
        with Progress() as progress:
            pbar1 = progress.add_task('[yellow]Getting data..[/yellow]', total=len(self.procs))
            for proc in self.procs:
                proc.join()
                progress.update(pbar1, advance=1)
        
        new_data_frame = pd.DataFrame(create_new_data)
        return new_data_frame   