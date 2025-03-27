#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download USAID DHS Indicator Documentation
Frank Donnelly, Mar 24, 2025

Notes: 
1. Save the homepage
2. Save all of the metadata about the indicators as JSON
3. Save codebook field list for each metadata collection as html
4. Save some PDF files that describe how the survey data is collected
6. Save the geometry data - more than 1 page is returned (max 5000 records), so must iterate
7. The indicators data is SUMMARY data for countries and subdivisions; microdata is
not publicly available
"""

import requests, os, json
from datetime import date

dataset='USAID DHS Indicators'
home_title='The DHS Program API'
person='Frank Donnelly, Head of GIS & Data Services, Brown University Library'
today = str(date.today())

outfolder='downloaded-'+today
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

intro_page='https://api.dhsprogram.com/'

fields_url='http://api.dhsprogram.com/rest/dhs/data/fields'
citation_url='http://api.dhsprogram.com/rest/dhs/info/citation'

doc_urls=['http://api.dhsprogram.com/rest/dhs/indicators',
          'http://api.dhsprogram.com/rest/dhs/countries',
          'http://api.dhsprogram.com/rest/dhs/surveys',
          'http://api.dhsprogram.com/rest/dhs/surveycharacteristics',
          'http://api.dhsprogram.com/rest/dhs/publications',
          'http://api.dhsprogram.com/rest/dhs/datasets',
          'http://api.dhsprogram.com/rest/dhs/tags',
          'http://api.dhsprogram.com/rest/dhs/dataupdates',
          'http://api.dhsprogram.com/rest/dhs/uiupdates',
          'http://api.dhsprogram.com/rest/dhs/info']

pdfs=['https://www.dhsprogram.com/pubs/pdf/DHSG1/Guide_to_DHS_Statistics_DHS-8.pdf',
      'https://www.dhsprogram.com/pubs/pdf/DHSG1/Guide_to_DHS_Statistics_DHS-7_v2.pdf',
      'https://www.dhsprogram.com/pubs/pdf/DHSG1/Guide_to_DHS_Statistics_DHS-7.pdf',
      'https://www.dhsprogram.com/pubs/pdf/DHSG1/Guide_to_DHS_Statistics_29Oct2012_DHSG1.pdf']

geo_url='http://api.dhsprogram.com/rest/dhs/geometry'

def write_html(inpage,outfolder,outfile):
    page=requests.get(inpage).content
    writefile=open(os.path.join(outfolder,outfile),'wb')
    writefile.write(page)
    writefile.close()
    
docpath=os.path.join(outfolder,'_CODEBOOKS')
if not os.path.exists(docpath):
    os.makedirs(docpath)
    
write_html(intro_page,outfolder,'_WEBPAGE-{}.html'.format(today))
write_html(citation_url+'?f=html',outfolder,'info_citation.html')
write_html(fields_url,docpath,'data_fields.html')    

for d in doc_urls:
    response=requests.get(d)
    metadata=response.json()
    data=metadata['Data']
    fname=d.split('/')[-1]+'.json'
    outpath=os.path.join(docpath,fname)
    with open(outpath, 'w') as jfile:
        json.dump(data, jfile, indent=4)
    table=d.split('/')[-1]+'_fields.html'
    write_html(d+'/fields',docpath,table)
    
for p in pdfs:
    response = requests.get(p)
    pname=p.split('/')[-1]
    datafile = open(os.path.join(docpath,pname),'wb')
    datafile.write(response.content)
    datafile.close()

gdata=[]
pnum=1    
response=requests.get(geo_url+'?page={}'.format(pnum))
geodata=response.json()
geodata_flat=geodata['Data']
t_pages=geodata['TotalPages']
gdata.extend(geodata_flat)
while t_pages>pnum: # Handles multiple pages
    pnum=pnum+1
    response = requests.get(geo_url+'?page={}'.format(pnum))
    geodata=response.json()
    geodata_flat=geodata['Data']
    gdata.extend(geodata_flat)
gname=geo_url.split('/')[-1]+'.json'
gfile=os.path.join(docpath,gname)
with open(gfile, 'w') as jfile:
    json.dump(gdata, jfile, indent=4)
gtable=geo_url.split('/')[-1]+'_fields.html'
write_html(geo_url+'/fields',docpath,gtable)

print("Finished downloading documentation") 