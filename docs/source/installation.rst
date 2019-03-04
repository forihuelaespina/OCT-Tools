.. _rst-installation:

Installation
============

.. _sec_instalar:

Installing OCT-Tools:
---------------------

1) Download the latest installer from `GitHub <https://github.com/forihuelaespina/OCTant/tree/master/build>`_.
2) Unzip the installer anywhere
3) Double click in OCTantApp_vX.X.exe
4) Follow on screen instructions

Ready to go!

If you are updating an installation, please uninstall your previous version
before installing the new one.


.. _sec_FixLaunchShortcuts:

Fixing shortcuts
^^^^^^^^^^^^^^^^

When everything is installed, the installer will generate 2 shortcuts for
launching the application.
Currently, these shortcuts will not work properly from install because
of a limitation with the packaging tool (pynsist / nsis).
Fortunately it is very easy to fix manually.
Find your installation folder, and there find the .bat file. In the Windows
application menu, look for OCTToolsApp and you may right click on the .bat
shortcut.


.. note:: The shortcuts do not work because the "Start from" field points to
    %HOMEDRIVE%%HOMEPATH% and these do not expand. Further, the
    "Start from" field cannot be configured directly from pynsist.


#. After installation, in the Windows Init menu, right click over the shortcut.
#. More -> Open the file location
#.  Select the link (.bat) with the right click and select Properties
#. Edit the field "Start from" and set it to the installation folder (whichever you have chosen).

This won't affect the installation, just the shortcut!

Once the change has been made, you should be able to launch the application from the .bat shorcut.


.. hint:: Finding the installation folder: While you were installing the application,
    in one of the steps, you were asked to confirm your installation folder.
    If you forgot to make note of this installation path, likely candidates are:

    * If you opted for an installation for a single user e.g. you; "C:\Users\<USERNAME>\AppData\Local\OCTantApp\"
    * If you opted for an installation for all users; "C:\Program Files\OCTantApp\". A variant may include a "(x86)" after "Program Files"

    To know for sure;

    * Open a file explorer windows. Go to "C:\" and try to navigate to either of the above paths.
    * If none are available, in the task bar search OCTantApp and wait a few seconds. Windows would find the folder for you. Then, right click and "Open the folder location".




.. _sec_launchApp:

Launching OCT-Tools:
--------------------

* If you have made the change to the shortcut as explained above, double click the fixed shortcut.
* If you haven't made the changes to the shortcut, open a file explorer window, navigate to the installation folder and double click on the .bat shortcut.
