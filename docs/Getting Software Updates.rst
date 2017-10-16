============
Getting Software Updates
============

The Metadata Wizard is set up to easily download and install updates directly from this GitHub repository. For this to work, the application must be installed in a location that the current user has write access to. If the application was installed with elevated or admin privileges (i.e. in the “C:\\Program Files” directory), this will not work unless the application is being run with elevated privileges when updating.

.. figure:: img/update.png
	:alt: Getting software updates
|	
**To update the application, click ‘Check for Updates’ in the ‘Help’ menu item at the top of the application.** A message box will pop up notifying you of the result of update. If an update was made, you will need to restart the application to see it.

|
|  **Technical note:**
Updates are made using simple git commands to **fetch** and **merge** the master branch from this GitHub repository. The commands to execute this operation are stored in a file called “update\_wizard.bat” in the application’s install folder. Other issues that might prevent this update from working include:

-  Edited or otherwise changed files in the local installation directory (merge conflict)
-  Internet connectivity issues
-  Firewalls or other security measures

Users with knowledge of GIT can troubleshoot these problems directly in the project’s GIT repository.