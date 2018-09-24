:: File: mySphinxMake_Laptop.bat
::
:: .bat maker of Sphinx documentation
::
:: Compiles sphinx documentation.
::
::
:: @dateCreated: 22-Sep-2018
:: @authors: Felipe Orihuela-Espina
:: @dateModified: 24-Sep-2018
::
:: See also:
::

SET MYPROJECTPATH=C:\Users\Felipe\OneDrive\Git\OCT-Tools

:: First, run sphinx-apidoc  to generate the .rst files for autodoc
::
:: http://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
:: http://www.sphinx-doc.org/en/1.4/man/sphinx-apidoc.html
::
:: Repeat the sphinx-apidoc statement below for other packages
::
:: Package src
C:\ProgramData\Miniconda3\Scripts\sphinx-apidoc -f -M -a -e ^
-A "Felipe Orihuela-Espina" ^
--tocfile srcPackageTOC ^
-o %MYPROJECTPATH%\docs\source ^
%MYPROJECTPATH%\src ^
%MYPROJECTPATH%\src\panorama.py ^
%MYPROJECTPATH%\src\Test.py ^
%MYPROJECTPATH%\src\setup.py ^
%MYPROJECTPATH%\src\segmentationUtils.py ^
%MYPROJECTPATH%\src\*.spec

:: Now build sphinx
C:\ProgramData\Miniconda3\Scripts\sphinx-build -b html C:\Users\Felipe\OneDrive\Git\OCT-Tools\docs\source C:\Users\Felipe\OneDrive\Git\OCT-Tools\docs\build
