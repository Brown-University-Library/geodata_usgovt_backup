# -*- coding: utf-8 -*-
"""
Change File Name of NCHE State Profiles
Frank Donnelly, Mar 29, 2025

Notes: 
1. Assumes you ran the Print script first where all the reports were printed
2. Walks through each state folder, changes generic name of printed page,
adds the name of the state as a prefix
3. Subsequently realized profile gets mixed in with downloaded reports,
moved profile into dedicated folder within each state subfolder
"""
# import os
# datapath='downloaded-2025-03-29'
# for path,folders,files in os.walk(datapath):
#     for fname in files:
#         print(fname)
#         if fname=='National Center for Homeless Education (NCHE).pdf':
#             fold=os.path.basename(path)
#             old_file=os.path.join(path,fname)
#             new_file=os.path.join(path,fold+'_'+fname)
#             os.rename(old_file,new_file)
#             print('Renamed',fold+'_'+fname)

import os
datapath='downloaded-2025-03-29'
for path,folders,files in os.walk(datapath):
    for fname in files:
        if fname.endswith('(NCHE).pdf'):
            ppath=os.path.join(path,'profile')
            if not os.path.exists(ppath):
                os.makedirs(ppath)
            old_file=os.path.join(path,fname)
            new_file=os.path.join(ppath,fname)
            os.rename(old_file,new_file)
            print('Moved',new_file)