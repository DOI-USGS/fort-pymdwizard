#!/usr/bin/env python3

import argparse

import sys
print(sys.argv)

from pymdwizard.gui import MainWindow

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Metadata Wizard")
    parser.add_argument("xml_fname", help="The FGDC (or BDP) XML file to load", type=str, default=None, nargs='?',)
    parser.add_argument("introspect_fname", help="The CSV or SHP file to use for populating the spdom, spdoinfo, spref and eainfo sections", type=str, default=None, nargs='?',)
    args = parser.parse_args()

    MainWindow.launch_main(xml_fname=args.xml_fname,
                           introspect_fname=args.introspect_fname)
