#this scraper extracts all the data from flipkart's newest arrived phones page
#and also the data of phones by visiting each link recursively
from bs4 import BeautifulSoup
import requests
import pandas as pd
status = 200
mobilen = 0
pagen = 1
data = []
datap = []
datan = []
while status==200:
     page = requests.get('https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&page='+str(pagen))
     status = page.status_code
    
     html = BeautifulSoup(page.content,'html.parser')

     rprice  = html.select('div._1vC4OE._2rQ-NK')
     if(len(rprice)==0):
          break
     for i in rprice:
          datap.append(i.get_text()[1:])
          
     name  = html.select('div._3wU53n')
     if(len(name)==0):
          break
     for i in name:
          datan.append(i.get_text())
    
     #phone links
     links  = html.select('div._3O0U0u a._31qSD5')
     if(len(links)==0):
          break
    
     #exploring each link
     for a in links:
          #compiled link
          link_mobile = 'https://www.flipkart.com'+a['href']
          mobile = requests.get(link_mobile)
          mobhtml = BeautifulSoup(mobile.content,'html.parser')
          mobilen += 1
          rows = mobhtml.select('tr._3_6Uyw.row')
          datar = []
          if(len(rows)==0):
                break
        
          features=['Model Number','Model Name','Color','SIM Type','Hybrid Sim Slot','Touchscreen','OTG Compatible','Operating System','Processor Type','Processor Core','Primary Clock Speed','Display Size','Resolution','Resolution Type','Internal Storage','RAM','Primary Camera','Secondary Camera','Expandable Storage','Network Type','Bluetooth Support','Wi-Fi','Wi-Fi Hotspot','USB Connectivity','Battery Capacity','Battery Type','Width','Height','Depth','Weight']
          #piece wise extraction of features
          for i in features:
               found = False
               for j in rows:
                    cols =  j.select('td')
                    if cols[0].get_text()==i:
                         feat = cols[1].select('li')
                         found = True
                         datar.append(feat[0].get_text())
                         break
               if(found==False):
                    datar.append(float('NaN'))
          print('Mobiles : ',mobilen) 
          data.append(datar)
     print('Page ',pagen)

unified_data = []
for i in range(len(data)):
     unified_data.append([datan[i]])
     unified_data[i].extend(data[i])
     unified_data[i].append(datap[i])

dataframe = pd.DataFrame(unified_data,columns=['Name','Model Number','Model Name','Color','SIM Type','Hybrid Sim Slot','Touchscreen','OTG Compatible','Operating System','Processor Type','Processor Core','Primary Clock Speed','Display Size','Resolution','Resolution Type','Internal Storage','RAM','Primary Camera','Secondary Camera','Expandable Storage','Network Type','Bluetooth Support','Wi-Fi','Wi-Fi Hotspot','USB Connectivity','Battery Capacity','Battery Type','Width','Height','Depth','Weight','Price'])
dataframe.to_csv('Flipkart.csv')


