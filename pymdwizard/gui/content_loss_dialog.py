#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            CC0 1.0 Universal
                    https://creativecommons.org/publicdomain/zero/1.0/

PURPOSE
------------------------------------------------------------------------------
Provide a resizable dialog for the content-loss warnings shown when a record
is opened or saved: an icon, a scrollable rich-text area, and a row of
buttons.


NOTES
------------------------------------------------------------------------------
+ QMessageBox can't be resized and doesn't scroll, so a long list of affected
  fields either overflows the screen or is cut off. This dialog keeps the
  message-box look but puts the text in a QTextBrowser.
+ Built in code rather than from a Qt Designer .ui file, since the layout is
  a single text area and a button row.
"""

# Non-standard python libraries.
try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QDialog,
        QDialogButtonBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QStyle,
        QTextBrowser,
        QVBoxLayout,
    )
except ImportError as err:
    raise ImportError(err, __file__)


class ContentLossDialog(QDialog):
    """
    Description:
        A modal, resizable dialog that shows rich text in a scrollable area
        and records which of its buttons the user pressed.

    Passed arguments:
        parent (QWidget): Parent window.
        title (str): Window title.
        html_text (str): The message, as Qt rich text (HTML).
        buttons (list of (str, str)): (label, key) for each button, left to
            right. The key of the pressed button is stored in clicked_key.
        default_key (str or None): Key of the button that Enter activates.
        warning (bool): Show the warning icon (True) or the information
            icon (False).

    Returned objects:
        None. After exec_(), clicked_key holds the key of the button pressed,
        or None if the dialog was closed with Esc or the window's close
        button. Callers must treat None as the safe choice.

    Workflow:
        1. Lays out the icon beside a QTextBrowser holding html_text.
        2. Sizes the dialog to the text, up to a cap, after which the text
           scrolls. The user can resize it with the size grip.
        3. Each button stores its key and closes the dialog.

    Notes:
        Links in the text open in the system browser.
    """

    # Width of the text area, and the tallest the dialog opens at before the
    # text scrolls. The user can resize past both.
    TEXT_WIDTH = 520
    MAX_TEXT_HEIGHT = 460

    def __init__(
        self,
        parent,
        title,
        html_text,
        buttons,
        default_key=None,
        warning=True,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        # Remove the "?" (What's This?) button Qt adds to dialogs on Windows;
        # the Wizard has no help text behind it, so it does nothing.
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint
        )
        self.setSizeGripEnabled(True)
        self.setModal(True)

        self.html_text = html_text
        self.button_keys = [key for _label, key in buttons]
        self.default_key = default_key
        self.clicked_key = None

        # Icon, matching the standard message box icons.
        which = (
            QStyle.SP_MessageBoxWarning
            if warning
            else QStyle.SP_MessageBoxInformation
        )
        icon = QLabel()
        icon.setPixmap(self.style().standardIcon(which).pixmap(32, 32))
        icon.setAlignment(Qt.AlignTop)

        # Scrollable rich text.
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setFrameShape(QTextBrowser.NoFrame)
        self.browser.setStyleSheet("background: transparent;")
        self.browser.setHtml(html_text)

        body = QHBoxLayout()
        body.addWidget(icon)
        body.addWidget(self.browser, 1)

        # Buttons.
        self.button_box = QDialogButtonBox()
        self.buttons = {}
        for label, key in buttons:
            button = QPushButton(label)
            button.setAutoDefault(key == default_key)
            button.setDefault(key == default_key)
            button.clicked.connect(
                lambda _checked=False, k=key: self._choose(k)
            )
            self.button_box.addButton(button, QDialogButtonBox.ActionRole)
            self.buttons[key] = button

        layout = QVBoxLayout(self)
        layout.addLayout(body, 1)
        layout.addWidget(self.button_box)

        self._fit_to_text()

    def text(self):
        """Returns the rich text the dialog shows."""

        return self.html_text

    def _choose(self, key):
        """Records the pressed button's key and closes the dialog."""

        self.clicked_key = key
        self.accept()

    def _fit_to_text(self):
        """
        Opens the dialog just tall enough for the text, up to
        MAX_TEXT_HEIGHT, after which the text area scrolls.
        """

        document = self.browser.document()
        document.setTextWidth(self.TEXT_WIDTH)
        margin = 2 * int(document.documentMargin())
        text_height = int(document.size().height()) + margin + 4
        self.browser.setMinimumWidth(self.TEXT_WIDTH + margin)
        self.browser.setMinimumHeight(min(text_height, 120))

        chrome = self.sizeHint().height() - self.browser.sizeHint().height()
        self.resize(
            self.TEXT_WIDTH + 100,
            min(text_height, self.MAX_TEXT_HEIGHT) + max(chrome, 60),
        )
