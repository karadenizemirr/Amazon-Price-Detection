from rich.console import Console
from rich.prompt import Prompt
from modules import scraper
from modules import file_operations

console = Console()
_scraper = scraper.Scraper()


def main():
    select_operations = Prompt.ask('Please select operation number: ', choices=['1','2','3'], default='1')
    if select_operations == '1':
        df = file_operations.open_file()
        product_link = _scraper.create_link(ansi=df['ASIN NO'])
        create_df = _scraper.get_data(product_link)
        merge_df = _scraper.data_merge(df1= df, df2= create_df)

        save_questions = Prompt.ask('Do you want to save the file: ', choices=['y','n'], default='y')

        if save_questions == 'y':
            file_operations.save_file(merge_df)
        else:
            print(merge_df)
    elif select_operations == '2':
        df = file_operations.open_file()
        _scraper.data_info(df)
        
if __name__ == '__main__':
    main()