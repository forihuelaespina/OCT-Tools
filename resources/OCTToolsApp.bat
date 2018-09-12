:: File: OCTToolsApp.bat
:: 
:: .bat launcher for OCT-Tools
:: 
:: For some reason, the installer does everything ok, but then "double
:: clicking" the OCTToolsApp.launch.py is unable to find Python.exe
:: or pythonw.exe. This .bat file only makes the familiar "double clicking"
:: a reality.
:: 
:: 
:: @dateCreated: 9-Sep-2018
:: @authors: Felipe Orihuela-Espina
:: @dateModified: 11-Sep-2018
:: 
:: See also:
:: 


:: LOG
::
:: 9-Sep-2018: FOE:
::	* File created
::
:: 11-Sep-2018: FOE:
::	* Added conditional for running either Python.exe or Python/Python.exe. It
::	just seems to be different depending on the machine.
::  


:: Do not display commands, only echo prints
echo off
title OCTToolsApp
echo OCT-Tools: Setting up things. Please wait...

:: Launch the application
Python.exe OCTToolsApp.launch.py
IF %ERRORLEVEL% NEQ 0 (
	::echo %ERRORLEVEL%
	echo.
	echo Unable to find Python in the system; trying local copy.
	Python/Python.exe OCTToolsApp.launch.py
)