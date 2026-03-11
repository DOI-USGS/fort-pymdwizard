#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard(pymdwizard) software was developed by the
U.S. Geological Survey Fort Collins Science Center.
See: https://github.com/usgs/fort-pymdwizard for current project source code
See: https://usgs.github.io/fort-pymdwizard/ for current user documentation
See: https://github.com/usgs/fort-pymdwizard/tree/master/examples
    for examples of use in other scripts

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    http://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module for Python package creation


NOTES
------------------------------------------------------------------------------
None
"""

import os
import sys

# try:
#     import core
#     import gui
# except ImportError:
#     from pymdwizard import gui
#     from pymdwizard.gui.ui_files import growingtextedit
#     from pymdwizard import core

this_fname = os.path.realpath(__file__)
root_dir = os.path.dirname(this_fname)
sys.path.append(os.path.join(root_dir, "gui", "ui_files"))

# Version of software properties used in different places of UIs. Change this
# value and do not hardcode else where.
__version__ = "2.2.0"
__author__ = "U.S. Geological Survey, Fort Collins Colorado"
__copyright__ = "Creative Commons (Universal 4.0)"
__license__ = "Creative Commons (Universal 4.0)"
__status__ = "Final"
