Contributing
============

Contributions are always welcome from the community. If you are interested in
contributing but intimidated or unsure how to get setup, please contact one
of the project maintainers for help and encouragement.


Issues
======
Questions and Bugs can be submitted on the GitHub [issues page][1]. Before creating 
a new issue, please take a moment to search open and closed issues
and make sure a similar issue does not already exist. If one does exist, you
can comment on the existing issue to show your support for that issue.


Code Conventions
================
All code is compatible with Python 2.7 and 3.4+.
We use [PEP8][2] conventions for all Python code, and recommend running 
a code checker prior to submitting a pull request.
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
We use the Anaconda distribution system for installation of the development 
environment, and recommend setting up a specific environment for this development effort.

see: ... for detailed instructions for setting up a development environment


 Running Tests
 =============
 cd into pymdwizard folder you're developing in
 py.test
 
 
 Building Docs
 =============
 cd into pymdwizard folder you're developing in
 sphinx-build -b html docs docs/html_output


[1]: https://github.com/usgs/fort-pymdwizard/issues
[2]: https://www.python.org/dev/peps/pep-0008/
[3]: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
[6]: https://pytest.org
[7]: https://help.github.com/articles/fork-a-repo/
[8]: https://help.github.com/articles/about-pull-requests/