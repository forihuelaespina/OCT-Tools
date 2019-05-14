:: File: OCTantApp.bat
:: 
:: .bat launcher for OCTant application (previously OCTToolsApp)
:: 
:: For some reason, the installer does everything ok, but then "double
:: clicking" the OCTantApp.launch.py is unable to find Python.exe
:: or pythonw.exe. This .bat file only makes the familiar "double clicking"
:: a reality.
:: 
:: 
:: @author: Felipe Orihuela-Espina
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
:: 17-Mar-2019: FOE:
::	* File renaming to OCTantApp.bat (from OCTToolsApp.bat). Rebranding to
::  OCTant and updated comments.
::


:: Do not display commands, only echo prints
echo off
title OCTantApp
echo OCTant: Setting up things. Please wait...

:: Launch the application
Python.exe OCTant.launch.py
IF %ERRORLEVEL% NEQ 0 (
	::echo %ERRORLEVEL%
	echo.
	echo Unable to find Python in the system; trying local copy.
	Python\Python.exe OCTantApp.launch.py
)