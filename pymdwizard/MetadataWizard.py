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
Launcher script (CLI) for the application

This module is used to launch the main application (MainWindow.py)
It does two things, initialize environment variables (windows only)
Pass command line arguments to the MainWindow script.

Todo:
    * Make this functionality cross platform


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intented to be
    used independently.  All pymdwizard package requirements are needed.
    
    See imports section for external packages used in this script as well as
    inter-package dependencies


U.S. GEOLOGICAL SURVEY DISCLAIMER
------------------------------------------------------------------------------
This software has been approved for release by the U.S. Geological Survey 
(USGS). Although the software has been subjected to rigorous review,
the USGS reserves the right to update the software as needed pursuant to
further analysis and review. No warranty, expressed or implied, is made by
the USGS or the U.S. Government as to the functionality of the software and
related material nor shall the fact of release constitute any such warranty.
Furthermore, the software is released on condition that neither the USGS nor
the U.S. Government shall be held liable for any damages resulting from
its authorized or unauthorized use.

Any use of trade, product or firm names is for descriptive purposes only and
does not imply endorsement by the U.S. Geological Survey.

Although this information product, for the most part, is in the public domain,
it also contains copyrighted material as noted in the text. Permission to
reproduce copyrighted items for other than personal use must be secured from
the copyright owner.
------------------------------------------------------------------------------
"""

import argparse

import os
import sys


def set_clean_path():
    """
    For installations on Windows (assumes installed via installer)
    - prepends the path with the installer's python directory and bin directory
    - makes a copy of the PEM file from the user's registry
    - sets the gdal environmental variables
    :return:
     None
    """

    if os.name == 'nt':
        cur_python_exe = sys.executable
        executable_dir = os.path.split(cur_python_exe)[0]
        os.environ['path'] = ";".join([executable_dir,
                                       os.path.join(executable_dir, 'Library',
                                                    'bin'),
                                       os.environ['path']])

        from pymdwizard.core.utils import check_pem_file
        check_pem_file()

        from pymdwizard.core.spatial_utils import set_local_gdal_data
        set_local_gdal_data()

    else:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Metadata Wizard")
    parser.add_argument("xml_fname", help="The FGDC (or BDP) XML file to load",
                        type=str, default=None, nargs='?',)
    help_str = "The CSV or SHP file to use for populating the spdom, spdoinfo,"
    help_str += " spref and eainfo sections"
    parser.add_argument("introspect_fname", help=help_str,
                        type=str, default=None, nargs='?',)
    args = parser.parse_args()

    set_clean_path()
    from pymdwizard.gui import MainWindow
    MainWindow.launch_main(xml_fname=args.xml_fname,
                           introspect_fname=args.introspect_fname)

