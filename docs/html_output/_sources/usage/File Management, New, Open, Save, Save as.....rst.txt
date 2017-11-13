=============================================
File Management, New, Open, Save, Save as....
=============================================

The Extensible Markup Language (XML) file format is the only currently supported format for metadata used by the Metadata Wizard. The XML format is one of the most commonly used formats for CSDGM metadata and is the format expected by many repositories and tools. By convention, the metadata file will be named identically to the data file it describes, with the addition of an .xml extension. For example data.csv would have an associated metadata file called data.csv.xml.

Within the Metadata Wizard tool, XML files can be created, opened, saved, or saved as a new name using a dropdown file menu similar to many desktop applications. In the file browser window that is accessed for these functions, only files with an .xml extension are recognized.

New
----

When creating new metadata files, click the **File -> New** option and navigate to a directory where metadata output should be saved. This will create a new .xml with the content contained in the default metadata template as well as the current date in the metadata date element. See `Changing-Your-Template`_ for more information about updating your template to streamline future metadata creation.

Open
----

To modify or extend an existing record, click **File -> Open** and browse to a local .xml file. An XML file can also be opened in the application via drag-and-drop.

Save
----

When closing the application or switching records, users will be prompted to save their changes. It is good practice to save periodically when editing a record by clicking **File -> Save**.

Save as ...
-----------

Click **File -> Save as…** to save the output as a new file.  

Recent Files
------------

A list of the last 10 files opened will be stored in the **File -> Recent Files:** menu item. Clicking on a file name in that menu list will open that record.

Exit
----

Clicking **File -> Exit** will close out of the tool.

--------------

File management in Metadata Wizard 2.0 is quite a bit different from the previous ESRI toolbox-based version.

.. _Changing-Your-Template: ../advancedusage/Changing%20Your%20Template.html
