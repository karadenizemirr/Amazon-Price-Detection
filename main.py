from rich.console import Console
from modules import scraper
from rich.prompt import Prompt
from modules import file_operations

console = Console()
_scraper = scraper.Scraper()

console.print(""" 

    [blue]\n------> Amazon Price Detect with Asin Code <------[/blue]
    \n
    \nAuthor: Emirhan KARADENİZ
    \nVersion: 2022.1
    \nGithub: https://github.com/karadenizemirr
    \n
    [purple]\nOperations[/purple]
    (1) - Price detect with asin code
    (2) - Data Info
    (3) - Exit
    \n\n
    \n[red]Warning:Recommended 1000 rows of data.[/red]

""", style="bold yellow", justify="center")

def main():
    select_operations = Prompt.ask('Please select operations number: ', choices=['1', '2', '3'],default='1')

    if select_operations == '1':
        # Open Excel File
        df = file_operations.open_file()

        # Create Links
        links = _scraper.create_link(asin=df['ASIN NO'][:10])
        #Links Scraper
        result = _scraper.get_link(links=links)

        #Merge df
        # merge_df = _scraper.merge_df(df1=df, df2=result)

        # #Save Df
        # save_questions = Prompt.ask('Do you want to save the file: ', choices=['y','n'], default='y')
        # if save_questions == 'y':
        #     file_operations.save_file(merge_df)
        # elif save_questions == 'n':
        #     console.print(merge_df)

    elif select_operations == '2':
        _scraper.data_info()
    elif select_operations == '3':
        quit()

if __name__ == '__main__':  
    while True:
        main()