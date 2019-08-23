=======================================
Installing and Updating Python Packages
=======================================

The metadataWizard (as installed by the precompiled installers) comes with a complete, self contained Python 3.6 installation.
By default this will be in:
  - Windows: C:\\Users\\<<username>>\\AppData\\Local\\Programs\\MetadataWizard\\Python36_64
  - Mac: /Applications/MetadataWizard.app/Contents/Frameworks/pymdwizard_36/bin/python3.6m

You might need to update one of the existing packages, or install an additional package.  For example if you're using
the Jupyter Notebook/Lab feature and need another package installed, or need to upgrade an existing package to gain new functionality.


**Be aware, that changing or removing an existing library that the MetadataWizard depends on could render the MetadataWizard completely unusable.**
**This might be difficult or impossible to remedy, short of uninstalling and reinstalling the application completely.**

|

To open an Anconda prompt select 'Anaconda Prompt' from the Advanced Menu:

.. image:: ../img/AnacondaPrompt.png
   :width: 300pt

|

The cmd that opens will look like the system command prompt but have the standard conda commands available.
The (base) env that it is set to is the MetadataWizard's Python environment.

.. image:: ../img/AnacondaPrompt2.png
   :width: 900pt
   :align: left

|
