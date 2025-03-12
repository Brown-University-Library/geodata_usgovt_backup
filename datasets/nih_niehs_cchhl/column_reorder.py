# -*- coding: utf-8 -*-
"""
Frank Donnelly
Head of GIS and Data Services
Brown University Library

Change order and name of columns
NIEHS Climate Change and Human Health Literature Portal
Bibliographic database

March 11, 2025
"""

import pandas as pd
import sqlite3

cols={'reference_id':'reference_id',
      'reference_type':'reference_type',
      'reference_title':'title',
      'Author':'author',
      'year_published':'year_published',
      'book_title':'book_title',
      'Journal':'journal',
      'volume_detailed':'volume',
      'issue':'issue',
      'page_s':'pages',
      'Series_detailed':'series',
      'Editor':'editor',
      'publisher_detailed':'publisher',
      'place_published':'place_published',
      'conference':'conference',
      'geo':'geo',
      'geo_nonus':'geo_non_us',
      'Geographic_Location':'geographic_location_terms',
      'Geographic_Features':'geographic_feature_terms',
      'Model_Methodology':'model_methods_terms',
      'Model_Timescale':'model_timescale',
      'Climate_Change_and_Socioeconomic_Scenarios':'climate_socioecon_scenario_terms',
      'Exposure':'exposure_terms',
      'Health_Impact': 'health_impact_terms',
      'Special_Topic':'special_topic_terms',
      'Abstract': 'abstract',
      'Publisher1_URL':'publisher1_url',
      'Publisher2_URL':'publisher2_url',
      'PubMed_URL':'pubmed_url'
      }


df=pd.read_csv('cchhl.csv')

df_new=df[cols.keys()].rename(cols,axis=1)

df_new['abstract']=df_new['abstract'].str.strip()

df_new.to_csv('niehs_cchhlp.csv',sep=',',na_rep='',index=False)

conn = sqlite3.connect('niehs_cchhlp.sqlite')
df_new.to_sql('bibliography',conn,index=False)
conn.close()