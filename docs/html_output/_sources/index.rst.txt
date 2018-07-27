.. image:: img/TitleBanner.png
   :width: 600pt
   :align: left

==========================================
MetadataWizard User Guide
==========================================
The Metadata Wizard is a user-friendly desktop application for creating, editing, 
and validating metadata that conforms to the Content Standard for Digital 
Geospatial Metadata (CSDGM) version 2.0. The Federal Geographic Data Committee 
(FGDC) has authored and endorsed this metadata standard as well as other standards. 
Metadata provides information about a data set, allowing data users to understand 
and appropriately use the data in different contexts. Metadata is crucial to support 
searchable information about data that otherwise is not directly incorporated within 
data and therefore undiscoverable. Metadata in its most basic form includes 
information about the data’s origin, creators, accuracy, availability, and 
distribution. Metadata is necessary for the appropriate interpretation and reuse of 
the data, and importantly provides the necessary definitions of data content. The
`Metadata section <https://www2.usgs.gov/datamanagement/describe/metadata.php>`_ 
of the USGS Data Management website has information on helpful metadata resources, 
as well as best practices for metadata creation.

The Metadata Wizard is designed to better standardize the workflow of metadata creation 
and decrease the user's level of effort to develop high quality and compliant CSDGM 
metadata. We accomplish this, in part by auto-capturing content from a dataset, 
pre-populating a record with reasonable defaults, and reducing the expertise level 
needed to create a high-quality metadata record. It provides an efficient and pleasant 
metadata experience for a wide range of users from scientists to data managers. 

Users should be advised that information not stored in CSDGM elements (such as custom 
elements, or elements belonging to different standards) will be lost upon saving in the 
Metadata Wizard. Users should also exercise caution with metadata records that contain 
information in less-used CSDGM elements that are not accessible in the tool. `Effort has 
been made <https://github.com/usgs/fort-pymdwizard/issues/6>`_ to retain information 
stored in some of these elements, but no guarantee can be made that information stored in 
elements not accessible in the tool will be retained.

This software was engineered as an open-source evolution of the original 
`MetadataWizard <https://www.sciencebase.gov/catalog/item/50ed7aa4e4b0438b00db080a>`_ 
to support metadata creation outside of the Environmental Systems Research Institute 
(ESRI) software environment.

The Metadata Wizard software was developed and is currently maintained by the Data 
Management Team at the U.S. Geological Survey (USGS) Fort Collins Science Center. 
We also worked with incorporating feedback from within other USGS science centers 
during the software’s infancy.

Installation Methods
====================

.. toctree::
   :maxdepth: 1

   Windows Installation
   Mac Installation
   Installing from Source
   Installing ArcMap Toolbox
   
Standard Usage
===============

.. toctree::
   :maxdepth: 1

   usage/File Management, New, Open, Save, Save as....
   Getting Software Updates
   usage/Using the Metadata Wizard
   usage/Spatial Content
   usage/How to fill out the Entity and Attribute tab
   usage/Generating a Taxonomic Information Section
   usage/Previewing a Record
   usage/Validating a Record
   


Advanced Usage
=================

.. toctree::
   :maxdepth: 1

   advancedusage/Metadata Review Report
   advancedusage/Settings
   advancedusage/Changing Your Template
   advancedusage/Launch Jupyter for Batch Processing
   advancedusage/Include Sections
   
Help Improve the Tool
========================

.. toctree::
   :maxdepth: 1

   Reporting Bugs and Enhancement Ideas


