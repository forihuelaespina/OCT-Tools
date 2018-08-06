# File: setup.py
#
# Code to compile OCT-Tools with py2exe
# 
# Initial example from:
#  http://www.py2exe.org/index.cgi/Tutorial
#
#
#
# @dateCreated: 5-Aug-2018
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 5-Aug-2018
#
# See also:
# 




#
# LOG:
#
# 5-Aug-2018: FOE:
#   * Initial script
#



# from distutils.core import setup
# import py2exe
# 
# setup(console=['run.py'])
# 


pyinstaller run.py

#pyinstaller --onefile run.py #To one file only