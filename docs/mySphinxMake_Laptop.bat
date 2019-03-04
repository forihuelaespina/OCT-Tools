:: File: mySphinxMake_Laptop.bat
::
:: .bat maker of Sphinx documentation
::
:: Compiles sphinx documentation.
:: Run this from an Anaconda command prompt.
::
::
:: @dateCreated: 22-Sep-2018
:: @authors: Felipe Orihuela-Espina
:: @dateModified: 24-Sep-2018
::
:: See also:
::

SET MYPROJECTPATH=C:\Users\Felipe\OneDrive\Git\OCTant

:: First, run sphinx-apidoc  to generate the .rst files for autodoc
::
:: http://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
:: http://www.sphinx-doc.org/en/1.4/man/sphinx-apidoc.html
::
:: Repeat the sphinx-apidoc statement below for other packages
::

:: Package octant
C:\ProgramData\Anaconda3\Scripts\sphinx-apidoc -f -M -a -e ^
-A "Felipe Orihuela-Espina" ^
--tocfile octantPackageTOC ^
-o %MYPROJECTPATH%\docs\source ^
%MYPROJECTPATH%\src\octant ^
%MYPROJECTPATH%\src\octant\*.spec

:: %MYPROJECTPATH%\src\octant\panorama.py ^
:: %MYPROJECTPATH%\src\octant\Test.py ^
:: %MYPROJECTPATH%\src\octant\setup.py ^
:: %MYPROJECTPATH%\src\octant\segmentationUtils.py ^
:: %MYPROJECTPATH%\src\octant\*.spec

:: Package app
C:\ProgramData\Anaconda3\Scripts\sphinx-apidoc -f -M -a -e ^
-A "Felipe Orihuela-Espina" ^
--tocfile appPackageTOC ^
-o %MYPROJECTPATH%\docs\source ^
%MYPROJECTPATH%\src\app ^
%MYPROJECTPATH%\src\app\*.spec

:: %MYPROJECTPATH%\src\app\panorama.py ^
:: %MYPROJECTPATH%\src\app\Test.py ^
:: %MYPROJECTPATH%\src\app\setup.py ^
:: %MYPROJECTPATH%\src\app\segmentationUtils.py ^
:: %MYPROJECTPATH%\src\app\*.spec

:: Now build sphinx
C:\ProgramData\Anaconda3\Scripts\sphinx-build -b html C:\Users\Felipe\OneDrive\Git\OCTant\docs\source C:\Users\Felipe\OneDrive\Git\OCTant\docs\build
