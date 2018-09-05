# File: setup.py
#
# Code to compile OCT-Tools
# 
#
#
# @dateCreated: 5-Aug-2018
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 3-Sep-2018
#
# See also:
# 




#
# LOG:
#
# 5-Aug-2018: FOE:
#   * Initial script
#
# 3-Sep-2018: FOE:
#   * Updated according to: https://packaging.python.org/tutorials/packaging-projects/
#



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


# See: https://packaging.python.org/tutorials/packaging-projects/
setuptools.setup(
    name="OCTToolsApp",
    version="0.1",
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


#pyinstaller run.py
# #pyinstaller --onefile run.py #To one file only