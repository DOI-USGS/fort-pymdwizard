#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Provide a pyqt widget for the FGDC component with a shortname matching this
file's name.


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import os
import tempfile
import getpass

# Non-standard python libraries.
try:
    import sciencebasepy
    from PyQt5.QtWidgets import (QWidget, QMessageBox)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (utils, xml_utils)
    from pymdwizard.gui.ui_files import UI_sb_locator
except ImportError as err:
    raise ImportError(err, __file__)


class SBLocator(QWidget):
    """
    Description:
        A widget used to locate and manage a metadata file associated
        with a ScienceBase item. It handles user login, permission
        checking, and file download/upload.

    Passed arguments:
        username (str, optional): ScienceBase username. Defaults to the
            current system user's email if possible.
        password (str, optional): ScienceBase password. Defaults to None.
        hash (str): The ScienceBase item ID (hash).
        parent (QWidget, optional): The parent widget. Defaults to None.
        mainform (QWidget, optional): Reference to the main application
            form for file loading operations.

    Returned objects:
        None

    Workflow:
        1. Initializes credentials and UI.
        2. Connects buttons to check permissions and handle the "OK"
           (load file) action.
        3. Manages login, permission checks, and file transfer using
           the "sciencebasepy" library.

    Notes:
        Inherits from "QWidget".
    """

    def __init__(
        self,
        username=None,
        password=None,
        hash="593af2e0e4b0764e6c602207",
        parent=None,
        mainform=None,
    ):

        # Store reference to the main application form.
        self.mainform = mainform
        self.fname = None

        # Use a utility to get contact email.
        if username is None:
            try:
                username = getpass.getuser()
                contact = utils.get_usgs_contact_info(username, True)
                self.username = contact["fgdc_cntemail"]
            except:
                self.username = ""
        else:
            self.username = username

        # Initialize the base class.
        QWidget.__init__(self, parent=parent)
        self.ui = UI_sb_locator.Ui_Form()
        self.ui.setupUi(self)

        # Store input credentials and item ID.
        self.password = password
        self.hash = hash

        # Populate UI fields.
        self.ui.username.setText(self.username)
        self.ui.password.setText(password)
        self.ui.hash.setText(hash)

        self.setWindowTitle("ScienceBase Item/User Identifier")

        self.connect_events()

    def log_into_sb(self):
        """
        Description:
            Creates and returns an active ScienceBase session by logging
            in with the stored username and password.

        Passed arguments:
            None

        Returned objects:
            sb (sciencebasepy.SbSession): An active ScienceBase session
                object.

        Workflow:
            Initializes SbSession and calls login with stored credentials.

        Notes:
            None
        """

        # Create a new ScienceBase session.
        sb = sciencebasepy.SbSession()

        # Log in with the current credentials.
        sb.login(username=self.username, password=self.password)

        return sb

    def connect_events(self):
        """
        Description:
            Connects the "OK" and "Check Permissions" buttons to their
            respective handler functions.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Connects "btn_ok.clicked" to "ok_click" and
            "btn_check.clicked" to "check_permissions".

        Notes:
            None
        """

        self.ui.btn_ok.clicked.connect(self.ok_click)
        self.ui.btn_check.clicked.connect(self.check_permissions)

    def update_content(self):
        """
        Description:
            Updates internal state variables with the current text
            from the UI input fields.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Reads text from username, password, and hash fields.

        Notes:
            None
        """

        self.password = self.ui.password.text()
        self.username = self.ui.username.text()
        self.hash = self.ui.hash.text()

    def ok_click(self):
        """
        Description:
            Handles the "OK" button click, verifying permissions and
            downloading the FGDC file to load into the main form.

        Passed arguments:
            None

        Returned objects:
            bool: False if permission check fails, None if file not found.

        Workflow:
            1. Updates credentials.
            2. Checks permissions.
            3. Downloads FGDC file.
            4. If successful, loads the file into "mainform" and hides.

        Notes:
            None
        """

        self.update_content()

        # Check permissions before proceeding.
        if not self.check_permissions():
            return False

        # Get the path to the downloaded FGDC file.
        fname = self.get_fgdc_file()
        if not fname:
            return None

        # Load the file into the main application.
        self.mainform.load_file(self.fname)
        self.mainform.sb_file = True
        self.mainform.cur_fname = self.fname
        self.hide()

        return True

    def check_item_click(self):
        """
        Description:
            Updates content and checks permissions, typically called
            by a "Check" button (though the primary handler is
            "check_permissions").

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Updates content and calls "check_permissions".

        Notes:
            None
        """

        self.update_content()
        accessible = self.check_permissions()

    def check_permissions(self):
        """
        Description:
            Attempts to log in to ScienceBase and verify that the user
            has write permissions for the specified item ID.

        Passed arguments:
            None

        Returned objects:
            bool: True if login and write permissions are successful,
                  False otherwise.

        Workflow:
            1. Tries to log in. Fails if credentials are bad.
            2. Tries to get permissions for the item.
            3. Checks for direct or inherited write permissions.
            4. Displays warning messages on failure.

        Notes:
            Retrieves item title and checks for the FGDC file on success.
        """

        try:
            self.update_content()
            sb = self.log_into_sb()
        except:
            # Handle login failure
            msg = "Login to ScienceBase Failed. \nCheck username and password"
            QMessageBox.warning(self, "SB Login Failed", msg)
            return False

            # Check for direct write permission.
            writable = False
            try:
                permissions = sb.get_permissions(self.hash)
                writable = ("USER:{}".format(self.username) in
                            permissions["write"]["acl"])
            except:
                # Continue to check for inherited permission.
                pass

        # Check for inherited write permission.
        if not writable:
            try: 
                writable = permissions["write"]["inherited"] == True
            except: 
                writable = False

        if not writable:
            # Handle write permission failure
            msg = ("This item does not appear to be writable by the "
                   "designated user.")
            QMessageBox.warning(self, "Write permission error", msg)
            return False

        if writable:
            # Permission check successful, check for file existence.
            item = sb.get_item(self.hash)
            title = item['title']

            fname = self.get_fgdc_file()

            if fname:
                # Inform user the item is ready to edit.
                msg = f"SB item:\n {self.hash} ready to open and edit."
                QMessageBox.information(self, "Good to go!", msg)
            else:
                return False

        return True

    def get_fgdc_file(self):
        """
        Description:
            Downloads the FGDC XML file associated with the ScienceBase
            item to a temporary directory.

        Passed arguments:
            show_success (bool): Whether to show a success message.

        Returned objects:
            str or bool: The temporary path to the downloaded file,
                         or False if the file could not be determined.

        Workflow:
            1. Saves the current open file (if any).
            2. Logs into SB and gets the item JSON.
            3. Filters files for "application/fgdc+xml".
            4. Handles zero, one, or multiple files, displaying warnings.
            5. If exactly one file, downloads it and returns the path.

        Notes:
            The downloaded file path is stored in self.fname.
        """

        # Save any currently open file before downloading a new one.
        if self.mainform.cur_fname:
            self.mainform.save_file()

        sb = self.log_into_sb()
        tempdir = tempfile.gettempdir()
        item_json = sb.get_item(self.hash)

        fgdc_files = []
        try:
            # Look for explicit FGDC files.
            fgdc_files = [
                f
                for f in item_json["files"]
                if f["contentType"] == "application/fgdc+xml"
            ]
        except KeyError:
            try:
                # Fallback: Look for XML files in the first facet.
                fgdc_files = [
                    f
                    for f in item_json["facets"][0]["files"]
                    if f["name"].endswith(".xml")
                ]
            except:
                fgdc_files = []

        if len(fgdc_files) == 1:
            # Case 1: Perfect match (one FGDC file)
            url = fgdc_files[0]["url"]
            fname = fgdc_files[0]["name"]

            # Download the file to the temporary directory.
            sb.download_file(url, fname, tempdir)
            self.fname = os.path.join(tempdir, fname)

            return self.fname
        elif len(fgdc_files) == 0:
            # Case 2: No FGDC file found
            msg = (f"There doesn't appear to be an FGDC XML file "
                   f"associated with item: {self.hash}.\n")
            msg += ("You will need to upload a new FGDC record to the "
                    "item to use this functionality.")
            QMessageBox.warning(self, "No existing Metadata file!", msg)

            return False
        else:
            # Case 3: More than one FGDC file found
            msg = (f"There appears to be more than one FGDC XML file "
                   f"associated with item: {self.hash}.\n")
            msg += ("Since we can't determine which to edit, this "
                    "functionality won't work.")
            msg += "\nYou will need to download and edit the file directly."
            QMessageBox.warning(self, "More than one XML file!", msg)

            return False

    def put_fgdc_file(self):
        """
        Description:
            Uploads the local FGDC file (self.fname) back to the
            ScienceBase item, replacing the existing file.

        Passed arguments:
            None

        Returned objects:
            None

        Workflow:
            Logs into SB, gets the item JSON, and calls "replace_file".

        Notes:
            Assumes self.fname is the local path of the metadata file.
        """

        sb = self.log_into_sb()

        # Get the item's current JSON structure.
        item_json = sb.get_item(self.hash)

        # Upload the local file, replacing the one in the item.
        sb.replace_file(self.fname, item_json)


if __name__ == "__main__":
    """
    Run the code as a stand alone application without importing script.
    """

    # Helper to launch the widget for testing.
    utils.launch_widget(SBLocator, "SBLocator", password="")
