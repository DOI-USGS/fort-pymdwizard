
Adding icons to the resource file:

Add the icon png files to the resource file using the QtDesigner and one of the GRIT tools. Save.
Then use makepyqt.pyw, point to the icons folder, and build.
Copy the qrc_resource.py to resource_rc.py script to the root of the ui_files folder so each tool can find it.

Use IcoFX to create icon files
Use greenfish (transform) to rescale images