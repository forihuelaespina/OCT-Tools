# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:03:24 2019

File: Settings.py

Class Settings

A class to hold a list of settings.  


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 10-Mar-2019 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 15-Mar-2019 | FOE    | - Opted for file format to be in JSON.               |
|             |        | - Methods _isempty, _parseField removed.             |
|             |        | - Method read now uses json library and jsonminify   |
|             |        |   util.                                              |
|             |        | - Added method write.                                |
+-------------+--------+------------------------------------------------------+



.. seealso:: None
.. note:: None
.. todo:: Control of value settings capabilities. Currently, all value
    settings are permitted.

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
import numpy as np
import os
import json
from datetime import datetime

from octant import version
from octant.util import jsonminify, fastjsonminify



## Class definition
class Settings(object):
    #Sphinx documentation
    """A class to hold a list of settings.
    
    A class to hold a list of settings. A list of settings is the classical
    "dictionary" (see note below on python's dict) of pairs key:value
    but with some additional capabilities. In particular, the class provides
    additional file reading and writing capabilities so that settings can
    be read to and from plain text files, as well as some value setting
    checking capabilities.
    
    The class is intended to behave like a dynamic struct
    where properties of the class, i.e. new settings, can be declared
    "on-the-fly" instead of being predefined.
    Although, creating a dynamic struct class in python itself is trivial
    (see https://stackoverflow.com/questions/1878710/struct-objects-in-python ),
    but because of the additional capabilities, hence the convenience of
    the class.
    
    .. Background:
        
    MATLAB's struct allows this "on-the-fly" field declaration on the fly.
    Python's built-in dictionary is not exactly a match because of the 
    required syntax i.e. ``mySettingsObj['fieldname']`` instead of
    ``mySettingsObj.fieldname`` and the inability to control value settings.
    
    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """

    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self, **kwargs):
        """The class constructor.
        """

        #Call superclass constructor
        
        
        #Initialize private attributes unique to this instance

        self.__dict__.update(kwargs) #Permits direct declaration of
                                     #key:value pairs from declaration, e.g.
                                     # x = Settings(foo=1, bar=2)
                                     #See: https://stackoverflow.com/questions/1878710/struct-objects-in-python

        return
        
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method


    #Private methods
    def __str__(self):
        """Provides the string representation of the object.

        :returns: The object representation as a string.
        :rtype: str
        """
        s = '<' + self.getClassName() + ': '
        s = s + str(self.__dict__)
        s = s + '>'
        return s    
    

    #Public methods
    def getClassName(self):
        """Retrieves the class name.

        :returns: The class name.
        :rtype: str
        """
        return type(self).__name__
    
    
    def read(self,filename):
        """Read settings from JSON file.
 
        :param filename: The name of the file to be read (including path)
        :type filename: str
        :returns: True if file was sucessfully read. False otherwise.
        :rtype: bool
        """
        
        with open(filename, 'r') as file:
            contentStr = file.read()
        
        #c=json.loads(jsonminify(content))
        contentDict=json.loads(fastjsonminify(contentStr))
            #c contains a dictionary that has to be
            #traspassed to self
            
        #Loop over the dictionary
        for fieldName, fieldValue in contentDict.items():
            setattr(self, fieldName, fieldValue)
        
        return True
    
   
    def write(self,filename):
        """Write settings to a JSON file.
    
        :returns: True if file was sucessfully read. False otherwise.
        :rtype: bool
        """
        contentStr = json.dumps(self.__dict__)
        with open(filename, 'w') as file:
            file.write('# \n')
            file.write('# File: ' + filename + '\n')
            file.write('# \n')
            file.write('# This is an OCTant settings file.\n')
            file.write('# You can add, edit or remove settings manually here.\n')
            file.write('# File format is in JSON. Although comments are permitted, but they will be lost after resaving because of minification.\n')
            file.write('# If you want your comments to be persistent declared them as "__comment" fields.\n')
            file.write('# \n')
            file.write('# File last saved: ' + datetime.utcnow().strftime('%d-%b-%Y %H:%M:%S UTC+0') + '\n')
            file.write('# \n')
            file.write('# (c) 2019. OCTant. Felipe Orihuela-Espina.\n')
            file.write('# \n\n')
            file.write(contentStr)
        return True
    