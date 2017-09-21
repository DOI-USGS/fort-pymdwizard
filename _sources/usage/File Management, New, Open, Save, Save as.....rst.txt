File Management, New, Open, Save, Save as....
********

The Extensible Markup Language (XML) file format is the only currently
supported format for the metadata used by the Metadata Wizard. The XML
format is one of the most commonly used formats for CSDGM metadata and
is the format expected by many repositories and tools. By convention the
metadata file will be named identically to the data file it describes
with the addition of a .xml extension. For example data.csv would have a
metadata file called data.csv.xml.

Within the Metadata Wizard XML files can be created, opened, saved, or
saved as a new name using a dropdown file menu similar to many desktop
applications. In the file browser window that pops up for these
functions only files with a .xml extension will be visible.

When first getting started making metadata click the File -> New option
and navigate to a directory wher you want to save metadata output. This
will create a new .xml with the content contained in the default
metadata template as well as the current date in the metadata date
element. See `Changing-Your-Template`_ for more information about
updating your template to streamline future metadata creation.

If you would like to modify or extend an existing record click File ->
Open and browse to a local .xml file. Make sure to click File -> Save
as… if you want to save the output to a new file.

A list of the last 10 files opened will be stored in the File -> Recent
Files: menu item. Clicking on a file name in that menu list will open
that record.

When closing the application or switching records a users will be
prompted to save their changes. It’s a good practice to save
periodically when editing a record by clicking File -> Save.

--------------

File Management in this new version of the Metadata Wizard is quite a
bit different the previous ESRI toolbox based version.

.. _Changing-Your-Template: img/Changing-Your-Template