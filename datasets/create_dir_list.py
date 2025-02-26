# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:47:33 2025

@author: Frank Donnelly
"""

import os
from datetime import date
today = str(date.today())

writefile=open(os.path.join('file_list-{}.txt'.format(today)),'w')
writefile.write('File list for US Government Data Backup Project \n')
for path, dirs, files in os.walk('.'):
    writefile.write(path+'\n')
    for f in files:
        writefile.write('\t'+f+'\n')
writefile.close()    
