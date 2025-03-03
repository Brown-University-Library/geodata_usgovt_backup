#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download NOAA Coast Lake Level Viewer Data
Frank Donnelly, Mar 1 2025

Notes: 
1. Documentation for this data CANNOT be downloaded programatically, and is captured manually
2. Data is stored on multiple pages
3. Each page has a text file with list of files to download
4. Some pages are further subdivided by lakes and must be iterated through
5. Must also capture extra documentation links embedded on the page 
6. Subfolders are created to store data for each page (but not subdivided by lakes)
7. Metadata with item counts, webpages, and errors are stored in the subfolders
8. Metadata from the home page not created from function as there is no data or file count
9. TEMPCOUNT variable lines in the downloads function can be uncommented for debugging
"""

import requests, os
from bs4 import BeautifulSoup as soup
from datetime import date

url='https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/index.html'
dataset='NOAA Coast Lake Level Viewer'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
today = str(date.today())

outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
    
urls_no_lakes={'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/DEMs/index.html':'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/DEMs/URLlist_DEMs.txt',
              'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/Lake_Level_Vectors/index.html':'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/Lake_Level_Vectors/URLlist_Lake_Level_Vectors.txt' }

urls_lakes={'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/Depth_Rasters/index.html':'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/Depth_Rasters/{}/URLlist_{}.txt',
            'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/Extent_Rasters/index.html':'https://chs.coast.noaa.gov/htdata/Inundation/GreatLakes/BulkDownload/Extent_Rasters/{}/URLlist_{}.txt'}

lakes=['Erie','Huron1','Huron2','Huron3','Michigan1','Michigan2','Michigan3',
       'Michigan4','Michigan5','Michigan6','Michigan7','Michigan8','Ontario',
       'St_Clair','Superior1','Superior2','Superior3','Superior4','Superior5',
       'Superior6','Superior7']
 
# SCRAPE

def create_filelist(filepage):
    'Takes list of files in text file pages and saves them in a list'
    response = requests.get(filepage)
    filelist = response.text.split('\n')
    if filelist[-1]=="":
        del filelist[-1]
    return filelist

def get_other_links(extra_links,fileformat): 
    'Grabs other files on a page outside the text file listing'
    other_links=[]
    for lnk in extra_links:
        if 'href' in lnk.attrs:
            if lnk.attrs['href'].endswith(fileformat):
                other_links.append(lnk.attrs['href'])
    return other_links
    
def download_data(datalinks,outpath,page_title):
    'Downloads data'
    TESTCOUNT=0
    i = 0 
    errors={}
    for d in datalinks:
        try:
            with requests.get(d, stream=True) as response:
                response.raise_for_status()
                fname=os.path.split(d)[1]
                filepath=os.path.join(outpath,fname)
                with open(filepath, 'wb') as writefile:
                    for chunk in response.iter_content(chunk_size=10000000):
                        writefile.write(chunk)
            i=i+1
            TESTCOUNT=TESTCOUNT+1
            print('Downloaded',fname)
        except requests.exceptions.RequestException as e:
            print('Could not retrieve',d,'because of',e)
            errors[d]=e
        finally:
            if TESTCOUNT==2:
                break
    print('Finished downloading',i,'files from',page_title)
    return i, errors

def make_subfolder(url,downfolder):
    'Creates subfolders to mirror whats on the website'
    subfolder=url.split('/')[-2]
    newpath=os.path.join(downfolder,subfolder)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath
    
def page_scrape(url):
    'Initial page scrape, to save the page and non-text file links'
    webpage=requests.get(url).content
    soup_page=soup(webpage,'html.parser')
    page_title = soup_page.title.text
    container=soup_page.find('body')
    links=container.findAll('a')
    return webpage,page_title,links

def save_page(url,path,webpage):
    'Saves the page as plain html'
    webfile = '_WEBPAGE-{}.html'.format(today)
    writefile=open(os.path.join(path,webfile),'wb')
    writefile.write(webpage)
    writefile.close()
    
def write_metadata(dataset,person,page_title,url,counter,errors,outpath):
    'Writes metadata files and error lists'
    metafile = "_METADATA-{}.txt".format(today)
    writefile=open(os.path.join(outpath,metafile),'w')
    writefile.write(dataset+'\n') 
    writefile.write('{} files archived on {}\n'.format(counter,today))
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
    
# SAVE HOME PAGE

webpage,home_title,links=page_scrape(url)
save_page(url,outfolder,webpage)

metafile = "_METADATA-{}.txt".format(today)
writefile=open(os.path.join(outfolder,metafile),'w')
writefile.write(dataset+'\n') 
writefile.write('See individual subfolders for number of files archived on {}\n'.format(today))
writefile.write('From webpage {}\n'.format(home_title)) 
writefile.write('At {}\n'.format(url))  
writefile.write('By {}'.format(person))  
writefile.close() 

all_links=[]
    
# SAVE DATA NOT SUBDIVIDED BY LAKES

for k,v in urls_no_lakes.items():
    webpage,page_title,links=page_scrape(k)
    subpath=make_subfolder(k,outfolder)
    save_page(k,subpath,webpage)
    datalinks=create_filelist(v)
    extralinks=get_other_links(links,'.pdf')
    if len(extralinks) > 1:
        datalinks.extend(extralinks)
    counter,errors=download_data(datalinks,subpath,page_title)
    write_metadata(dataset,person,page_title,k,counter,errors,subpath)

    all_links.extend(datalinks)

# SAVE DATA SUBDIVIDED BY LAKES

for k,v in urls_lakes.items():
    webpage,page_title,links=page_scrape(k)
    subpath=make_subfolder(k,outfolder)
    save_page(k,subpath,webpage)
    lakelinks=[]
    for lk in lakes:
        lklink=v.format(lk,lk)
        datalinks=create_filelist(lklink)
        lakelinks.extend(datalinks)
    extralinks=get_other_links(links,'.pdf')
    if len(extralinks)>0:
        lakelinks.extend(extralinks)   
    counter,errors=download_data(lakelinks,subpath,page_title)
    write_metadata(dataset,person,page_title,k,counter,errors,subpath)

    all_links.extend(lakelinks) 

print('FINISHED DOWNLOADING DATA FOR',dataset)