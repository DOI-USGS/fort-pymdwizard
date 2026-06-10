Contributing
============

Contributions are always welcome from the community. If you are interested in
contributing but intimidated or unsure how to get setup, please contact one
of the project maintainers for help and encouragement.


Issues
======
Questions and Bugs can be submitted on the GitHub [issues page][1].


Code Conventions
================
We use [PEP8][2] conventions for all Python code, and recommend running 
a code checker prior to submitting a pull request. Black is the recommended
code formatter.

For docstrings we're using the [numpy format][3]
We use [pytest][6] for all testing and will require tests for new features.


Git Conventions
===============
Prior to contributing you will need to [create a GitHub fork][7] of the project that
you will be pushing your changes to.

Create a new branch in your fork with a name that describes the feature or bug
you'll be addressing.

Create a [GitHub pull request][8] early in the process so that the project maintainers
will be aware of your effort and able to coordinate your changes with current
development.

Development Environment
=======================
We use the Conda distribution system for installation of the development 
environment, and recommend setting up a specific environment for this development effort.

Use the file fort-pymdwizard/environment.yml to install requirements in new dev environments.


 Running Tests
 =============
 cd into pymdwizard folder you're developing in
 py.test
 
 
 Building Docs
 =============
 cd into pymdwizard folder you're developing in
 sphinx-build -b html docs docs/html_output


[1]: https://github.com/DOI-USGS/fort-pymdwizard/issues
[2]: https://www.python.org/dev/peps/pep-0008/
[3]: https://numpydoc.readthedocs.io/en/latest/format.html
[6]: https://pytest.org
[7]: https://docs.github.com/en/get-started/quickstart/fork-a-repo
[8]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
