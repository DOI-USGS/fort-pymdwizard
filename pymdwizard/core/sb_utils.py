#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

PURPOSE
------------------------------------------------------------------------------
Legacy module placeholder. Direct editing of USGS ScienceBase metadata files
has been removed from the Metadata Wizard.


NOTES
------------------------------------------------------------------------------
The ScienceBase integration functionality was deprecated and removed. This
stub remains to avoid breaking imports in older code.
"""

# Non-standard python libraries.
try:
    import sciencebasepy
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

    # sciencebasepy is already imported at module level (line 23)
    # If not available, the module would have failed to load
    return func
