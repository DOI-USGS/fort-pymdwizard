=======================================
Populating the Entity and Attribute Tab
=======================================

**The Entity and Attribute section is one of the most useful sections
for data re-use**. It allows users to unambiguously determine the
appropriate way to interpret the data. Included are items such as what
units the data are in, measurement resolution, abbreviation definitions, 
and links to data dictionaries, or codesets, if applicable.

----------------------------------------------------------------------

This tool facilitates a robust Entity and Attribute generation by
auto-populating much of the data's content and allowing the user to more 
easily define the attributes. 

File types that are currently supported for populating the Entity and Attribute tab are: 

-  Comma Separated Values (.csv)
-  Unformatted Texts Documents (.txt)
-  Excel Spreadsheet (.xls, .xlsx, .xlsm) 
-  Shapefile (.shp) 
-  GeoTIFF (.tif) 
-  JPEG (.jpg) 
-  Bitmap (.bmp) 
-  Disk Image File (.img) 
-  Portable Network Graphics (.png)
-  ASCII Grid (.grd) 
-  High Dynamic Range Image (.hdr)
-  ESRI ArcInfo Binary Grid (.adf)

Additional geospatial formats are available when calling the
MetadataWizard from the `ArcToolbox <../Installing%20ArcMap%20Toolbox.html>`_.

----------------------------------------------------------------------


**Given the diversity of data that can be described in a single Entity and attribute metadata section, here are some options for how to fill out this section:**

Data Described Elsewhere
---------------------------

The data are fully described in a data dictionary or other document that
can be referenced in this record.

    | *Leave the Detailed tab empty but fill out the Overview tab with a
      description of where one can obtain the appropriate data
      dictionary or other document. Make sure that the document being
      referenced is going to be persistent and easily available to all
      users of this data. If there is some question about this, consider
      including a copy of the data dictionary with this data/metadata.*
    | 

Data in a Proprietary or Complex Format
---------------------------------------

The data are in a proprietary format (for example, `Genbank <https://www.ncbi.nlm.nih.gov/books/NBK53707/>`_), 
organized in a complex but non-tabular format (folder with individual files that
adhere to a naming convention), or are easily described (a photo scan of a historic map).

    | *Leave the Detailed tab empty but fill out the Overview with a
      description of the data format, naming conventions, and/or contents.*
    | 

Single Tabular Dataset
----------------------

The data are tabular in nature (for example, CSV, shapefile attribute table, Excel
worksheet, raster attribute table) where each column represents an attribute,
each observation forms a row, and where the rows and columns together form a table.

      On the Detailed tab click the ‘Browse to Dataset’ button on the
      left and navigate to the data file. Appropriate content will be
      extracted from the file to fill the form. Sequentially fill out
      each of the columns on the right, by providing a definition of
      what is in that column. For each column also provide the Column
      Contents which will be one of:
	  
    | 1.  **Enumerated** for categorical or factor data, for which a definition will need to be provided for each unique value in the column (for example, data collected in binary (1 = Yes, 2 = No), or taxonomic abbreviations (URAM = Ursus americanus, or black bear)).
	  
    | 2.  **Range** for numerical, non-categorical data. A minimum value, maximum value, and the units of measure (where applicable) will be required (for example, elevation, and other measurements, or count data). 
	
    | 3.  **Codeset** for when the values can be obtained from a definitive source which is specified (for example, FIPS codes).
	  
    | 4. **Unrepresentable** for every other case where a free text description must be provided of how to interpret the values in this column (for example, names of people, or specific locations).
    

Multiple Tabular Datasets
-------------------------

The data consists of multiple distinct tabular datasets, for example,
several CSVs that contain related data or multiple sheets in an Excel workbook.

    Click the **Add Detailed** button at the bottom of the Instructions tab.