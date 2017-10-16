How to fill out the Entity and Attribute tab
********

|

**The Entity and Attribute section is one of the most useful sections
for data re-use**. It allows users to unambiguously determine the
appropriate way to interpret the data. Included are items such as what
units the data are in, measurement resolution, what abbreviations stand
for, and where you could look up the categorical values used.

--------------

This tool facilitates a robust Entity and Attribute generation by
auto-populating much of this content by introspecting the data being
documented directly. Currently CSV, Excel, and Shapefile formats are
supported, with additional geospatial formats available when calling the
MetadataWizard 2.0 from the ArcToolbox.

--------------

--------------

**Given the diversity of data that can be described in a single Entity and attribute metadata section, here are some options for how to fill out this section:**

Data described elsewhere
------------------------

The data are fully described in a data dictionary or other document that
can be referenced in this record.

    | *Leave the ‘Detailed’ tab empty but fill out the ‘Overview’ tab with a
      description of where one can obtain the appropriate data
      dictionary or other document. Make sure that the document being
      referenced is going to be persistent and easily available to all
      users of this data. If there is some question about this, consider
      including a copy of the data dictionary with this data/metadata.*
    | 

Data in a proprietary or complex format
----------------------------------

The data are in a proprietary format (Genbank format data), organized in
a complex but non-tabular format (folder with individual files that
adhere to a naming convention), or are easily described (A photo scan of
a historic map).

    | *Leave the ‘Detailed’ tab empty but fill out the ‘Overview’ with a
      description of the data format, naming conventions, or contents.*
    | 

Single tabular dataset
----------------------

The data are tabular in nature (CSV, shapefile attribute table, Excel
worksheet) and in a ‘tidy format’ where each variable forms a column,
each observation forms a row, and each observational unit forms a table.

      On the ‘Detailed’ tab click the ‘Browse to Dataset’ button on the
      left and navigate to your data file. Appropriate content will be
      extracted from your file to fill the form. Sequentially fill out
      each of the columns on the right, by providing a definition of
      what’s in that column. For each column also provide the Column
      Contents which will be one of:
    | 1.  **Enumerated** (Categorical/Factor data for which a definition will
      need to be provided for each unique value in the column.
    | 2.  **Range** for numerical, non-categorical data. A minimum value, maximum value, and the units of measure (where applicable) will be required.
    | 3.  **Codeset** for when the values can be obtained from a definitive
      source which is specified.
    | 4. **Unrepresentable** for every other case where you must provide a
      free text description of how to interpret the values in this column.
    

Multiple tabular datasets
-------------------------

The data consists of multiple distinct tabular datasets, for example
several related CSVs or multiple sheets in an Excel workbook.

    Click the ‘Add Detailed‘ button at the bottom of the Instructions tab.