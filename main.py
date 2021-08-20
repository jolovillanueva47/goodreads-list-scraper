from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup
import requests

def main():
    print("GoodReads List Scraper\n")
    url=input("Please input url for Goodreads list to scrape: ")
    print("\nSelect values to scrape:\n")
    options = ["Book Title Only", "Book Title and Author"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")
    soup=get_soup(url)
    num_of_pages=get_number_of_pages(soup)
    goodreads_list=[]
    goodreads_dict={}
    for page_num in range(1,num_of_pages+1):
        soup=get_soup(f"{url}?page={page_num}")
        if menu_entry_index==0:
            goodreads_list+=scrape_data(menu_entry_index,soup)
        else:
            goodreads_dict_temp=scrape_data(menu_entry_index,soup)
            goodreads_dict=merge_two_dicts(goodreads_dict,goodreads_dict_temp)
    if menu_entry_index==0:
        show_table(goodreads_list,menu_entry_index)
    else:
        show_table(goodreads_dict,menu_entry_index)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def get_number_of_pages(soup):
    pages=soup.select("div.pagination>a")
    if not pages:
        return 1
    else:
        return int(pages[-2].getText())

def get_soup(url):
    response=requests.get(url)
    goodreads_webpage=response.text
    soup=BeautifulSoup(goodreads_webpage,"html.parser")
    return soup

def scrape_data(choice,soup):
    book_title_results=soup.select("a.bookTitle>span")
    goodreads_dict={}
    goodreads_list=[]
    if choice==0:
        for book_title in book_title_results:
            goodreads_list.append(book_title.getText())
        return goodreads_list
    else:
        author_results=soup.select("a.authorName>span")
        for (book_title,author) in zip(book_title_results,author_results):
            goodreads_dict[book_title.getText()]=author.getText()
        return goodreads_dict


def show_table(data,choice):
    print()
    table = Table(title="Goodreads List")

    table.add_column("Book Title", justify="left", style="cyan", no_wrap=False)
    if choice==1:
        table.add_column("Author", style="magenta")
        for index,(key,value) in enumerate(data.items(),start=1):
            table.add_row(f"{index}. {key}",value)
    else:
        for index,value in enumerate(data,start=1):
            table.add_row(f"{index}. {value}")
    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()