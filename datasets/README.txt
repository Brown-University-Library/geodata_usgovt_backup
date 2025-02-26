US FEDERAL GOVERNMENT DATASET BACK-UPS
Brown University Library
Frank Donnelly, Head of GIS & Data Services
-------------------------------------------

Each folder is named for an agency and dataset, and contains:

- A Python script that was written to download data
- Subfolder(s) containing datasets, date-stamped to indicate download date

Each download instance contains:

- Datasets, documentation, and summary reports hosted on a specific webpage
- _METADATA-datestamp.txt has basic information about the download
- _WEBPAGE-datestamp.html is a no-frills HTML copy of the page that was scraped
- _ERRORS-datestemp.txt if applicable, lists files not downloaded due to broken links

-------------------------------------------

MANIFEST = {
imls_mdf : IMLS Museum Data Files,
imls_pls : IMLS Public Library Survey,
imls_slaa : IMLS State Library Administrative Agency Survey,
irs_soi_eobmf : IRS SOI Exempt Organizations Business Master File Extract,
noaa_coast_slrviewer : NOAA Coast Sea Level Rise Viewer,
noaa_ncei_climate_glance : NOAA NCEI Climate at a Glance
}




