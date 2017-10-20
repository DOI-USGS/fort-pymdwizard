#!/usr/bin/env python3

import argparse

import os
import sys



def set_clean_path():

    if os.name == 'nt':
        cur_python_exe = sys.executable
        executable_dir = os.path.split(cur_python_exe)[0]
        os.environ['path'] = ";".join([executable_dir,
                                       os.path.join(executable_dir, 'Library', 'bin')])

        from pymdwizard.core.utils import check_pem_file
        check_pem_file()

        from pymdwizard.core.spatial_utils import set_local_gdal_data
        set_local_gdal_data()
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
