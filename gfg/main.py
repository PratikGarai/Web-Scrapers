from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from typing import Tuple, Union

MAIN_URL = "https://www.geeksforgeeks.org/python-programming-language/"
SECTIONS = ["Basics", "io", "Data Types", "Variables", "Operators", "Control Flow", \
    "Functions", "Object Oriented Concepts", "Exception Handling", "Python Collections", \
    "Django tutorial", "Data Analysis", "Numpy", "Pandas", "Machine Learning with Python",\
    "Python GUI", "Modules in Python", "WorkingWithDatabase", "Misc", "Applications and Projects"]


def process_class_name(st : str) -> str :
    return ".".join(st.split(" "))


def write_html_to_file(fname : str, html : BeautifulSoup) -> None:
    s = str(html.html)
    try : 
        with open(fname, "w+",  encoding="utf-8") as f :
            f.write(s)
    except Exception as e :
        raise Exception("Error in writing html to file : ", e)


def scrape_page(url: str) -> Tuple[int, Union[BeautifulSoup, None]]:
    try:
        page = requests.get(url)
        status = page.status_code
        html = BeautifulSoup(page.content, "html.parser")
        return (200, html)
    except Exception as e:
        return (-1, None)


def scrape_gfg() -> None:
    try : 
        status, page = scrape_page(MAIN_URL)
        assert status==200 , f"Status {status}"
        for i in SECTIONS :
            links = page.select(f"div.{process_class_name(i)} a")
            print(f"{i}: {len(links)}")
    except Exception as e : 
        print("Error in main : ", e)


if __name__ == "__main__":
    scrape_gfg()
