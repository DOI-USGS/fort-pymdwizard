#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module contains functionality for direct editing of USGS ScienceBase metadata
files


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
This script is part of the pymdwizard package and is not intended to be
used independently. All pymdwizard package requirements are needed.

See imports section for external packages used in this script as well as
inter-package dependencies.
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
