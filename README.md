[![Build Status](https://travis-ci.org/talbertc-usgs/pymdwizard.svg?branch=master)](https://travis-ci.org/talbertc-usgs/pymdwizard)
[![Hackage](https://coveralls.io/repos/github/talbertc-usgs/pymdwizard/badge.svg?branch=master)](https://coveralls.io/github/talbertc-usgs/pymdwizard?branch=master)

<img width="250" align="right" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/USGS_logo_green.svg/500px-USGS_logo_green.svg.png"/>



pymdwizard: A Python based open source version of the Metadata Wizard
===========================================================================================

The [Metadata Wizard](https://github.com/dignizio-usgs/MDWizard_Source) is an extremely useful tool designed to facilitate FGDC 
metadata creation for spatial and some non-spatial datasets.  It is distributed
as an ESRI toolbox.  It is written in a combination of VB.net forms, ArcObjects, 
and arcpy code.  This limits the usage to Windows computers with ArcGIS installed.

This project aims to recreate and extend the current functionality using an
open-source Python based architecture which will allow for use by people who do
not have an installation of ArcMap on their computer.  Additonally we hope to extend current functionality by allowing for direct access to CSVs, and Excel workbooks, automated ITIS Taxonomy generation, and Copy-Paste (or Drag-Drop) of complete sections between different instances of the Wizard as well as between the Wizard and XML Notepad or Notepad++, and automatic navigation in the Wizard to the location of parsing errors.



----
Disclaimer:
-----------

Although this software program has been used by the U.S. Geological Survey (USGS), no warranty, expressed or implied, is made by the USGS or the U.S. Government as to the accuracy and functioning of the program and related program material nor shall the fact of distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.
