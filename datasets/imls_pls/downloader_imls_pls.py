#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download IMLS Public Library Survey
Frank Donnelly, Feb 5, 2025

Notes: 
1. Links to data are saved in a div along with links to a lot of unrelated stuff
2. Just pull links that end with file extensions
3. Links to files are relative and stored in location that differs from the url
4. Links must be reconstructed to point to correct source
5. There are a couple of absolute links that must be handled separately
6. A separate loop captures some publications stored on separate pages
"""

import requests, os
from bs4 import BeautifulSoup as soup
from datetime import date

url='https://www.imls.gov/research-evaluation/surveys/public-libraries-survey-pls'
dataurl='https://www.imls.gov' # root location where files are stored
dataset='IMLS Public Library Survey'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
today = str(date.today())

outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
    
# SCRAPE

webpage=requests.get(url).content
soup_page=soup(webpage,'html.parser')
page_title = soup_page.title.text
container=soup_page.find(('div', {'class': 'usa-main-container'})) # all links to data files are in this div
links=container.findAll('a') # all the links, mix of data and non-data

datalinks={}
pub_urls=[]

for lnk in links:
    if lnk.attrs['href'].endswith(('.pdf','.zip','.xlsx')):
        if lnk.attrs['href'].startswith('/sites/'): # relative links
            filename=lnk.attrs['href'].split('/')[-1]
            datalinks[filename]=dataurl+lnk.attrs['href']
        else:
            filename=lnk.attrs['href'].split('/')[-1] # absolute links
            datalinks[filename]=lnk.attrs['href']
    elif lnk.attrs['href'].startswith('/publications/'): # publications with no direct download
        pub_urls.append(dataurl+lnk.attrs['href'])

pubcount=0        
for p in pub_urls: # This loop gets the links for publications on other pages
    pubpage=requests.get(p).content
    soup_pubs=soup(pubpage,'html.parser')
    pubcontainer=soup_pubs.find('table')
    publink=pubcontainer.findAll('a')
    for pl in publink:
        filename=pl.attrs['href'].split('/')[-1]
        datalinks[filename]=dataurl+pl.attrs['href']
        pubcount=pubcount+1
print('Got {} additional links for {} publications stored on different pages \n'.format(pubcount,len(pub_urls)))

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
        errors[k]=e

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