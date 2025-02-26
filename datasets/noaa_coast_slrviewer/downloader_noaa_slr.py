#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download NOAA Coast Sea Level Rise Viewer Data
Frank Donnelly, Feb 23 2025

Notes: 
1. Data is stored on multiple pages
2. Except for the wetlands page, each page has a text file with list of files to download
3. Some pages are further subdivided by state and must be iterated through
4. Must also capture extra documentation links embedded on the page 
5. A page with dataset updates must be captured separately
6. Subfolders are created to store data for each page (but not subdivided by state)
7. Metadata with item counts, webpages, and errors are stored in the subfolders
8. Wetlands page has no text file listing, uses relative links to zips stored in the page
9. Metadata from the home page not created from function as there is no data or file count
10. One of the state pages uses different abbreviations and is treated as exception
11. TEMPCOUNT variable lines in the downloads function can be uncommented for debugging
"""

import requests, os
from bs4 import BeautifulSoup as soup
from datetime import date

url='https://coast.noaa.gov/slrdata/index.html'
dataset='NOAA Coast Sea Level Rise Viewer'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
today = str(date.today())

outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)
    

url_update='https://coast.noaa.gov/slr/#/updates/data/'

urls_no_states={'https://coast.noaa.gov/slrdata/Ancillary/index.html':'https://coast.noaa.gov/slrdata/Ancillary/URLlist_Ancillary.txt',
                'https://coast.noaa.gov/slrdata/Ancillary/NOAA_OCM_SLR_MergedPolys_Shapefiles_0225/index.html':'https://coast.noaa.gov/slrdata/Ancillary/NOAA_OCM_SLR_MergedPolys_Shapefiles_0225/URLlist_NOAA_OCM_SLR_MergedPolys_Shapefiles_0225.txt',
                'https://coast.noaa.gov/slrdata/High_Tide_Flooding/index.html':'https://coast.noaa.gov/slrdata/High_Tide_Flooding/URLlist_High_Tide_Flooding.txt',
                'https://coast.noaa.gov/slrdata/Tidal_Surfaces/index.html':'https://coast.noaa.gov/slrdata/Tidal_Surfaces/URLlist_Tidal_Surfaces.txt'
                }

urls_states={'https://coast.noaa.gov/slrdata/DEMs/index.html':'https://coast.noaa.gov/slrdata/DEMs/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Depth_Rasters/index.html':'https://coast.noaa.gov/slrdata/Depth_Rasters/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Extent_Rasters/index.html':'https://coast.noaa.gov/slrdata/Extent_Rasters/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Mapping_Confidence/index.html':'https://coast.noaa.gov/slrdata/Mapping_Confidence/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Sea_Level_Rise_Vectors/index.html':'https://coast.noaa.gov/slrdata/Sea_Level_Rise_Vectors/{}/URLlist_{}.txt'
              }

urls_states={'https://coast.noaa.gov/slrdata/Depth_Rasters/index.html':'https://coast.noaa.gov/slrdata/Depth_Rasters/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Extent_Rasters/index.html':'https://coast.noaa.gov/slrdata/Extent_Rasters/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Mapping_Confidence/index.html':'https://coast.noaa.gov/slrdata/Mapping_Confidence/{}/URLlist_{}.txt',
              'https://coast.noaa.gov/slrdata/Sea_Level_Rise_Vectors/index.html':'https://coast.noaa.gov/slrdata/Sea_Level_Rise_Vectors/{}/URLlist_{}.txt'
              }

url_wetland='https://coastalimagery.blob.core.windows.net/ccap-landcover/CCAP_bulk_download/Sea_Level_Rise_Wetland_Impacts/index.html'

states=['AK','AL','AS','CA','CT','DC','DE','FL','GA','GU','HI','LA','MA','MD',
        'ME','MP','MS','NC','NH','NJ','NY','OR','PA','PR','RI','SC','TX','VA',
        'VI','WA']

states_alt=['AK','AL','AS','CA','CT','DC','DE','FL','GA','Guam','HI','LA','MA','MD',
        'ME','CNMI','MS','NC','NH','NJ','NY','OR','PA','PR','RI','SC','TX','VA',
        'USVI','WA']
  
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

# SAVE UPDATES

webpage,page_title,links=page_scrape(url_update)
subpath=make_subfolder(os.path.split(url_update)[0],outfolder)
save_page(url,subpath,webpage)

all_links=[]

# SAVE DATA NOT SUBDIVIDED BY STATE

# for k,v in urls_no_states.items():
#     webpage,page_title,links=page_scrape(k)
#     subpath=make_subfolder(k,outfolder)
#     save_page(k,subpath,webpage)
#     datalinks=create_filelist(v)
#     extralinks=get_other_links(links,'.pdf')
#     if len(extralinks) > 1:
#         datalinks.extend(extralinks)
#     counter,errors=download_data(datalinks,subpath,page_title)
#     write_metadata(dataset,person,page_title,k,counter,errors,subpath)

#     all_links.extend(datalinks)
    
# SAVE DATA SUBDIVIDED BY STATE

for k,v in urls_states.items():
    webpage,page_title,links=page_scrape(k)
    subpath=make_subfolder(k,outfolder)
    save_page(k,subpath,webpage)
    if k=='https://coast.noaa.gov/slrdata/Mapping_Confidence/index.html':
        slist=states_alt
    else:
        slist=states
    statelinks=[]
    for s in slist:
        slink=v.format(s,s)
        datalinks=create_filelist(slink)
        statelinks.extend(datalinks)
    extralinks=get_other_links(links,'.pdf')
    if len(extralinks)>0:
        statelinks.extend(extralinks)   
    counter,errors=download_data(statelinks,subpath,page_title)
    write_metadata(dataset,person,page_title,k,counter,errors,subpath)

    all_links.extend(statelinks)  

# SAVE DATA FOR WETLANDS

webpage,page_title,links=page_scrape(url_wetland)
subpath=make_subfolder(url_wetland,outfolder)
save_page(url_wetland,subpath,webpage)
relativelinks=get_other_links(links,'.zip')
rootpath=os.path.split(url_wetland)[0]
datalinks=[]
for r in relativelinks:
    abslink=os.path.join(rootpath,r)
    datalinks.append(abslink)
counter,errors=download_data(datalinks,subpath,page_title)
write_metadata(dataset,person,page_title,url_wetland,counter,errors,subpath)

all_links.extend(datalinks)

print('FINISHED DOWNLOADING DATA FOR',dataset)