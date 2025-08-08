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
Module contains functionality for direct editing of USGS ScienceBase metadata
files


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

# Non-standard python libraries.
try:
    import pysb
except ImportError as err:
    raise ImportError(err, __file__)


class PYSBMissing(Exception):
    """Exception raised when the PYSB module is not available."""
    pass


def has_pysb(func):
    """
    Description:
        Decorator function to check if the PYSB module is available.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The original function if PYSB is available; raises
            PYSBMissing if PYSB is not found.
    """

    try:
        import pysb  # Attempt to import the PYSB module
    except ImportError:
        raise PYSBMissing(
            "This functionality requires the ScienceBase "
            "Python package (pysb) which was not found in this "
            "environment."
        )

    # Return the original function if PYSB is available.
    return func
