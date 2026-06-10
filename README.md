
<img width="170" align="right" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/USGS_logo_green.svg/500px-USGS_logo_green.svg.png"/>

# Metadata Wizard

>***Note about GitHub branches:*** *Version 2.2.0 contains updated Python libraries. These updates result in breaking changes for installed Metadata Wizard applications. As a result, current users should not pull updates using the in-app 'check for updates' feature. Instead, they should download the v2.2.0 installer from the GitHub Releases page: https://github.com/DOI-USGS/fort-pymdwizard/releases.*
>*To make sure existing installations don't inadvertently pull breaking changes, v2.2.0 is set up to pull updates from a new branch, ___'main-v2.2'___. All future updates will be published to this new branch or to later 'main' branches.*<br>
---
The USGS Metadata Wizard is a desktop application to create XML metadata records that describe data products. The tool creates metadata in the Content Standard for Digital Geospatial Metadata (CSDGM) format, as endorsed by the Federal Geographic Data Committee (FGDC).

Complete user documentation available [here](https://doi-usgs.github.io/fort-pymdwizard).

![Alt text](docs/img/screenshot.png?raw=true "Screen shot")

It provides a user-friendly and efficient environment for metadata creation, editing, preview, and validation.  Built-in tools facilitate and automate the creation of high quality metadata records.


* Auto-population of challenging metadata sections such as the spatial reference, 
spatial organization, and entity and attributes, based on information contained in
the data (CSV, Excel, Shapefiles, etc.)<br>

 ![Alt text](./docs/img/EA_screenshot.png?raw=true "Screen shot") 

* Auto-population of contact information for USGS affiliates, taxonomic information from ITIS, or keywords from USGS controlled vocabularies.<br>

 ![Alt text](docs/img/keywords_screenshot.png?raw=true "Screen shot") 
* Built-in FGDC validator that highlights any missing or error elements directly on the GUI and in a printable report suitable for metadata review.<br>

 ![Alt text](docs/img/error_screenshot.png?raw=true "Screen shot") 

* Copy/Paste or Drag-and-Drop of entire sections, subsections, or individual content
between different records or other tools including XML-Notepad and text editors.
* Built-in help documentation that guides users through common and detailed questions about metadata.


This project is modeled off of the original [Metadata Wizard](https://github.com/dignizio-usgs/MDWizard_Source), which was designed as a toolbox in ArcMap and required an ESRI installation.

Recommended Citation:
----------------

Talbert, C.B., Ignizio, D.A., Norkin, T., O'Donnell, M.S., and Enns, K.D., 2017, Metadata Wizard (ver. 2.2.0, June 2026): U.S. Geological Survey software release, https://doi.org/10.5066/F7V9870D.

Authors:
----------------

Colin B. Talbert -- https://orcid.org/0000-0002-9505-1876<br>
Drew A. Ignizio -- https://orcid.org/0000-0001-8054-5139<br>
Tamar Norkin -- https://orcid.org/0000-0003-0797-3940<br>
Michael S. O'Donnell -- https://orcid.org/0000-0002-3488-003X<br>
Kyle D. Enns -- https://orcid.org/0000-0001-7675-697X

Acknowledgements:
----------------
The Metadata Wizard was developed by the data management team at the USGS Fort Collins Science Center, with support from the USGS Science Analytics and Synthesis (SAS), and the USGS Community for Data Integration (CDI).<br><br>
Ongoing support provided by the USGS Science Analytics and Synthesis (SAS) branch<br>

Use of Artificial Intelligence:
----------------
Claude Code (Claude Sonnet 4.5) was used as an AI pair-programming assistant during application development. All code was reviewed, tested, and validated by the authors.

Disclaimer:
-----------

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

Any use of trade, product or firm names is for descriptive purposes only and does not imply endorsement by the U.S. Geological Survey.

Although this software product, for the most part, is in the public domain, the installers contain copyrighted material as noted in the file LICENSE.md. Permission to reproduce copyrighted items for other than personal use must be secured from the copyright owner.

Contact:
-----------
ask-sdm@usgs.gov

Software repositories:
-----------
Official source code: https://code.usgs.gov/usgs/fort-pymdwizard  
Mirrored into GitHub: https://github.com/usgs/fort-pymdwizard  
User documentation: https://doi-usgs.github.io/fort-pymdwizard/  
Examples of use in other scripts: https://github.com/DOI-USGS/fort-pymdwizard/tree/master/examples
