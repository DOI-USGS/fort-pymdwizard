======================
Installing from Source
======================

Currently the only option for installation on Mac or Linux systems is to install the application from source.

Instructions for installing pymdwizard from source are intended for someone with at least a basic familiarity with Python and Python installations, but should be possible for someone with minimal experience to follow.

|
1.  Install `Anaconda <https://www.continuum.io/downloads>`_ or `Miniconda <https://conda.io/miniconda.html>`_.

	 *While the code for the MetadataWizard is 2-3 compatible, I would recommend installing the Python 3 version (64x), as 2.7 is being phased out.*
	  
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

        $ conda create -–name pymdwizard python=3.5 pyqt=5.6.0*
		
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
8. CD to the directory you want to install the actual wizard in:

	*Your directory below could be different depending on operating system or organization*

  .. code-block:: console

        $ cd c:/projects
		
|
9. clone our pymdwizard project:

  .. code-block:: console

        $ git clone https://github.com/talbertc-usgs/fort-pymdwizard.git
		
|
10. CD into our project folder:

  .. code-block:: console

        $ cd fort-pymdwizard
		
|
11. Install the rest of our requirements:

  .. code-block:: console

        $ conda install -–yes -–file requirements.txt
		
|
12. Add our git folder to the pythonpath:

  .. code-block:: console

        $ conda develop C:/projects/fort-pymdwizard
		
|
13. Launch the Wizard:

  .. code-block:: console

        $ python pymdwizard/gui/MainWindow.py


