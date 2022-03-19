from bs4 import BeautifulSoup
import requests
import time
from typing import Optional, Tuple, Union
import pandas as pd
import os

BASE_URL = "https://www.tutorialspoint.com"
MAIN_URL = "https://www.tutorialspoint.com/python/index.htm"


def process_class_name(st: str) -> str:
    return ".".join(st.split(" "))


def write_html_to_file(fname: str, html: BeautifulSoup) -> None:
    s = str(html.html)
    try:
        with open(fname, "w+", encoding="utf-8") as f:
            f.write(s)
    except Exception as e:
        raise Exception(f"Error in writing html to file : {e}")


def scrape_page(url: str) -> Tuple[int, Union[BeautifulSoup, None]]:
    try:
        page = requests.get(url)
        html = BeautifulSoup(page.content, "html.parser")
        return (page.status_code, html)
    except Exception as e:
        raise Exception(f"Error in scraping page {url} : {e}")


def get_content(page : BeautifulSoup, name : str) -> str :
    try : 
        main_article = page.select_one("article.content div.text")
        return main_article.text
    except Exception as e : 
        raise Exception(f"Error in getting main content of {str} : {e}")


def save_as_csv(
    data, fname: str, index: Optional[bool] = False, cnames: Optional[str] = None
) -> None:
    try:
        if not os.path.isdir("save_data") :
            os.mkdir("save_data")
        df = pd.DataFrame(data)
        if cnames:
            df.columns = cnames
        df.to_csv(f"save_data/{fname}", index=index)
        print(f"File saved to : save_data/{fname}")
    except Exception as e:
        raise Exception(f"Error in saving data as csv : {e}")


def scrape_tutorialspoint() -> None:
    try:
        p = 0
        f = 0
        data = []
        status, page = scrape_page(MAIN_URL)
        assert status == 200, f"Status {status}"

        links = page.select("ul.toc.chapters a")
        for i in links : 
            try :
                print(i.text)
                print(BASE_URL+i.get("href"))
            except : 
                f += 1
                print(f"Failure ---- Problem in getting content of sub page {sub_text}. Error : {e}")
                continue
        
        # save_as_csv(data, "tutorials_data.csv", cnames=["section", "url", "data"])
        print("\n===================================")
        print(f"Total : {p+f}\tPass : {p}\tFail : {f}")
    except Exception as e:
        print(f"Error in main : {e}")


if __name__ == "__main__":
    print("Scanning tutorialspoint starting... ")
    scrape_tutorialspoint()
