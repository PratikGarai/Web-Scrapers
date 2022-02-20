from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from typing import Tuple, Union

MAIN_URL = "https://www.geeksforgeeks.org/python-programming-language/"


def scrape_page(url: str) -> Tuple[int, Union[BeautifulSoup, None]]:
    try:
        page = requests.get(url)
        status = page.status_code
        if status != 200:
            print(f"Status {status} on url {url}")
            return (status, None)
        html = BeautifulSoup(page.content, "html.parser")
        return (200, html)
    except Exception as e:
        print(e)
        return (-1, None)

def scrape_gfg():
    status, page = scrape_page(MAIN_URL)

    if status==-1 :
        return
    print(page.text)


if __name__ == "__main__":
    scrape_gfg()
