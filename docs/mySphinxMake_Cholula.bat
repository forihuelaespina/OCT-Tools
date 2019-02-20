:: File: mySphinxMake_Cholula.bat
::
:: .bat maker of Sphinx documentation
::
:: Compiles sphinx documentation.
:: Run this from an Anaconda command prompt.
::
::
:: @dateCreated: 22-Sep-2018
:: @authors: Felipe Orihuela-Espina
:: @dateModified: 19-Feb-2019
::
:: See also:
::

SET MYPROJECTPATH=C:\Users\fo067\OneDrive\Git\OCT-Tools

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
C:\ProgramData\Anaconda3\Scripts\sphinx-build -b html C:\Users\fo067\OneDrive\Git\OCT-Tools\docs\source C:\Users\fo067\OneDrive\Git\OCT-Tools\docs\build
