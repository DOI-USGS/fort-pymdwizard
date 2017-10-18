Batch Processing using Jupyter and Python
*****************************************

Some data management or metadata tasks can best be tackled by writing a script
to automate processes that are repetitive or repeated regularly.
Since the Metadata Wizard is built on, and ships with a fairly complete
Python stack, we allow advanced users to leverage this functionality using a Jupyter Notebook.

Prerequisites
-------------

Use of scripting, as described below, will require a basic knowledge of
the `Python programing language <https://www.python.org/>`_ as well as how to use `Jupyter Notebooks <http://jupyter.org/>`_.
There are many excellent resources for learning these powerful tools such as:

-  `Software Carpentry <http://swcarpentry.github.io/python-novice-inflammation/>`_
-  `Code Acadamy <https://www.codecademy.com/learn/learn-python>`_
-  `Google's Python Class <https://developers.google.com/edu/python/>`_

|
Launching Jupyter from the Wizard
---------------------------------

A live instance of a Jupyter Notebook kernel can be launched directly from the Metadata Wizard 2.0 application by clicking **Launch Jupyter** in the **Advanced** menu.

.. figure:: ../img/JupyterLaunchMenu.png
	:alt: Launch Jupyter Menu Item

	Menu item to Launch Jupyter

|

The user will be asked where they would like to open Jupyter.  If you are just
getting started or want to take a look at the examples, choose the default directory.
If you are working on a project, you can browse to a different directory.
The Notebooks you produce will get written to this location.

.. figure:: ../img/JupyterBrowse.png
	:alt: Launch Jupyter Browse

	Prompt for choosing where to start the Notebook server

Example Notebooks
-----------------

The Metadata Wizard 2.0 ships with a set of example Notebooks that are intended to
provide a demonstration of how one might use these capabilities.  Each is self
documenting, in that it contains internal explanations of the code contained in
it's cells.


**pymdwizard scripting (Start Here).ipynb**  -- Provides a introduction to
general opening, searching, editing, saving, and validation of FGDC metadata.
It uses the pymdwizard's core functionality and is probably where most users
will want to start.

**Report on all metadata in a directory.ipynb**  -- Provides an example of how one might
generate a report on all the metadata contained in a directory including the FGDC schema
errors in each file.

**FGDC ITIS Taxonomy generation.ipynb**  -- Provides an example of how to use the
core functionality to search the Integrated Taxonomic Information System (ITIS)
by scientific and common name and generate FGDC taxonomy sections in code.

**BatchUpdateAuthorsDatesEtc.ipynb**  -- Provides a real world example of how the
above techniques were used to update a large batch of existing metadata records.

**---TBD---.ipynb**  -- Provides a real world example of how we extended the
above techniques to generate metadata for multiple datasets and moved the associated
data and metadata up to an online repository (A Data Release on the USGS ScienceBase system).

