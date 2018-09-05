# File: __init__.py
#
# This file is necessary to compile python as a package (not a module)
#
#
# From: https://stackoverflow.com/questions/448271/what-is-init-py-for
# The __init__.py is required to make Python treat the directories as
# containing packages; this is done to prevent directories with a common
# name, such as string, from unintentionally hiding valid modules that
# occur later (deeper) on the module search path. In the simplest case,
# __init__.py can just be an empty file, but it can also execute
# initialization code for the package or set the __all__ variable.
# 
#
#
#
# @dateCreated: 3-Sep-2018
# @authors: Felipe Orihuela-Espina
# @dateModified: 3-Sep-2018
#
# See also:
# 

name = "OCTToolsApp"