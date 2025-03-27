#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create CSV Files for USAID DHS Indicators
Frank Donnelly, Mar 24, 2025

Notes: 
1. Assumes that the docs and data download programs have been run first
2. Converts each json file to a csv
"""

import os,pandas as pd

datapath=os.path.join('downloaded-2025-03-24')

i=0
for path,folders,files in os.walk(datapath):
    for fname in files:
        if fname.endswith('.json'):
            jfile=os.path.join(path,fname)
            jdf=pd.read_json(jfile)
            cfile=fname.split('.')[0]+'.csv'
            cpath=os.path.join(path,cfile)
            jdf.to_csv(cpath,index=False)
            i=i+1
    print('Checked',path)
print ('Created',i,'CSV files')