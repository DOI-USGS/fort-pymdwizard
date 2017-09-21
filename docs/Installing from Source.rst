============
Installing from Source
============

Currently the only option for installation on Mac or Linux systems is to install the application from source.
|
Instructions for installing pymdwizard from source are intended for someone with at least a basic familiarity with Python and Python installations, but should be possible for someonewith minimal experience to follow.


1. Install Anaconda or Miniconda
      (https://www.continuum.io/downloads or
      https://conda.io/miniconda.html). While the code is 2-3 compatible
      I would recommend installing the Python 3 version (64x), as 2.7 is
      being phased out.
      :name: install-anaconda-or-miniconda-httpswww.continuum.iodownloads-or-httpsconda.iominiconda.html.-while-the-code-is-2-3-compatible-i-would-recommend-installing-the-python-3-version-64x-as-2.7-is-being-phased-out.
|
2. Open the Anaconda command window
      :name: open-the-anaconda-command-window
|
3. Add the conda-forge channel:
      :name: add-the-conda-forge-channel
|
   ``conda config --add channels conda-forge``
|
4. Install the optional conda developer tools
      :name: install-the-optional-conda-developer-tools
|
   ``conda install conda-build``
|
5. Create a pymdwizard environment:
      :name: create-a-pymdwizard-environment
|
   *conda create –name pymdwizard python=3.5 pyqt=5.6.0*
|
6. Activate this environment:
      :name: activate-this-environment
|
   | *(on Windows)*
   | ``activate pymdwizard``
   | *(on Linux, Mac)*
   | ``source activate pymdwizard``
|
7. Install git:
      :name: install-git
|
   *conda install git*
|
8. CD to the directory you want to install the actual wizard
      in:
      :name: cd-to-the-directory-you-want-to-install-the-actual-wizard-in
|
   *cd c:\\projects*
|
9. clone our pymdwizard project:
      :name: clone-our-pymdwizard-project
|
   \_git clone https://github.com/talbertc-usgs/fort-pymdwizard.git_
|
10. CD into our project folder:
      :name: cd-into-our-project-folder
|
   *cd fort-pymdwizard*
|
11. Install the rest of our requirements:
      :name: install-the-rest-of-our-requirements
|
   *conda install –yes –file requirements.txt*
|
12. Add our git folder to the pythonpath:
      :name: add-our-git-folder-to-the-pythonpath
|
   *conda develop C:\\projects\\fort-pymdwizard*
|
13. Launch the Wizard:
      :name: launch-the-wizard
|
   *python pymdwizard\\gui\\MainWindow.py*
