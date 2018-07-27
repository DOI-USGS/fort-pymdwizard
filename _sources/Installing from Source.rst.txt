=======================================
Installing from Source (Windows, Linux)
=======================================

These instructions do not currently work on Mac computers, but will be updated
in a subsequent release to support Macs.

Currently the only option for installation on Linux systems is to install the application from source.

Instructions for installing pymdwizard from source are intended for someone with a basic familiarity with Python and Python Package installations.

|

1.  Install `Anaconda <https://www.continuum.io/downloads>`_ or `Miniconda <https://conda.io/miniconda.html>`_.

	 *While the code for the MetadataWizard is  compatible with both Python versions 2 and 3, installing the Python 3 version (64x) is recommended, as 2.7 is being phased out.*
	  
|

2.  Open the Anaconda command window.

|

3.  Add the conda-forge channel:

  .. code-block:: console

        $ conda config --add channels conda-forge		

|

4.  Install the optional conda developer tools

  .. code-block:: console

        $ conda install conda-build
		
|

5.  Create a pymdwizard environment:

  .. code-block:: console

        $ conda create --name pymdwizard python=3.6 pyqt=5.6.0*
		
|

6. Activate this environment:

| *(on Windows)*

  .. code-block:: console

        $ activate pymdwizard
	
	
| *(on Linux, Mac)*  
 
  .. code-block:: console

        $ source activate pymdwizard
		
|

7. Install git:

  .. code-block:: console

        $ conda install git
		
|

8. Navigate to the directory where the Metadata Wizard will be installed:

	*The example directory below could be different depending on operating system or organization*

  .. code-block:: console

        $ cd c:/projects
		
|

9. Clone our pymdwizard project:

  .. code-block:: console

        $ git clone https://github.com/talbertc-usgs/fort-pymdwizard.git
		
|

10. Navigate to our project folder:

  .. code-block:: console

        $ cd fort-pymdwizard
		
|

11. Install the remaining software requirements (library dependencies):

  .. code-block:: console

        $ conda install --yes --file requirements.txt
		
|

12. Add our git folder to the pythonpath:

  .. code-block:: console

        $ conda develop C:/projects/fort-pymdwizard
		
|

13. Launch Metadata Wizard:

  .. code-block:: console

        $ python pymdwizard/gui/MainWindow.py


