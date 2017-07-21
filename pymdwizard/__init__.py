from __future__ import absolute_import

import os, sys

try:
    import gui
    import core
except:
    from pymdwizard import gui
    from pymdwizard.gui.ui_files import growingtextedit
    from pymdwizard import core

this_fname = os.path.realpath(__file__)
root_dir = os.path.dirname(this_fname)
sys.path.append(os.path.join(root_dir, 'gui', 'ui_files'))