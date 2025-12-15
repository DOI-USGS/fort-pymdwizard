#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Launcher script (CLI) for the application

This module is used to launch the main application (MainWindow.py)
It does two things, initialize environment variables (windows only)
Pass command line arguments to the MainWindow script.


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import argparse
import os
import sys


def set_clean_path():
    """
    Description:
        For installations on Windows (assumes installed via installer)
            - prepends the path with the installer's python directory and bin
              directory
            - makes a copy of the PEM file from the user's registry
            - sets the gdal environmental variables

    Args:
        None

    Returns:
        None
    """

    if os.name == "nt":
        cur_python_exe = sys.executable
        executable_dir = os.path.split(cur_python_exe)[0]
        os.environ["path"] = ";".join(
            [
                executable_dir,
                os.path.join(executable_dir, "Library", "bin"),
                os.path.join(executable_dir, "Scripts"),
                # os.environ["path"],
            ]
        )

    else:
        pass

    # Allow python to recognize module pymdwizard.
    this_fname = os.path.realpath(__file__)
    root_dir = os.path.dirname(this_fname)
    sys.path.append(os.path.dirname(root_dir))

    # Setup DOI (organizational) certificate.
    from pymdwizard.core.utils import check_pem_file
    check_pem_file()

    # Set up access to GDAL data.
    from pymdwizard.core.spatial_utils import set_local_gdal_data

    # Set up local GDAL data.
    set_local_gdal_data()


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    parser = argparse.ArgumentParser(description="Metadata Wizard")
    parser.add_argument(
        "xml_fname",
        help="The FGDC (or BDP) XML file to load",
        type=str,
        default=None,
        nargs="?",
    )
    help_str = "The CSV or SHP file to use for populating the spdom, spdoinfo,"
    help_str += " spref and eainfo sections"
    parser.add_argument(
        "introspect_fname", help=help_str, type=str, default=None,
        nargs="?"
    )
    args = parser.parse_args()

    # Call function above.
    set_clean_path()

    # Handle high resolution displays with QT.
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Open application.
    from pymdwizard.gui import MainWindow
    MainWindow.launch_main(
        xml_fname=args.xml_fname,
        introspect_fname=args.introspect_fname,
        env_cache=os.environ,
    )
