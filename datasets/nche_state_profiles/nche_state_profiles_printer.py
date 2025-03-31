# -*- coding: utf-8 -*-
"""
Print NCHE State Profiles
Frank Donnelly, Mar 29, 2025

Notes: 
1. Complex JS page, must use Selenium
2. Using Firefox on MS Windows
3. Ran a block to get unique page IDs for each state to create a list
4. On each pass, used soup to extract state name from each page
5. Creates a folder for each state
6. Cycles through pages, hits print button, user must manually save each page as PDF
7. Kept default name of each PDF, but saved in the appropriate state folder
8. Dictionary of IDs and state names was carried over into downloader script
9. The national page and funding allocation sheets were downloaded manually
10. Number of records in the metadata file was added manually
"""

import requests, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import date
from time import sleep
from bs4 import BeautifulSoup as soup

url='https://profiles.nche.seiservices.com/StateProfile.aspx?StateID={}'
dataurl='https://profiles.nche.seiservices.com/ConsolidatedStateProfile.aspx'
dataset='NCHE State Profiles'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'

today = str(date.today())
outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

pids=[1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 18, 19, 20, 
     21, 22, 23, 24, 25, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 
     38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 51, 52, 53, 
     54, 56, 57, 58, 59, 60]

# THIS BLOCK WAS USED ONCE TO OBTAIN VALID PAGE IDS
# pids=[]
# for i in range (1,61):
#     try:
#         response=requests.get(url.format(i))
#         print(i,response.status_code)
#         if response.status_code==200:
#             pids.append(i)
#         else:
#             pass

states={}
for p in pids:
    try: # Soup to get name of state from h1 to create folder
        webpage=requests.get(url.format(p)).content
        soup_page=soup(webpage,'html.parser')
        page_title = soup_page.title.text
        container=soup_page.find('div', class_='col-1-1') # has header with state name
        header=container.find('h1').text # state name
        state=header.lower().replace(" ","_")
        states[p]=state
        statepath=os.path.join(outfolder,state)
        if not os.path.exists(statepath):
            os.makedirs(statepath)
        abspath=os.path.abspath(statepath)
   
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir",r"{}".format(abspath))
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        browser=webdriver.Firefox(options=options)
        page=url.format(p)
        browser.get(page)
        browser.implicitly_wait(10)
        sleep(10)
        # Find the print button and click it
        pbutton = browser.find_element(By.ID, "MainContent_btnConvertToPDF1")
        browser.execute_script("arguments[0].click();", pbutton) 
        browser.implicitly_wait(10)
        browser.close()
    except requests.exceptions.RequestException as e:
        print('Could not retrieve page',p,'because of',e)
        
metafile = "_METADATA-{}.txt".format(today)
writefile=open(os.path.join(outfolder,metafile),'w')
writefile.write(dataset+'\n') 
writefile.write('X files archived on {}\n'.format(today))
writefile.write('From webpage {}\n'.format(page_title)) 
writefile.write('At {}\n'.format(dataurl))  
writefile.write('By {}'.format(person))  
writefile.close() 
print("Finished")