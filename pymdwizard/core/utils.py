#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
The MetadataWizard (pymdwizard) software was developed by the U.S. Geological
Survey Fort Collins Science Center.

License:            Creative Commons Attribution 4.0 International (CC BY 4.0)
                    https://creativecommons.org/licenses/by/4.0/

PURPOSE
------------------------------------------------------------------------------
Module contains a variety of miscellaneous functions


NOTES
------------------------------------------------------------------------------
None
"""

# Standard python libraries.
import sys
import os
from os.path import dirname
import platform
import datetime
import traceback
import json
import subprocess
import urllib.request
from urllib.parse import urlparse
import requests
# import pkg_resources

# Non-standard python libraries.
try:
    import pandas as pd
    from PyQt5.QtWidgets import (QLineEdit, QTextBrowser, QPlainTextEdit,
                                 QApplication, QComboBox)
    from PyQt5.QtCore import (QAbstractTableModel, Qt, QSettings)
    from PyQt5.QtGui import (QBrush, QColor, QIcon)
except ImportError as err:
    raise ImportError(err, __file__)

# Custom import/libraries.
try:
    from pymdwizard.core import (xml_utils, org_cert_setup)
    from pymdwizard import __version__
except ImportError as err:
    raise ImportError(err, __file__)

# Global variable of URL to Query USGS employee contacts.
USGS_PEOPLEPICKER_URL = "https://data.usgs.gov/modelcatalog/graphql"


def get_from_people_picker(email):
    """
    Description:
        Fetches personal information from the USGS People Picker Active
        Directory for a given email address.

    Args:
        email (str): The email address of the person to query information for.

    Returns:
        dict: A dictionary containing the person's information retrieved
            from the USGS Active Directory. If the person is not found,
            an empty dictionary is returned.

    Note:
        This function requires the `requests` library and assumes that
        the person's information is always present. It does not handle
        cases where the person might not exist in the directory or if
        the response structure is different from expected.

        The information retrieved includes email, name, DOI access ID, active
        status, affiliation, department, description, ORCID, ORCID number,
        title, street address, city, state, postal code, and telephone number.

        This function sends a GraphQL query to the USGS People Picker GraphQL
        endpoint to retrieve information about a person identified by their
        email address.
    """

    # Headers for the HTTP request.
    headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Connection": "keep-alive",
            }

    # GraphQL query to fetch user information based on email.
    query = """
            {
              active_directory(where: {email: {_eq: """
    query += f'"{email}"'
    query += """}}) {
            email
            name
            active
            affiliation
            department
            description
            orcid
            orcid_num
            title
            street_address
            city
            state
            postal_code
            telephone
          }
        }
    """

    # Data object for the GraphQL request.
    data = {
        "query": query,
        "variables": {}
    }

    # Sending POST request to the USGS People Picker API.
    response = requests.post(USGS_PEOPLEPICKER_URL, headers=headers,
                             data=json.dumps(data))

    # Return the user's data as a dictionary, or an empty dictionary.
    return dict(response.json()["data"]["active_directory"][0].items())


def convert_persondict_to_fgdc(person_dict):
    """
    Description:
        Converts a dictionary representing a person's information into
        an FGDC (Federal Geographic Data Committee) compliant XML structure.

    Args:
        person_dict (dict):
            A dictionary containing the person's information. Expected keys:
            - 'name': Full name (str).
            - 'department': Department within USGS (str).
            - 'title': Job title (str).
            - 'street_address': Street address (str).
            - 'city': City of the address (str).
            - 'state': State of the address (str).
            - 'postal_code': Postal code (str).
            - 'telephone': Telephone number (str).
            - 'email': Email address (str).

    Returns:
        ElementTree.Element: An XML node representing the contact information
            in FGDC format.

    Note:
        Constructs an XML structure for a single contact person,
        including their name, organization, position title, address,
        telephone number, and email address. The address is marked
        as both 'mailing and physical'.
    """

    # Replace any None values with the empty string
    person_dict = {k: ("" if v is None else v) for k, v in person_dict.items()}

    # Prepare contact information strings.
    cntper_str = person_dict.get("name", "")
    cntorg_str = f"USGS - {person_dict.get("department", '')}"
    cntpos_str = person_dict.get("title", "")
    address_str_comma = person_dict.get("street_address", "")
    address_str = address_str_comma.replace(",", ", ")
    city_str = person_dict.get("city", "")
    state_str = person_dict.get("state", "")
    postal_str = person_dict.get("postal_code", "")
    cntvoice_str = person_dict.get("telephone", "")
    cntemail_str = person_dict.get("email", "")
    addrtype_str = "mailing and physical"

    # Create the XML structure.
    cntinfo = xml_utils.xml_node("cntinfo")
    cntperp = xml_utils.xml_node("cntperp", parent_node=cntinfo)
    xml_utils.xml_node("cntper", text=cntper_str, parent_node=cntperp)
    xml_utils.xml_node("cntorg", text=cntorg_str, parent_node=cntperp)
    xml_utils.xml_node("cntpos", text=cntpos_str, parent_node=cntinfo)

    # Create address nodes.
    cntaddr = xml_utils.xml_node("cntaddr", parent_node=cntinfo)
    xml_utils.xml_node("addrtype", text=addrtype_str, parent_node=cntaddr)
    xml_utils.xml_node("address", text=address_str, parent_node=cntaddr)
    xml_utils.xml_node("city", text=city_str, parent_node=cntaddr)
    xml_utils.xml_node("state", text=state_str, parent_node=cntaddr)
    xml_utils.xml_node("postal", text=postal_str, parent_node=cntaddr)

    # Create contact voice and email nodes.
    xml_utils.xml_node("cntvoice", text=cntvoice_str, parent_node=cntinfo)
    xml_utils.xml_node("cntemail", text=cntemail_str, parent_node=cntinfo)

    return cntinfo


def get_usgs_contact_info(ad_username, as_dictionary=True):
    """
    Description:
        Retrieves the USGS contact information for a given Active Directory
        username.

    Args:
        ad_username (str): The Active Directory username to return contact
            information for.
        as_dictionary (bool): Specify return format as nested dictionary or
            lxml element.

    Returns:
        dict or ElementTree.Element or None: Returns None if ad_username is not
            found, otherwise returns the FGDC contact section as a dictionary
            or lxml element.
    """

    # Get the person dictionary from the People Picker service.
    person_dict = get_from_people_picker(ad_username)

    # Convert the person's dictionary to FGDC-compliant XML structure.
    element = convert_persondict_to_fgdc(person_dict)

    # Check if the organization is "GS ScienceBase" and rename tag if so.
    try:
        if element.xpath("cntperp/cntper")[0].text == "GS ScienceBase":
            element.xpath("cntperp")[0].tag = "cntorgp"
    except IndexError:
        # This exception handles the case where the required nodes do not exist.
        pass

    # Return the formatted contact information based on requested format.
    if as_dictionary:
        return xml_utils.node_to_dict(element)  # Convert to dict if requested.
    else:
        return element


def get_orcid(ad_username):
    """
    Description:
        Retrieves the ORCID of a USGS user based on their Active Directory
        username.

    Args:
        ad_username (str): The Active Directory username to search for.

    Returns:
        str or None: The ORCID as a string if found; otherwise, returns None.
    """

    try:
        # Retrieve contact information and access the ORCID.
        return get_usgs_contact_info(ad_username)["fgdc_cntperp"]["fgdc_orcid"]
    except (KeyError, TypeError):
        # Return None if the ORCID is not found or the structure is incorrect.
        return None


def populate_widget(widget, contents):
    """
    Description:
        Populates a widget's QLineEdits with text from a dictionary.

    Args:
        widget (QtGui.QWidget): The widget containing QLineEdits named according
            to the keys in the dictionary.
        contents (dict): A dictionary containing keys that correspond to line
             edits and values to be inserted as text. This dictionary will be
            flattened if it contains a nested hierarchy.

    Returns:
        None
    """

    # Convert contents to a dictionary if it is not already.
    if not isinstance(contents, dict):
        contents = xml_utils.node_to_dict(contents)

    # Iterate through the contents to populate the widget.
    for key, value in contents.items():
        if isinstance(value, dict):
            # Recursively populate for nested dictionaries.
            populate_widget(widget, value)
        else:
            # Attempt to retrieve the corresponding widget ui or widget.
            try:
                child_widget = getattr(widget.ui, key)
            except AttributeError:
                try:
                    child_widget = getattr(widget, key)
                except AttributeError:
                    child_widget = None  # Widget not found

            # Set the text for the child widget, if it exists.
            if child_widget is not None:
                set_text(child_widget, value)



def set_text(widget, text):
    """
    Description:
        Sets the text of a widget regardless of its base type.

    Args:
        widget (QtGui.QWidget): This widget could be a QLineEdit,
            QPlainTextEdit, QTextBrowser, or QComboBox.

        text (str): The text that will be inserted into the widget.

    Returns:
        None
    """


    # Check if the widget is a QLineEdit and set the text.
    if isinstance(widget, QLineEdit):
        widget.setText(text)  # Set the text for QLineEdit
        widget.setCursorPosition(0)  # Move cursor to the start

    # Check if the widget is a QPlainTextEdit and set the text.
    elif isinstance(widget, QPlainTextEdit):
        widget.setPlainText(text)  # Set plain text

    # Check if the widget is a QTextBrowser and set the text.
    elif isinstance(widget, QTextBrowser):
        widget.setText(text)  # Set text for QTextBrowser

    # Check if the widget is a QComboBox and set the text.
    elif isinstance(widget, QComboBox):
        index = widget.findText(text, Qt.MatchFixedString)
        if index >= 0:
            widget.setCurrentIndex(index)  # Set the current index if found
        else:
            widget.setEditText(text)  # Set edit text if not found


def populate_widget_element(widget, element, xpath):
    """
    Description:
        Populates a PyQt widget with text from a lxml element based on the
        provided XPath.

    Args:
        widget (QWidget): A PyQt widget, either QLineEdit or QPlainTextEdit.
        element (lxml.etree.Element): The lxml element from which to extract
            text.
        xpath (str): XPath string to locate the child element within the
            provided lxml element.

    Returns:
        None
    """

    # Check if the XPath returns any results.
    if element.xpath(xpath):
        # Get the first child element found by the XPath.
        first_child = element.xpath(xpath)[0]

        # Set the text of the widget to that of the first child.
        set_text(widget, first_child.text)


# TODO: Back up the reference to the exceptionhook. ???????????????????????????????????????? move to top
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    """
    Description:
        Custom exception hook to print exception information and exit.

    Args:
        exctype (type): The exception type.
        value (Exception): The exception instance.
        traceback (traceback): The traceback object associated with the
            exception.

    Returns:
        None
    """

    # Print the exception type, value, and traceback.
    print(exctype, value, traceback)

    # Call the default exception hook to handle the exception normally.
    sys.__excepthook__(exctype, value, traceback)

    # Exit the program with a non-zero exit code.
    sys.exit(1)


# TODO: Set the exception hook to our wrapping function ????????????????????????????????????
sys.excepthook = my_exception_hook


def launch_widget(Widget, title="", **kwargs):
    """
    Description:
        Launches a widget within its own QApplication.

    Args:
        Widget (QWidget): The widget class to be instantiated.

        title (str): The title to use for the application window.

    Returns:
        None
    """

    try:
        # Create a new instance of QApplication.
        app = QApplication([])

        # Set the application title.
        app.setApplicationName(title)

        # Instantiate the widget with provided arguments.
        widget = Widget(**kwargs)

        # Set the window title for the widget.
        widget.setWindowTitle(title)

        # Show the widget.
        widget.show()

        # Execute the application event loop.
        sys.exit(app.exec_())

    except Exception as e:
        # Handle exceptions and print the error trace.
        print("Problem encountered:")
        print(traceback.format_exc())


def get_resource_path(fname):
    """
    Description:
        Retrieves the full file path to a specified resource.

    Args:
        fname (str): The filename of the resource you would like to find.

    Returns:
        str: The full file path to the specified resource.
    """

    # return pkg_resources.resource_filename("pymdwizard",
    #                                        "resources/{}".format(fname))

    # Construct the full resource path.
    resource_path = os.path.join(
        get_install_dname("pymdwizard"),
        "pymdwizard/resources/{}".format(fname)
    )

    # Return the absolute path to the resource.
    return os.path.abspath(resource_path)


def set_window_icon(widget, remove_help=True):
    """
    Description:
        Sets a default ducky icon for a given widget.

    Args:
        widget (QWidget): The PyQt widget to which the icon will be added.

        remove_help (bool): Whether to show the help question mark icon.

    Returns:
        None
    """

    # Load the ducky icon from the resource path.
    icon = QIcon(get_resource_path("icons/Ducky.ico"))

    # Set the window icon for the widget.
    widget.setWindowIcon(icon)

    # Adjust window flags if help icon should be removed.
    if remove_help:
        widget.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )


class PandasModel(QAbstractTableModel):
    """
    Description:
        Class to populate a table view with a pandas DataFrame.
    """

    options = {
        "striped": True,
        "stripesColor": "#fafafa",
        "na_values": "least",
        "tooltip_min_len": 21,
    }


    def __init__(self, dataframe, parent=None):
        """
        Description:
            Initialize the PandasModel with a DataFrame.

        Args:
            dataframe (pd.DataFrame): The pandas DataFrame to model.
            parent (QObject): Parent object for the model.
        """

        QAbstractTableModel.__init__(self, parent)
        self.setDataFrame(dataframe if dataframe is not None else
                          pd.DataFrame())


    def setDataFrame(self, dataframe):
        """
        Description:
            Set the DataFrame for the model.

        Args:
            dataframe (pd.DataFrame): The DataFrame to set.
        """

        self.df = dataframe
        # self.df_full = self.df

        # Notify views of layout change.
        self.layoutChanged.emit()


    def rowCount(self, parent=None):
        """Return the number of rows in the DataFrame."""

        return len(self.df.values)


    def columnCount(self, parent=None):
        """Return the number of columns in the DataFrame."""

        return self.df.columns.size


    def data(self, index, role=Qt.DisplayRole):
        """
        Description:
            Retrieve data for the model.

        Args:
            index (QModelIndex): The index of the data to retrieve.
            role (int): The role of the data (e.g., display or tooltip).

        Returns:
            The data corresponding to the index and role, or None.
        """

        row, col = index.row(), index.column()
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            ret = self.df.iat[row, col]
            if (
                ret is not None and ret == ret
            ):  # convert to str except for None, NaN, NaT
                if isinstance(ret, float):
                    ret = "{:n}".format(ret)
                elif isinstance(ret, datetime.date):
                    # FIXME: show microseconds optionally
                    ret = ret.strftime(("%x", "%c")[isinstance(
                        ret, datetime.datetime)])
                else:
                    ret = str(ret)
                if role == Qt.ToolTipRole:
                    if len(ret) < self.options["tooltip_min_len"]:
                        ret = ""
                return ret
        elif role == Qt.BackgroundRole:
            if self.options["striped"] and row % 2:
                return QBrush(QColor(self.options["stripesColor"]))

        return None


    def dataframe(self):
        """Return the current DataFrame."""

        return self.df


    def reorder(self, oldIndex, newIndex, orientation):
        """
        Description:
            Reorder columns or rows in the DataFrame.

        Args:
            oldIndex (int): The original index of the item.
            newIndex (int): The desired index after reordering.
            orientation (int): Orientation of the operation (Qt.Horizontal or
                Qt.Vertical).

        Returns:
            bool: True if successfully reordered.
        """

        horizontal = orientation == Qt.Horizontal
        cols = list(self.df.columns if horizontal else self.df.index)
        cols.insert(newIndex, cols.pop(oldIndex))
        self.df = self.df[cols] if horizontal else self.df.T[cols].T

        return True


    def headerData(self, section, orientation, role):
        """
        Description:
            Retrieve header data for the model.

        Args:
            section (int): The section index for the header.
            orientation (int): The orientation (Qt.Horizontal or Qt.Vertical).
            role (int): The role of the header data.

        Returns:
            str: The header data for the specified section.
        """

        if role != Qt.DisplayRole:
            return
        label = getattr(self.df, ("columns", "index")[
            orientation != Qt.Horizontal])[section]
        # return label if type(label) is tuple else label
        return (
            ("\n", " | ")[orientation != Qt.Horizontal].join(
                str(i) for i in label)
            if type(label) is tuple
            else str(label)
        )


    def dataFrame(self):
        """Return a copy of the current DataFrame."""

        return self.df


    def sort(self, column, order):
        """
        Description:
            Sort the DataFrame based on a column.

        Args:
            column (int): The index of the column to sort by.
            order (int): The order to sort (Qt.AscendingOrder or
                Qt.DescendingOrder).

        Returns:
            None
        """

        if len(self.df):
            asc = order == Qt.AscendingOrder
            na_pos = (
                "first" if (self.options["na_values"] == "least") == asc else
                "last"
            )
            self.df.sort_values(
                self.df.columns[column], ascending=asc, inplace=True,
                na_position=na_pos
            )

            # Notify views of layout change
            self.layoutChanged.emit()


def check_fname(fname):
    """
    Description:
        Checks if the given file name is valid concerning permissions
        and the existence of its directory.

    Args:
        fname (str): The file path and name to check.

    Returns:
        str:
            'good' if the fname meets all criteria.
            'missing directory' if the directory does not exist.
            'not writable directory' if the user lacks write access.
            'not writable file' if the file cannot be opened for writing.
    """

    # Extract the directory name from the file path.
    dname = os.path.split(fname)[0]

    # Check if the directory exists.
    if not os.path.exists(dname):
        return "missing directory"

    # Check if the file exists.
    if not os.path.exists(fname):
        try:
            # Attempt to create the file and then remove it.
            with open(fname, "w") as f:
                pass  # Create the file to check for write access.
            os.remove(fname)  # Remove the file after creating it.
            return "good"
        except Exception:
            # Return an error if the directory is not writable.
            return "not writable directory"
    else:
        try:
            # Attempt to open the existing file in append mode.
            with open(fname, "a") as f:
                pass  # Check if the file can be opened for writing.
            return "good"
        except Exception:
            # Return an error if the file is not writable.
            return "not writable file"


def url_validator(url, qualifying=None):
    """
    Description:
        Validates if a given string adheres to URL syntax.

    Args:
        url (str): The string to check for valid URL syntax.
        qualifying (list, optional): URL attributes to check for as a list of
            strings. Defaults to ['scheme', 'netloc'].

    Returns:
        bool: True if the URL is valid based on the qualifying attributes,
            otherwise False.
    """

    # Default attributes required for a valid URL.
    min_attributes = ("scheme", "netloc")

    # Use default attributes if none provided.
    qualifying = min_attributes if qualifying is None else qualifying

    # Parse the URL into its components.
    token = urlparse(url)

    # Verify that all qualifying attributes are present.
    return all(
        getattr(token, qualifying_attr) for qualifying_attr in qualifying)


def get_install_dname(which="pymdwizard"):
    """
    Description:
        Retrieves the full path to the installation directory.

    Args:
        which (str, optional): Specifies which subdirectory to return:
            'root', 'pymdwizard', or 'python'.

    Returns:
        str: path and directory name of the directory where pymdwizard is
            installed.
    """

    # Get the absolute file path of the current script.
    this_fname = os.path.realpath(__file__)

    if platform.system() == "Darwin":
        # For macOS, get the path to the 'content' folder .
        pymdwizard_dname = os.path.abspath(
            os.path.join(dirname(this_fname), *[".."] * 2)
        )
        root_dir = pymdwizard_dname
        executable = sys.executable
        python_dname = os.path.split(executable)[0]

    else:
        # For non-macOS systems, navigate three levels up to find the directory.
        pymdwizard_dname = dirname(dirname(dirname(this_fname)))
        root_dir = os.path.dirname(pymdwizard_dname)
        python_dname = os.path.join(root_dir, "pymdwizard")

        # Check if the python directory exists.
        if not os.path.exists(python_dname):
            executable = sys.executable
            python_dname = os.path.split(executable)[0]

    # Return the requested directory based on the 'which' argument.
    if which == "root":
        return root_dir
    elif which == "pymdwizard":
        return pymdwizard_dname
    elif which == "python":
        return python_dname

    # If no valid option is provided, return None.
    return None


def get_pem_fname():
    """
    Description:
        Retrieves the absolute path to the DOIRootCA2.pem file.

    Args:
        None

    Returns:
        str: The absolute path to the DOIRootCA2.pem file.
    """

    # Construct the full path to the DOIRootCA2.pem file.  ?????????????????????? TODO: Do we want to use this path
    pem_path = os.path.abspath(os.path.join(
        get_install_dname("pymdwizard"),
        "pymdwizard",
        "resources",
        "DOIRootCA2.pem"
    ))

    return pem_path


def check_pem_file():
    """
    Description:
        Convenience USGS function to check if the DOI PEM file is stored
        in the wincertstore and to export a local copy for use in the
        application.

    Args:
        None

    Returns:
        str or None: The local path to the PEM file if successfully obtained,
            otherwise None.
    """

    # Define path and name of pem file that will be stored locally (if this
    # function has been run once before).
    pem_fname = get_pem_fname()
    cert_file = os.path.basename(pem_fname)  # "DOIRootCA2.pem"

    # Set up certificate on system for Metadata Wizard.
    cert_file = org_cert_setup.cert_setup(cert_file)


def requests_pem_get(url, params={}):
    """
    Description:
        Makes a GET request using the provided URL and parameters,
        utilizing a local PEM file if an SSL error occurs.

    Args:
        url (str): The URL to make the GET request to.
        params (dict, optional): Parameters to send with the GET request.

    Returns:
        Response: The result of the requests.get call, which includes
            the server's response.
    """

    # Use an empty dictionary if no params are provided.
    if params is None:
        params = {}

    try:
        # Attempt to make a GET request.
        return requests.get(url, params=params)
    except requests.exceptions.SSLError:
        # In case of an SSL error, get the PEM file name.
        pem_fname = get_pem_fname()

        # Retry the GET request with the PEM file for verification.
        return requests.get(url, params=params, verify=pem_fname)


def get_setting(which, default=None):
    """
    Description:
        Retrieves a setting from the pymdwizard application.

    Args:
        which (str): The name of the setting to return.

        default (optional): The value to return if the setting is not found.

    Returns:
        The setting in its native format (string, integer, etc.).
    """

    # Create a QSettings object for the application settings.
    settings = QSettings("USGS_" + __version__,
                             "pymdwizard_" + __version__)

    # Return the setting value, or default if not found
    return settings.value(which, default)


def url_is_alive(url):
    """
    Description:
        Checks if a given URL is reachable.

    Args:
        url (str): The URL to check for reachability.

    Returns:
        bool: True if the URL is reachable, False otherwise.
    """

    # Prefix the URL with 'https://' if it starts with 'www'.
    if url.startswith("www"):
        url = "https://" + url

    # Create a request to perform a HEAD request.
    try:
        request = urllib.request.Request(url)
        request.get_method = lambda: "HEAD"  # Use HEAD method for request
    except Exception:
        # Return False if request creation fails
        return False

    # Attempt to open the URL and return True if successful.
    try:
        urllib.request.urlopen(request)
        return True
    except Exception:
        # Return False if URL is not reachable.
        return False
