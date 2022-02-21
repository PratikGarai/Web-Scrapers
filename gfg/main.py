from bs4 import BeautifulSoup
import requests
import time
from typing import Optional, Tuple, Union
import pandas as pd
import os


MAIN_URL = "https://www.geeksforgeeks.org/python-programming-language/"
SECTIONS = [
    "Basics",
    "io",
    "Data Types",
    "Variables",
    "Operators",
    "Control Flow",
    "Functions",
    "Object Oriented Concepts",
    "Exception Handling",
    "Python Collections",
    "Django tutorial",
    "Data Analysis",
    "Numpy",
    "Pandas",
    "Machine Learning with Python",
    "Python GUI",
    "Modules in Python",
    "WorkingWithDatabase",
    "Misc",
    "Applications and Projects",
]


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


def scrape_gfg() -> None:
    try:
        p = 0
        f = 0
        data = []
        status, page = scrape_page(MAIN_URL)
        assert status == 200, f"Status {status}"
        for section in SECTIONS:
            links = page.select(f"div.{process_class_name(section)} a")
            for link in links : 
                try : 
                    sub_text = link.text
                    sub_url = link.attrs['href']
                    sub_status, sub_page = scrape_page(sub_url)
                    if sub_status!=200 :
                        f += 1
                        print(f"Failure ---- Problem scraping sub page {sub_text}. Status : {sub_status}")
                        continue
                    data.append((section, sub_text, sub_url, get_content(sub_page, sub_text)))
                except Exception as e : 
                    f += 1
                    print(f"Failure ---- Problem in getting content of sub page {sub_text}. Error : {e}")
                    continue
                p += 1
                print(f"Success ---- Scraped page {sub_text}")
                time.sleep(0.5) # avoid ddos ban
        save_as_csv(data, "gfg_data.csv", cnames=["section", "subsection", "url", "data"])
        print("\n===================================")
        print(f"Total : {p+f}\tPass : {p}\tFail : {f}")
    except Exception as e:
        print(f"Error in main : {e}")


if __name__ == "__main__":
    print("Scanning gfg starting... ")
    scrape_gfg()
