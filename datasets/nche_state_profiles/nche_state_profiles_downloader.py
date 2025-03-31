# -*- coding: utf-8 -*-
"""
Download NCHE State Profile Data
Frank Donnelly, Mar 29, 2025

Notes: 
1. Complex JS page, must use Selenium
2. Using Firefox on MS Windows
3. Assumes you ran the Print script first which created all the state folders
4. On each pass, cycle through drop down list and download reports to state folder
5. Reports for most recent years were not available, drop down yielded nothing
"""

import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep

url='https://profiles.nche.seiservices.com/StateProfile.aspx?StateID={}'

states={1: 'alaska', 2: 'alabama', 3: 'arkansas', 5: 'arizona',
        6: 'california', 7: 'colorado', 8: 'connecticut', 
        9: 'district_of_columbia', 10: 'delaware', 11: 'florida',
        13: 'georgia', 15: 'hawaii', 16: 'iowa', 17: 'idaho', 
        18: 'illinois', 19: 'indiana', 20: 'kansas', 21: 'kentucky',
        22: 'louisiana', 23: 'massachusetts', 24: 'maryland', 
        25: 'maine', 27: 'michigan', 28: 'minnesota', 29: 'missouri',
        31: 'mississippi', 32: 'montana', 33: 'north_carolina', 
        34: 'north_dakota', 35: 'nebraska', 36: 'new_hampshire', 
        37: 'new_jersey', 38: 'new_mexico', 39: 'nevada', 
        40: 'new_york', 41: 'ohio', 42: 'oklahoma', 43: 'oregon', 
        44: 'pennsylvania', 45: 'puerto_rico', 47: 'rhode_island', 
        48: 'south_carolina', 49: 'south_dakota', 50: 'tennessee', 
        51: 'texas', 52: 'utah', 53: 'virginia', 54: 'vermont', 
        56: 'washington', 57: 'west_virginia', 58: 'wisconsin', 
        59: 'wyoming', 60: 'bureau_of_indian_education'}

outfolder='downloaded-2025-03-29'

for k,v in states.items():
    statepath=os.path.join(outfolder,v)
    abspath=os.path.abspath(statepath)
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir",r"{}".format(abspath)) # INSERT PATH HERE
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    browser=webdriver.Firefox(options=options)
    page=url.format(k)
    browser.get(page) # Load page, wait to render
    browser.implicitly_wait(10)
    sleep(10)      
    dropdown = Select(browser.find_element(By.ID, "MainContent_ddlConsolidatedSPR"))
    options = dropdown.options # Get dropdown menu and list of options
    
    for index in range(1, len(options) - 1): # cycle through options, first one at 0 is blank      
        dropdown.select_by_index(index) # select option by index / order in options list
        sleep(5)
        # Find download button and hit it
        download = browser.find_element(By.ID, "MainContent_btndownload")
        browser.execute_script("arguments[0].click();", download)
        sleep(5)
        if len(browser.window_handles)>1: # Return to previous tab
            browser.switch_to.window(browser.window_handles[1])
        else: # Unless there is only one tab
            pass
        browser.get(page)
        browser.implicitly_wait(10)
        # Find the dropdown again for the next iteration
        dropdown = Select(browser.find_element(By.ID, "MainContent_ddlConsolidatedSPR"))
        sleep(5)
    print('Downloaded files for',v)
    browser.quit()
    

