#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download NOAA NCEI Climate at a Glance
Frank Donnelly, Feb 5, 2025

Notes:
1. Links to data are saved in a single table
2. Download all links from that table
3. Omit a few links that contain odd characters
4. Links are relative and must be reconstructed
"""

import requests, os
from bs4 import BeautifulSoup as soup
from datetime import date

url='https://www.ncei.noaa.gov/pub/data/cirs/climdiv/'
dataset='NOAA NCEI Climate at a Glance'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
today = str(date.today())

outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

# SCRAPE

webpage=requests.get(url).content
soup_page=soup(webpage,'html.parser')
page_title = soup_page.title.text
container=soup_page.find('table') # all links to data files are in a table
links=container.findAll('a') # these are relative links, just the filenames

datalinks={}

for lnk in links:
    if not lnk.attrs['href'].startswith(('?','/')):
        datalinks[lnk.attrs['href']]=url+lnk.attrs['href']

# DOWNLOAD DATA
        
i = 0
errors={}
for k,v in datalinks.items():
    try:
        response = requests.get(v)
        response.raise_for_status()
        datafile = open(os.path.join(outfolder,k),'wb')
        datafile.write(response.content)
        datafile.close()
        i=i+1
        print('Downloaded',k)
    except requests.exceptions.RequestException as e:
        print('Could not retrieve',k,'because of',e)
        errors[k]:e
print('Finished downloading',i,'files from',page_title)

# WRITE WEBPAGE & METADATA

webfile = '_WEBPAGE-{}.html'.format(today)
writefile=open(os.path.join(outfolder,webfile),'wb')
writefile.write(webpage)
writefile.close()
   
metafile = "_METADATA-{}.txt".format(today)
writefile=open(os.path.join(outfolder,metafile),'w')
writefile.write(dataset+'\n') 
writefile.write('{} files archived on {}\n'.format(i,today))
writefile.write('From webpage {}\n'.format(page_title)) 
writefile.write('At {}\n'.format(url))  
writefile.write('By {}'.format(person))  
writefile.close() 

efile = "_ERRORS-{}.txt".format(today)
epath=os.path.join(outfolder,efile)
if os.path.exists(efile):
    os.remove(efile)

if len(errors)>0:
    writefile=open(epath,'w')
    writefile.write('Download Errors for {}\n'.format(page_title))
    for ek,ev in errors.items():
        writefile.write('{}: {}\n'.format(ek,ev))
    writefile.close()