#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

PURPOSE
------------------------------------------------------------------------------
Contains a custom PyQt5 syntax highlighter for real-time spell checking in 
text widgets


SCRIPT DEPENDENCIES
------------------------------------------------------------------------------
    This script is part of the pymdwizard package and is not intended to be
    used independently.  All pymdwizard package requirements are needed.

    See imports section for external packages used in this script as well as
    inter-package dependencies


NOTES
------------------------------------------------------------------------------
None
"""

from PyQt5 import QtCore, QtGui
import re

from pymdwizard.core import utils


def load_words():

    fname = utils.get_resource_path("spelling/words.txt")
    global word_set
    try:
        word_set = set(line.strip() for line in open(fname, "r"))
    except UnicodeDecodeError:
        word_set = set(line.strip() for line in open(fname, "r", encoding="latin-1"))

    return word_set


word_set = load_words()


class Highlighter(QtGui.QSyntaxHighlighter):
    """
    An implementation of a custom syntax highlighter that highlights
    misspelled words
    """

    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.sectionFormat = QtGui.QTextCharFormat()
        self.sectionFormat.setForeground(QtCore.Qt.blue)
        self.errorFormat = QtGui.QTextCharFormat()
        self.errorFormat.setForeground(QtCore.Qt.red)
        self.errorFormat.setBackground(QtCore.Qt.yellow)

        # Only hightlight when the hightlighter is enabled
        self.enabled = True

    def highlightBlock(self, text):
        """

        Parameters
        ----------
        text

        Returns
        -------

        """
        if not self.enabled:
            return None

        words = re.findall(r"[\w]+", text)

        for word in words:
            if word.lower() not in word_set and re.search("[a-zA-Z]", word) is not None:
                clean = " " + re.sub(r"[^a-zA-Z]", " ", text) + " "
                try:
                    self.setFormat(
                        clean.index(" {} ".format(word)), len(word), self.errorFormat
                    )
                except ValueError:
                    pass
