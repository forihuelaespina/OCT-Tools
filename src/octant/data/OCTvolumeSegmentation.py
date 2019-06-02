# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 17:08:29 2019

@author: fo067
"""

"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: OCTvolumeSegmentation.py

Class OCTvolumeSegmentation

A set of :class:`octant.OCTscanSegmentation` . All scans are of :class:`OCTscanSegmentation`.

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 25-Mar-2019 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 19-May-2019 | FOE    | - Bug fixed. Method addScanSegmentation flag for     |
|             |        |   testing all inputs to be of type OCTscans was not  |
|             |        |   being correctly initialized.                       |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import warnings

from octant import version
import octant.data as octant

## Class definition
class OCTvolumeSegmentation(object):
    #Sphinx documentation
    """A set of :class:`octant.data.OCTscanSegmentation`

    A set of :class:`octant.data.OCTscanSegmentation`
    
    .. seealso:: :class:`octant.data.OCTscanSegmentation`
    .. note:: None
    .. todo:: None

    """

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = OCTvolumeSegmentation() - Creates an empty segmentation volume with no scans.
        
        """
        self.scanSegmentations = list()
        return
        



    #Properties getters/setters
    @property
    def scanSegmentations(self): #scans getter
        """
        The set of OCT scans segmentations.

        :getter: Gets the set of scans segmentations
        :setter: Sets the set of scans segmentations
        :type: list. All scans are of :class:`octant.data.OCTscanSegmentation`
        
        .. seealso:: :func:`octant.data.OCTvolumeSegmentation.addScan` , :func:`octant.data.OCTvolumeSegmentation.removeScan` , :func:`octant.data.OCTvolumeSegmentation.clear`
        
        """
        return self.__scanSegmentations


    @scanSegmentations.setter
    def scanSegmentations(self,*args): #scanSegmentations setter
        tmpScanSet=args[0]
        if type(tmpScanSet) is not list:
            warnMsg = self.getClassName() + ':scanSegmentations: Unexpected type. ' \
                            'Please provide a list of octant.data.OCTscanSegmentation.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__scanSegmentations = list()
            for x in tmpScanSet:
                if type(x) is not octant.OCTscanSegmentation:
                    warnMsg = self.getClassName() + ':scanSegmentations: Unexpected scan type ' \
                                'for object ' + x + '. Skipping object.'
                    warnings.warn(warnMsg,SyntaxWarning)
                else:
                    self.__scanSegmentations.append(x)
        return None


    #Public methods
    def clear(self):
        """
        Clears the OCT segmentation volume; Removes all scan segmentations.
        
        :return: None
        """
        self.__scanSegmentations = list()
        return None
    
    def addScanSegmentations(self,theScanSegmentations):
        """
        Add one or multiple OCT scan segmentation to the volume.
        
        :param theScanSegmentations: The list of OCT scan segmentations
        :type theScanSegmentations: list of :class:`octant.data.OCTscanSegmentation` or
            single :class:`octant.data.OCTscanSegmentation`
        :return: None
        """
        flagAllOCTscans=False
        if type(theScanSegmentations) is octant.OCTscanSegmentation:
            flagAllOCTscans=True
            self.__scanSegmentations.append(theScanSegmentations)
        elif type(theScanSegmentations) is list:
            flagAllOCTscans=True
            for elem in theScans:
                if type(elem) is not octant.OCTscanSegmentation:
                    warnMsg = self.getClassName() + ':addScans: Unexpected scan type. ' \
                                'Nothing will be added.'
                    flagAllOCTscans=False
                    break
            if flagAllOCTscans:    
                self.__scanSegmentations.extend(theScanSegmentations)
        return flagAllOCTscans
        
    
    
    def getScanSegmentations(self,t):
        """
        Retrieves all scans in the volume of type t.
        
        :param t: Scan type 'A', 'B' or 'C' or scan indexing
        :type t: str, list or int
        :return: The set of scans in the volume of the chosen
        :rtype: list
        
        .. seealso:: :func:`octant.data.OCTvolumeSegmentation.getVolume`
        """
        theScans = list()
        if type(t) is str:
            t=t.upper() #Uppercase
            for x in self.__scanSegmentations:
                if (x.scantype==t):
                    theScans.append(x)
        elif type(t) is list:
            for elem in t:
                theScans.append(self.__scanSegmentations[elem])
        elif type(t) is int:
            theScans.append(self.__scanSegmentations[elem])
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
        theScans = octant.OCTvolumeSegmentation()
        for x in self.__scanSegmentations:
            if (x.scantype==t):
                theScans.addScanSegmentation(x)
        return theScans
        
    
    def getNScans(self):
        """Get the number of scans segmentations.
        
        :return: The number of scans segmentations
        :rtype: int
        """
        return len(self.__scanSegmentations)
