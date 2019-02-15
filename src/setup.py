"""
-*- coding: utf-8 -*-

File: setup.py

Code to compile OCT-Tools

:Log:

+-------------+--------+------------------------------------------------------+   
| Date        | Author | Description                                          |
+=============+========+======================================================+
|  5-Aug-2018 | FOE    | - Initial script.                                    |
+-------------+--------+------------------------------------------------------+   
|  3-Sep-2018 | FOE    | - Updated according to:                              |
|             |        | https://packaging.python.org/tutorials/packaging-projects/ |
+-------------+--------+------------------------------------------------------+   
| 13-Feb-2019 | FOE    | - Updated version to __version__                     |
|             |        | (NOTE: variable __version__ imported in __init__.py) |
|             |        | - Comments updated to Sphinx style.                  |
+-------------+--------+------------------------------------------------------+   



.. seealso:: None
.. note:: None
.. todo:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Compiling with setuptools and wheels:
#
# Run this command from the same directory where setup.py is located:
#
# python setup.py sdist bdist_wheel
#
# This command should generate two files in the dist/ directory.
#
# dist/
#  example_pkg-0.0.1-py3-none-any.whl
#  example_pkg-0.0.1.tar.gz
#
# The tar.gz file is a source archive whereas the .whl file is a built
# distribution.


import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

exec(open('src/version.py').read())

# See: https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name="OCTToolsApp",
    version=__version__,
    author="Felipe Orihuela-Espina; Arlem Aleida Castillo Ávila",
    author_email="f.orihuela-espina@inaoep.mx",
    description="A suite of tools for segmenting retinal OCT tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


## Compiling with py2exe
# 
# Initial example from:
#  http://www.py2exe.org/index.cgi/Tutorial
#

# from distutils.core import setup
# import py2exe
# 
# setup(console=['run.py'])
# 


## Compiling with pyinstaller
# To generate the .exe and the distribution from a miniconda cmd at the
#directory where this setup-py is, and with admin permissions run:
#
# To one folder
pyinstaller --onedir --noconfirm --nowindow ^
--hidden-import tkinter ^
--hidden-import scipy ^
--hidden-import scipy._lib.messagestream ^
--hidden-import pywt._extensions._cwt ^
--hidden-import PyQt5.sip ^
--distpath ..\dist\pyinstaller\ ^
--workpath ..\build\pyinstaller\ ^
--icon=..\resources\inaoe.ico ^
-d ^
OCTToolsApp.py
# Esta de arriba me lleva al siguiente error en tiempo de ejecución:
#
# This application failed to start because it could not find or load the Qt platform plugin "windows" in "".
# Reinstalling the application may fix this problem.
#
# Ni idea de como corregirlo!
#

# To one file
#pyinstaller --onefile --distpath ../dist/ --workpath ../build/pyinstaller/ --no-confirm OCTToolsApp.py