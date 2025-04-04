# US Federal Government Data Backup

This repo hosts scripts (Python, R, others) used to create back-ups of specific US federal government datasets (which are in the public domain). The actual datasets (with the exception of imls_mdf, which is included as an example) are NOT stored in this repo, but are hosted in a public [Globus](https://www.globus.org/get-started) guest collection:

**BrownU_Library_PUBL_usgovdata_backup**

For institutions and organizations that want a copy of the archive, you can download and install [Globus Connect Personal](https://www.globus.org/globus-connect-personal) to create an endpoint on your machine, connect to this collection, and then [transfer the datasets](https://docs.globus.org/guides/tutorials/manage-files/transfer-files/) in whole or part. Alternatively, these back-ups are also being shared with ICPSR, and eventually will be hosted on [DataLumos](https://www.datalumos.org/datalumos/) for easier end-user access.

Each folder is named for an agency and dataset, and contain:

- A script that was written to download data
- Subfolder(s) containing datasets, date-stamped to indicate download date

Most download instances contain:

- Datasets, documentation, and summary reports hosted on a specific webpage
- _METADATA-datestamp.txt has basic information about the download
- _WEBPAGE-datestamp.html is a no-frills HTML copy of the page that was scraped
- _ERRORS-datestemp.txt if applicable, lists files not downloaded due to broken links

See the [README.txt](https://github.com/Brown-University-Library/geodata_usgovt_backup/blob/main/datasets/README.txt) doc to correlate folder names with the names of datasets that were downloaded
