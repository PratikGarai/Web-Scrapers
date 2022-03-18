from bs4 import BeautifulSoup
import requests

r = requests.get(
    "https://www.tutorialspoint.com/machine_learning/deep_machine_learning.htm")
html = BeautifulSoup(r.content, "html.parser")

paras = html.select(
    ".tutorial-content > p, .tutorial-content > h1, .tutorial-content > h2, .tutorial-content > h3")

arr = []
content = ""
for i in paras:
    if i.name == "p":
        content += i.text+"\n"
    else:
        arr.append(content)
        content = ""
        content += i.text+"\n\n"
for i in arr:
    print(i)
    print("\n-----------------\n\n")
