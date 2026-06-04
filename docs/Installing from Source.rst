=======================================
Installing from Source (Windows, Linux)
=======================================

These instructions are for installing pymdwizard from source on Windows, Linux.

Instructions for installing pymdwizard from source are intended for someone with a basic familiarity with Python and conda package installations.

|

1.  Install `Miniforge <https://conda-forge.org/download/>`_.

    Miniforge is a minimal conda installer that uses conda-forge as the default channel.
    Download the appropriate installer for your operating system (Windows, Linux, or Mac) and follow the installation instructions.

|

2.  Open the Miniforge command prompt:

    * **Windows**: Launch "Miniforge Prompt" from the Start menu
    * **Linux/Mac**: Open a terminal (conda will be available in your shell if you selected the option during installation)

|

3.  Navigate to the directory where you want to install the Metadata Wizard:

    *The example directory below could be different depending on operating system or organization*

  .. code-block:: console

        $ cd c:/projects

|

4. Clone the fort-pymdwizard project:

  .. code-block:: console

        $ git clone https://github.com/talbertc-usgs/fort-pymdwizard.git

|

5. Navigate to the project folder:

  .. code-block:: console

        $ cd fort-pymdwizard

|

6. Create the pymdwizard conda environment from the environment.yml file:

   This will create an environment with Python 3.13 and all required dependencies.

  .. code-block:: console

        $ conda env create -f environment.yml


7. Activate the environment:

   *(Works on all platforms - Windows, Linux, and Mac)*

  .. code-block:: console

        $ conda activate pymdwizard

|

8. Add the project folder to the Python path:

  .. code-block:: console

        $ conda develop .

   *Note: Use your full path if the relative path doesn't work, e.g., `conda develop C:/projects/fort-pymdwizard`*

|

9. Launch Metadata Wizard:

  .. code-block:: console

        $ python pymdwizard/gui/MainWindow.py


