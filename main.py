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
    show_table(scrape_data(url,menu_entry_index),menu_entry_index)


def scrape_data(url,choice):
    response=requests.get(url)
    goodreads_webpage=response.text
    soup=BeautifulSoup(goodreads_webpage,"html.parser")
    results=soup.find_all("a", class_="bookTitle")
    book_title_results=soup.select("a.bookTitle>span")
    goodreads_dict={}
    if choice==0:
        for index,book_title in enumerate(book_title_results, start=1):
            goodreads_dict[index]=[book_title.getText()]
    else:
        author_results=soup.select("a.authorName>span")
        for ((index,book_title),author) in zip(enumerate(book_title_results, start=1),author_results):
            goodreads_dict[index]=[book_title.getText(),author.getText()]
    return goodreads_dict

def show_table(data,choice):
    print()
    table = Table(title="Goodreads List")

    table.add_column("Book Title", justify="left", style="cyan", no_wrap=True)
    if choice==1:
        table.add_column("Author", style="magenta")
        for key,value in data.items():
            table.add_row(f"{key}. {value[0]}",value[1])
    else:
        for key,value in data.items():
            table.add_row(f"{key}. {value[0]}")
    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()