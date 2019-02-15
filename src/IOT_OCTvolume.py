"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: IOT_OCTvolume.py

Class IOT_OCTvolume

A set of OCT scans. All scans are of :class:`IOT_OCTscan`s.

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 26-Aug-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
|  2-Dec-2018 | FOE    | - Minor debugging.                                   |
+-------------+--------+------------------------------------------------------+
| 13-Dec-2018 | FOE    | - Remove importing of deprecated.                    |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import warnings


## Class definition
class IOT_OCTvolume(object):
    #Sphinx documentation
    """A set of :class:`IOT_OCTscan`s

    A set of :class:`IOT_OCTscan`s
    
    .. seealso:: :class:`IOT_OCTscan`
    .. note::
    .. todo::

    """

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = IOT_OCTvolume() - Creates an empty volume with no scans.
        
        """
        self.scans = list()
        return
        



    #Properties getters/setters
    @property
    def scans(self): #scans getter
        """
        The set of OCT scans.

        :getter: Gets the set of scans
        :setter: Sets the set of scans
        :type: list. All scans are of :class:`IOT_OCTscan`s
        
        .. seealso: :func:`IOT_OCTvolume.addScan`, :func:`IOT_OCTvolume.removeScan`, :func:`IOT_OCTvolume.clear`
        """
        return self.__scans


    @scans.setter
    def scans(self,*args): #scans setter
        tmpScanSet=args[0]
        if (not isinstance(tmpScanSet,(list,))):
            warnMsg = self.getClassName() + ':scans: Unexpected type. ' \
                            'Please provide a list of IOT_OCTscan.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__scans = list()
            for x in tmpScanSet:
                if (not isinstance(x,(IOT_OCTscan,))):
                    warnMsg = self.getClassName() + ':scans: Unexpected scan type ' \
                                'for object ' + x + '. Skipping object.'
                    warnings.warn(warnMsg,SyntaxWarning)
                else:
                    self.__scans.append(x)
        return None


    #Public methods
    def clear(self):
        """
        Clears the OCT volume; Removes all scans.
        
        :return: None
        """
        self.__scans = list()
        return None
    
    def addScan(self,theScan):
        """
        Add an OCT scan to the volume.
        
        :param theScan: The OCT scan.
        :type theScan: :class:`IOT_OCTscan`
        :return: None
        """
        if (not isinstance(theScan,(IOT_OCTscan,))):
            warnMsg = self.getClassName() + ':addScan: Unexpected scan type. ' \
                        'Nothing will be added.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__scans.append(theScan)
        return None
        
    
    
    def getScans(self,type):
        """
        Retrieves all scans in the volume of type t.
        
        :param t: Scan type 'A', 'B' or 'C'
        :type t: char
        :return: The set of A scans in the volume
        :rtype: list
        
        .. seealso:: :func:`IOT_OCTvolume.getVolume`
        """
        t=t.upper() #Uppercase
        theScans = list()
        for x in self.__scans:
            if (x.scantype==t):
                theScans.append(x)
        return theScans
        
    
    def getVolume(self,type):
        """
        Retrieves the (sub-)volume of scans of type t.
        
        :param t: Scan type 'A', 'B' or 'C'
        :type t: char
        :return: A volume with the set of scans of type t.
        :rtype: :class:`IOT_OCTvolume`

        .. seealso:: :func:`IOT_OCTvolume.getScans`
        """
        t=t.upper() #Uppercase
        theScans = IOT_OCTvolume()
        for x in self.__scans:
            if (x.scantype==t):
                theScans.addScan(x)
        return theScans
        
    

