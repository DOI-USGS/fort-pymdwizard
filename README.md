[![Build Status](https://travis-ci.org/talbertc-usgs/fort-pymdwizard.svg?branch=master)](https://travis-ci.org/talbertc-usgs/fort-pymdwizard)
[![Hackage](https://coveralls.io/repos/github/talbertc-usgs/fort-pymdwizard/badge.svg?branch=master)](https://coveralls.io/github/talbertc-usgs/fort-pymdwizard?branch=master)

<img width="250" align="right" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/USGS_logo_green.svg/500px-USGS_logo_green.svg.png"/>



Metadata Wizard
===========================================================================================

The  is a useful tool designed to facilitate FGDC  
metadata creation for spatial and non-spatial data sets.  It is a cross-platform desktop application
built using an open-source Python architecture.  

Complete user documentation available [here](https://usgs.github.io/fort-pymdwizard)

![Alt text](docs/img/screenshot.png?raw=true "Screen shot")

It provides a pleasant and highly efficient environment for metadata creation, 
editing, preview, and validation.  Built in tools automate and facilitate the creation of high quality 
metadata records.


* Auto-population* of challenging sections such as the spatial reference, 
spatial organization, and entity and attribute based on information contained in
the data being documented (CSV, Excel, Shapefiles, etc.)
 ![Alt text](docs/img/EA_screenshot.png?raw=true "Screen shot") 

* Automate population of contact information for USGS affiliates, 
Taxonomic information from itis, or keywords from USGS controlled vocabularies
 ![Alt text](docs/img/keywords_screenshot.png?raw=true "Screen shot") 
* Built in FGDC validator which highlights any missing or error elements directly on the GUI and in a printable report suitable for metadata review.
 ![Alt text](docs/img/error_screenshot.png?raw=true "Screen shot") 
* Copy/Paste or Drag-and-Drop of entire sections, subsections, or individual content
between different records or other tools including XML-Notepad and text editors.
* Built in help documentation which guides users through common and detailed questions about metadata.


This project is modeled off of the original [Metadata Wizard](https://github.com/dignizio-usgs/MDWizard_Source), which was designed as a toolbox in ArcMap, and required an ESRI installation.



----
Disclaimer:
-----------

This software is preliminary or provisional and is subject to revision. It is
being provided to meet the need for timely best science. The software has not
received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the
functionality of the software and related material nor shall the fact of release
constitute any such warranty. The software is provided on the condition that
neither the USGS nor the U.S. Government shall be held liable for any damages
resulting from the authorized or unauthorized use of the software.

Although this software program has been used by the U.S. Geological Survey (USGS), no warranty, expressed or implied, is made by the USGS or the U.S. Government as to the accuracy and functioning of the program and related program material nor shall the fact of distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.