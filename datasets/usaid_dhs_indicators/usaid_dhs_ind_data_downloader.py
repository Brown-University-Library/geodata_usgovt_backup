#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download USAID DHS Indicator Data
Frank Donnelly, Mar 24, 2025

Notes: 
1. Create a list of all surveys from the survey API
2. Cycle through each survey, and get national, subnational, and categorical summaries
3. Save these in a folder named for the survey
4. Max number of returned records is 5000 per page, have to cycle through each page
5. The indicators data is SUMMARY data for countries and subdivisions; microdata is
not publicly available
"""

import requests, os, json, gc
from datetime import date
from random import randint
import time

dataset='USAID DHS Indicators'
home_title='The DHS Program API'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
url='https://api.dhsprogram.com/'
today = str(date.today())

outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

# GET LIST OF ALL SURVEYS
surveys=[]    
survey_url='http://api.dhsprogram.com/rest/dhs/surveys'
response=requests.get(survey_url)
data=response.json()
for record in data['Data']:
    surveys.append(record['SurveyId'])

levels=['National','Subnational','Background']       
surl='http://api.dhsprogram.com/rest/dhs/v8/data?surveyIds={}&breakdown={}&page={}'
record_count={'Dataset':'Records'}

# RETRIEVE AND DOWNLOAD DATA
               
i = 0 
errors={}
for s in surveys: # for every survey
    for lev in levels: # for all three levels
        sdata=[]
        sfolder=os.path.join(outfolder,s)
        if not os.path.exists(sfolder):
            os.makedirs(sfolder)
        try:
            pnum=1
            response = requests.get(surl.format(s,lev,pnum))
            response.raise_for_status()
            data=response.json()
            data_flat=data['Data']
            t_pages=data['TotalPages']
            r_count=data['RecordCount']
            sdata.extend(data_flat)
            while t_pages>pnum: # Handles multiple pages
                pnum=pnum+1
                response = requests.get(surl.format(s,lev,pnum))
                response.raise_for_status()
                data=response.json()
                data_flat=data['Data']
                sdata.extend(data_flat)
            sfile='{}_{}.json'.format(s,lev)
            spath=os.path.join(sfolder,sfile)
            with open(spath, 'w') as jfile:
                json.dump(sdata, jfile, indent=4)
            i=i+1
            down_count=len(sdata)
            record_count[s+' '+lev]=down_count
            if down_count==r_count:    
                print('Downloaded',down_count,'records from',s,lev)
            else:
                print('MISMATCH in downloaded',down_count,'versus retrieved',r_count,'record count for',s,lev)
            del(sdata)
            gc.collect()           
        except requests.exceptions.RequestException as e:
            print('Could not retrieve',s,lev,'because of',e)
            errors[s+' '+lev]=e
    time.sleep(randint(10,20))

print('Finished downloading',i,'files from',url)

# WRITE METADATA

metafile = "_METADATA-{}.txt".format(today)
writefile=open(os.path.join(outfolder,metafile),'w')
writefile.write(dataset+'\n') 
writefile.write('{} data files archived on {}\n'.format(i,today))
writefile.write('From webpage {}\n'.format(home_title)) 
writefile.write('At {}\n'.format(url))  
writefile.write('By {}'.format(person))  
writefile.close() 

rfile="_RECORD_COUNT.csv"
with open(os.path.join(outfolder,rfile),'w') as writefile:
    for k,v in record_count.items():
        writefile.write('{},{}\n'.format(k,v))

efile = "_ERRORS-{}.txt".format(today)
epath=os.path.join(outfolder,efile)
if os.path.exists(efile):
    os.remove(efile)

if len(errors)>0:
    writefile=open(epath,'w')
    writefile.write('Download Errors for {}\n'.format(home_title))
    for ek,ev in errors.items():
        writefile.write('{}: {}\n'.format(ek,ev))
    writefile.close()