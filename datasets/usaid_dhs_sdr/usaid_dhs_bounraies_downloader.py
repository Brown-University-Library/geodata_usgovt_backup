# -*- coding: utf-8 -*-
"""
Download USAID DHS Country Boundaries
Frank Donnelly, Mar 20, 2025

Notes: 
1.   
2. Complex JS page, must use Selenium
3. Using Firefox on MS Windows
4. Read in list of countries to build links to iterate through
5. Best to run test first, then run entire program
6. Built in pauses to allow time for page to load and download files
7. Use browser.execute trick to prevent Firefox popup from blocking next download
8. Due to complexity just saving files - save web page and docs manually
9. Only DHS SDR page captured by script - other pages / files downloaded manually
"""

import os, time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import date

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", r"") # INSERT PATH HERE
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

test=False

url='https://spatialdata.dhsprogram.com/boundaries/#countryId={}&view=table'
baseurl='https://spatialdata.dhsprogram.com/boundaries/'
dataset='USAID DHS Spatial Data Repository'
page_title='Spatial Data Repository - Boundaries'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
country_file='dhs_ccode_bndy.csv'
today = str(date.today())

hardpath=r"" # INSERT PATH HERE
outfolder=os.path.join(hardpath,'downloaded-'+today)
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
    
countries=[]

with open(country_file, 'r') as reader:
    next(reader)  # skip the headers
    for record in csv.reader(reader):
        countries.append(record[0])

if test ==True:
    countries=countries[0:2]
else:
    pass        

i=0
for c in countries:
    browser=webdriver.Firefox(options=options)
    cpage=url.format(c)
    browser.get(cpage)
    browser.implicitly_wait(20)
    elems=browser.find_elements(By.CSS_SELECTOR,'.download-boundaries-img.download-boundaries--button')  
    for e in elems:
        browser.execute_script("arguments[0].click();", e)
        i=i+1
    time.sleep(20)
    browser.quit()

print('Finished downloading',i,'files from',dataset)
    
metafile = "_METADATA-{}.txt".format(today)
writefile=open(os.path.join(outfolder,metafile),'w')
writefile.write(dataset+'\n') 
writefile.write('{} files archived on {}\n'.format(i,today))
writefile.write('From webpage {}\n'.format(page_title)) 
writefile.write('At {}\n'.format(baseurl))  
writefile.write('By {}'.format(person))  
writefile.close() 