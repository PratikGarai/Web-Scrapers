# This program scrapes and extracts data of all the phones listed on the URL given below and 
# store them as a table
URL = 'https://gadgets.ndtv.com/mobiles/best-phones-1'
from bs4 import BeautifulSoup
import requests
page  = requests.get(URL)
html = BeautifulSoup(page.content,'html.parser')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome()
driver.get(URL)
driver.implicitly_wait(100)
for i in range(2,100):
    num= driver.find_element_by_id('page_'+str(i))
    if(num==None):
        break
    num.click()
links  = driver.find_elements_by_class_name('rvw-title')
import pandas as pd
status = 200
mobilen = 0
pagen = 1
data = []
datap = []
datan = []
count = 0
def getter(iter1):
    global count
    page = requests.get(iter1)
    status = page.status_code
    if(status!=200):
        return
    html = BeautifulSoup(page.content,'html.parser')

    prc_comp = html.select("div._trtwgt a")
    if(len(prc_comp)==0):
        datap.append(float('NaN'))
    else:
        datap.append(prc_comp[0].get_text())

    datan.append(html.select("div._thd h1")[0].get_text().strip())
    rows = html.select("div._gry-bg._spctbl._ovfhide tr")
    features = ['Brand','Model','Release date','Form factor','Body type','Dimensions (mm)','Weight (g)','Battery capacity (mAh)','Colours','Screen size (inches)','Touchscreen','Resolution','Aspect ratio','Processor','Processor make','RAM','Internal storage','Rear camera','Front camera','Operating system','Wi-Fi','Bluetooth','GPS','Number of SIMs','2G','3G','4G','4G/ LTE']


    #for iter2 in rows:
    #      print(iter2.select("td")[0].get_text())

    data.append([])
    for iter3 in features:
        found  = False
        for iter4 in rows:
            if(iter4.select("td")[0].get_text().strip()==iter3):
                data[count].append(iter4.select("td")[1].get_text().strip())
                found = True
                break
        if found == False:
            data[count].append(float('NaN'))
    count += 1
    # print(count)
for i in links:
    getter(i.get_attribute("href"))
unified_data = []
c = 0
for i in range(len(data)):
    if(datap[i] == datap[i]):
        unified_data.append([datan[i]])
        unified_data[c].extend(data[i])
        unified_data[c].append(datap[i])
        c+=1
dataframe = pd.DataFrame(unified_data,columns=['Name','Brand','Model','Release date','Form factor','Body type','Dimensions (mm)','Weight (g)','Battery capacity (mAh)','Colours','Screen size (inches)','Touchscreen','Resolution','Aspect ratio','Processor','Processor make','RAM','Internal storage','Rear camera','Front camera','Operating system','Wi-Fi','Bluetooth','GPS','Number of SIMs','2G','3G','4G','4G/ LTE','Price'])
dataframe.to_csv('ndtv_raw.csv')
