#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download USAID DHS IDocumentation for Indicators
Frank Donnelly, Mar 24, 2025

Notes: 
1. Assumes that the docs and data download programs have been run first
2. Create a list of all publications from the survey API
3. Match the survey ID number of a pub with the survey's folder ID (which contains its data)
4. If there is no matching survey, put pubs in special folder
"""

import requests, os

outfolder='downloaded-2025-03-24'

nodatafolder=os.path.join(outfolder,'PUBS_NODATA')
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

# GET LIST OF ALL SURVEYS
pubs={}   
pub_url='http://api.dhsprogram.com/rest/dhs/publications'
response=requests.get(pub_url)
data=response.json()
for record in data['Data']:
    pubs[record['PublicationURL']]=record['SurveyId']

i=0   
for k,v in pubs.items():
    spath=os.path.join(outfolder,v)
    if os.path.isdir(spath) is True:
        try:
            with requests.get(k, stream=True) as response:
                response.raise_for_status()
                fname=os.path.split(k)[1]
                filepath=os.path.join(spath,fname)
                with open(filepath, 'wb') as writefile:
                    for chunk in response.iter_content(chunk_size=10000000):
                        writefile.write(chunk)
            i=i+1
            print('Downloaded',fname, v)
        except requests.exceptions.RequestException as e:
            print('Could not retrieve',fname,'because of',e)
    else:
        pubfolder=os.path.join(nodatafolder,v)
        if not os.path.exists(pubfolder):
            os.makedirs(pubfolder)
        try:
            with requests.get(k, stream=True) as response:
                response.raise_for_status()
                fname=os.path.split(k)[1]
                filepath=os.path.join(pubfolder,fname)
                with open(filepath, 'wb') as writefile:
                    for chunk in response.iter_content(chunk_size=10000000):
                        writefile.write(chunk)
            i=i+1
            print('Downloaded pub to No Data folder',fname, v)
        except requests.exceptions.RequestException as e:
            print('Could not retrieve',fname,'because of',e)
            
print('Finished downloading',i,'documents.')

    