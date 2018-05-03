"""Unittests for misc functions"""


import pytest


def test_spellinghighlighter():
    from pymdwizard.gui.ui_files import spellinghighlighter

    for word in ['this', 'word', 'is', 'correct']:
        assert word in spellinghighlighter.word_set

    for word in ['thisss', 'worrd', 'istar', 'notcorrect']:
        assert word not in spellinghighlighter.word_set

