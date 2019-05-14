"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: OCTvolume.py

Class OCTvolume

A set of OCT scans. All scans are of :class:`OCTscan`.

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
| 19-Feb-2018 | FOE    | - Bug fixed. Importing of IOT_OCTscan.               |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded OCTvolumne. The prefix             |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
+-------------+--------+------------------------------------------------------+
| 25-Mar-2019 | FOE    | - Changed calls to isinstance for calls to type.     |
|             |        | - Added method getClassName.                         |
|             |        | - Added method addScans.                             |
|             |        | - Added method getNScans.                            |
|             |        | - Deprecated method addScan.                         |
+-------------+--------+------------------------------------------------------+
| 30-Mar-2019 | FOE    | - Bug fixed. Importing deprecation.                  |
|             |        | - Bug fixed. Imports __version__ instead of version. |
|             |        | - Bug fixed. flagAllOCTScans in method addScans is   |
|             |        |   now correctly returned in all cases.               |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import warnings
import deprecation

from octant import __version__
import octant.data as octant

## Class definition
class OCTvolume(object):
    #Sphinx documentation
    """A set of :class:`octant.data.OCTscan`

    A set of :class:`octant.data.OCTscan`
    
    .. seealso:: :class:`octant.data.OCTscan`
    .. note:: None
    .. todo:: None

    """

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = OCTvolume() - Creates an empty volume with no scans.
        
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
        :type: list. All scans are of :class:`octant.data.OCTscan`
        
        .. seealso:: :func:`octant.data.OCTvolume.addScan` , :func:`octant.data.OCTvolume.removeScan` , :func:`octant.data.OCTvolume.clear`
        
        """
        return self.__scans


    @scans.setter
    def scans(self,*args): #scans setter
        tmpScanSet=args[0]
        if type(tmpScanSet) is not list:
            warnMsg = self.getClassName() + ':scans: Unexpected type. ' \
                            'Please provide a list of octant.data.OCTscan.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__scans = list()
            for x in tmpScanSet:
                if type(x) is not octant.OCTscan:
                    warnMsg = self.getClassName() + ':scans: Unexpected scan type ' \
                                'for object ' + x + '. Skipping object.'
                    warnings.warn(warnMsg,SyntaxWarning)
                else:
                    self.__scans.append(x)
        return None


    #Public methods
    def getClassName(self):
        return type(self).__name__
    
    def clear(self):
        """
        Clears the OCT volume; Removes all scans.
        
        :return: None
        """
        self.__scans = list()
        return None
    
    
    @deprecation.deprecated(deprecated_in="0.3", removed_in="1.0",
                        current_version=__version__,
                        details="Use method addScans() instead.")
    def addScan(self,theScan):
        """
        Add an OCT scan to the volume.
        
        :param theScan: The OCT scan.
        :type theScan: :class:`octant.data.OCTscan`
        :return: None
        """
        if type(theScan) is not octant.OCTscan:
            warnMsg = self.getClassName() + ':addScan: Unexpected scan type. ' \
                        'Nothing will be added.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__scans.append(theScan)
        return None
        
    
    def addScans(self,theScans):
        """
        Add one or more OCT scans to the volume at once.
        
        :param theScans: The list of OCT scans.
        :type theScan: list of :class:`octant.data.OCTscan` or
            single :class:`octant.data.OCTscan`
        :return: True if scans added, False otherwise.
        """
        flagAllOCTscans=True
        if type(theScans) is octant.OCTscan:
            self.__scans.append(theScans)
        elif type(theScans) is list:
            for elem in theScans:
                if type(elem) is not octant.OCTscan:
                    warnMsg = self.getClassName() + ':addScans: Unexpected scan type. ' \
                                'Nothing will be added.'
                    flagAllOCTscans=False
                    break
            if flagAllOCTscans:    
                self.__scans.extend(theScans)
        return flagAllOCTscans
            
   
    def getScans(self,t):
        """
        Retrieves all scans in the volume of type t.
        
        :param t: Scan type 'A', 'B' or 'C'
        :type t: char
        :return: The set of A scans in the volume
        :rtype: list
        
        .. seealso:: :func:`octant.data.OCTvolume.getVolume`
        """
        t=t.upper() #Uppercase
        theScans = list()
        for x in self.__scans:
            if (x.scantype==t):
                theScans.append(x)
        return theScans
        
    
    def getVolume(self,t):
        """
        Retrieves the (sub-)volume of scans of type t.
        
        :param t: Scan type 'A', 'B' or 'C'
        :type t: char
        :return: A volume with the set of scans of type t.
        :rtype: :class:`octant.data.OCTvolume`

        .. seealso:: :func:`octant.data.OCTvolume.getScans`
        """
        t=t.upper() #Uppercase
        theScans = octant.OCTvolume()
        for x in self.__scans:
            if (x.scantype==t):
                theScans.addScan(x)
        return theScans
        


    def getNScans(self,t = None):
        """Get the number of scans of a certain type.
        
        If type is not given, then the total number of scans is given.
        
        :param t: Scan type 'A', 'B' or 'C' or None
        :type t: char
        :return: The number of scans of a certain type
        :rtype: int
        """
        if t is None:
            res=len(self.__scans)
        else:
            res= self.getNScans(self.getVolume(t))
        return res