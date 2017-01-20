#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide functions for querying the USGS Controlled Vocabulary Service.
Provide functions for formatting the Results.
Provide functions for updating an FGDC Keywords Section with the results.


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    None


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.

Although these data have been processed successfully on a computer system at
the U.S. Geological Survey, no warranty, expressed or implied is made
regarding the display or utility of the data on any other system, or for
general or scientific purposes, nor shall the act of distribution constitute
any such warranty. The U.S. Geological Survey shall not be held liable for
improper or incorrect use of the data described and/or contained herein.

Although this program has been used by the U.S. Geological Survey (USGS), no
warranty, expressed or implied, is made by the USGS or the U.S. Government as
to the accuracy and functioning of the program and related program material
nor shall the fact of distribution constitute any such warranty, and no
responsibility is assumed by the USGS in connection therewith.
------------------------------------------------------------------------------
"""

import requests

from lxml import etree

ISO_URL = "https://www2.usgs.gov/science/term.php?thcode=15&text=ISO 19115 Topic Category"
THESAURUS_URL = "https://www2.usgs.gov/science/thesaurus.php?format=json"
SEARCH_URL = "https://www2.usgs.gov/science/term-search.php?thcode=any&term={}"
DETAILS_URL = "https://www2.usgs.gov/science/term.php?thcode={}&text={}"


def get_iso_topics():
    results = requests.get(iso_url).json()
