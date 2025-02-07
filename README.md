# US Federal Government Data Backup

This repo hosts Python scripts that use the Beautiful Soup and Requests modules to create back-ups of specific US federal government datasets (which are in the public domain). The actual datasets are not stored here, but are hosted in a public [Globus](https://www.globus.org/get-started) guest collection:

BrownU_Library_PUBL_usgovdata_backup

You can download and install [Globus Connect Personal](https://www.globus.org/globus-connect-personal) to create an endpoint on your machine, connect to this collection, and then [transfer the datasets](https://docs.globus.org/guides/tutorials/manage-files/transfer-files/) in whole or part. Alternatively, these back-ups are also being shared with ICPSR to host on [DataLumos](https://www.datalumos.org/datalumos/).

Each folder is named for an agency and dataset, and contain:

- A Python script that was written to download data
- Subfolder(s) containing datasets, date-stamped to indicate download date

Each download instance contains:

- Datasets, documentation, and summary reports hosted on a specific webpage
- _METADATA-datestamp.txt has basic information about the download
- _WEBPAGE-datestamp.html is a no-frills HTML copy of the page that was scraped
- _ERRORS-datestemp.txt if applicable, lists files not downloaded due to broken links

See the [README.txt](https://github.com/Brown-University-Library/geodata_usgovt_backup/blob/main/datasets/README.txt) doc to correlate folder names with the names of datasets that were downloaded
