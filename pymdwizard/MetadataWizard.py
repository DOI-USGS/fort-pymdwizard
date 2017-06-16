#!/usr/bin/env python3

import argparse

import os
import sys



def set_clean_path():

    if os.name == 'nt':
        this_fname = os.path.realpath(__file__)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_fname)))
        python_dname = os.path.join(root_dir, 'Python35_64')
        os.environ['path'] = ";".join([python_dname, os.path.join(python_dname, 'Library', 'bin')])
    else:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Metadata Wizard")
    parser.add_argument("xml_fname", help="The FGDC (or BDP) XML file to load", type=str, default=None, nargs='?',)
    parser.add_argument("introspect_fname", help="The CSV or SHP file to use for populating the spdom, spdoinfo, spref and eainfo sections", type=str, default=None, nargs='?',)
    args = parser.parse_args()

    set_clean_path()
    from pymdwizard.gui import MainWindow
    MainWindow.launch_main(xml_fname=args.xml_fname,
                           introspect_fname=args.introspect_fname)
