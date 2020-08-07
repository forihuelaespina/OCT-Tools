"""
-*- coding: utf-8 -*-

File: Document.py

Class Document

The document class.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 21-Aug-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 22-Aug-2018 | FOE    | - Defined method _getClassName                       |
|             |        | - Improved verbosity; now using class name           |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx documentation to |
|             |        |   the class                                          |
+-------------+--------+------------------------------------------------------+
|  2-Dec-2018 | FOE    | - Encapsulated properties and deprecated get/set     |
|             |        |   pairs for those properties.                        |
|             |        | - Minor debugging                                    |
+-------------+--------+------------------------------------------------------+
| 13-Dec-2018 | FOE    | - Updated deprecation package to "deprecation" due   |
|             |        |   compilation problems with package "deprecated".    |
+-------------+--------+------------------------------------------------------+
| 26-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded Document. The prefix IOT is        |
|             |        |   drop and it is now part of the package.            |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
|             |        | - Previously deprecated get/set function pairs       |
|             |        |   have now been fully removed.                       |
|             |        | - Private class attribute defaultName has been       |
|             |        |   eliminated. Instead the default name is directly   |
|             |        |   assigned to the property name in the constructor.  |
+-------------+--------+------------------------------------------------------+
| 25-Mar-2019 | FOE    | - Added properties docsettings.                      |
|             |        | - Started migration to OCTvolume based document.     |
|             |        |   As part of this, added new docsetting .selectedScan|
|             |        | - Added read only property currentScan               |
|             |        | - Added method pickScan.                             |
+-------------+--------+------------------------------------------------------+
| 30-Mar-2019 | FOE    | - Bug fixed. Imports __version__ instead of version. |
|             |        | - Property currentScan replaced by methods           |
|             |        |   getCurrentScan and setCurrentScan.                 |
+-------------+--------+------------------------------------------------------+
|  4-Apr-2019 | FOE    | - New methods getCurrentScanSegmentation and         |
|             |        |   setCurrentScanSegmentation.                        |
|             |        | - Bug fixed. Method `segmentation` now calls         |
|             |        |   `addScanSegmentations`. Also, parameter passed is  |
|             |        |   now correct.                                       |
+-------------+--------+------------------------------------------------------+
| 19-May-2019 | FOE    | - Bug fixed. Segmentation property setter was        |
|             |        |   incorrectly setting property study.                |
|             |        | - Bug fixed. Segmentation property setter was        |
|             |        |   asserting the number of scans against the study    |
|             |        |   reference using shape instead of len.              |
|             |        | - Bug fixed. Methods `getCurrentScan' and            |
|             |        |   `getCurrentScanSegmentation` were not checking for |
|             |        |   empty scan lists.                                  |
|             |        | - Properties `study` and `segmentation` are now      |
|             |        |   initialized to :class:`OCTvolume` and              |
|             |        |   :class:`OCTvolumeSegmentation` respectively.       |
+-------------+--------+------------------------------------------------------+
|  4-Apr-2019 | FOE    | - New method readFile in preparation for persistence.|
|             |        |   Still naive though.                                |
+-------------+--------+------------------------------------------------------+
| 16-Jan-2020 | FOE    | - Import line:                                       |
|             |        |     import octant.data as octant                     |
|             |        |   was causing error:                                 |
|             |        |     AttributeError: module 'octant' has no attribute |
|             |        |    'data'                                            |
|             |        |   It has now been updated to:                        |
|             |        |    from octant import data as octant                 |
+-------------+--------+------------------------------------------------------+


.. seealso:: None
.. note:: None
.. todo:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""



## Import
import warnings
#from deprecated import deprecated
import deprecation

import os

#from version import __version__
#from IOT_OCTscan import IOT_OCTscan
#from IOT_OCTscanSegmentation import IOT_OCTscanSegmentation
#from IOT_OCTvolume import IOT_OCTvolume
from octant import __version__
#import octant.data as octant
from octant import data as octant



## Class definition
class Document():
    #Sphinx documentation
    """The document class for OCTant.
    
    The document class for OCTant.
    
    This class represents a document in OCTant. A document holds information
    about a study plus some additional metadata.
    
    Currently, a study is only an OCT image (with several scans) with or without
    segmentation information.
    
    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """

    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        
        
        #Initialize private attributes unique to this instance
        self.study = octant.OCTvolume() #The current study.
                #Currently, an OCT volume
        self.segmentation = octant.OCTvolumeSegmentation() #The current study.
                #Currently, an OCT volumeSegmentation


        self.docsettings = octant.Settings()
        self.docsettings.selectedScan = None; #shared between study and segmentation
                
        #Document metadata
        self.folderName = '.' #Folder where the document is currently stored
        self.fileName = 'OCTantDocument0001' #The filename of the document
        self.name = 'OCTantDocument0001' #A logical name for the study
        
        return
        
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def docsettings(self): #docsettings getter
        """
        The application settings.

        :getter: Gets the document settings
        :setter: Sets the document settings 
        :type: class:`octant.data.Settings`
        """
        return self.__appsettings

    @docsettings.setter
    def docsettings(self,newSettings): #document setter
        if newSettings is None:
            newSettings = octant.Settings() #Initialize settings
        if (type(newSettings) is octant.Settings):
            self.__appsettings = newSettings
        else:
            warnMsg = self.getClassName() + ':docsettings: Unexpected settings type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        

    @property
    def study(self): #study getter
        """
        The OCT volume being processed and analysed.
        
        ..todo: Upgrade to volume. Watch out! This will affect many
            other classess using this method.

        :getter: Gets the OCT volume.
        :setter: Sets the OCT volume. 
        :type: :class:`octant.data.OCTvolume`
        """
        return self.__study

    @study.setter
    def study(self,vol): #study setter
        if (vol is None or type(vol) is octant.OCTvolume):
            self.__study = vol
            #...and reset scan
            self.segmentedScan = None
        elif type(vol) is octant.OCTscan:
            warnMsg = self.getClassName() + ':study: OCTvolume expected but OCTscan received. Embedding scan.'
            warnings.warn(warnMsg,SyntaxWarning)
            self.__study = octant.OCTvolume();
            self.__study.addScan(vol)
        else:
            warnMsg = self.getClassName() + ':study: Unexpected study type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        
        
    @property
    def segmentation(self): #segmentation getter
        """
        The segmentation over the OCT study being processed and analysed.

        :getter: Gets the OCT volume segmentation.
        :setter: Sets the OCT volume segmentation. 
        :type: :class:`octant.data.OCTvolumeSegmentation`
        """
        return self.__segmentation

    @segmentation.setter
    def segmentation(self,newSegmentation): #segmentation setter
        if ((newSegmentation is None) or (type(newSegmentation) is octant.OCTvolumeSegmentation)):
            self.__segmentation = newSegmentation
            if (newSegmentation is not None):
              if self.study is None:
                warnMsg = self.getClassName() + ':segmentation: No reference image.'
                warnings.warn(warnMsg,SyntaxWarning)
              if not (len(newSegmentation.scanSegmentations) == len(self.study.scans)):
                warnMsg = self.getClassName() + ':segmentation: Unexpected size.'
                warnings.warn(warnMsg,SyntaxWarning)
        elif (type(newSegmentation) is octant.OCTscanSegmentation):
            warnMsg = self.getClassName() + ':study: OCTvolumeSegmentation expected but OCTscanSegmentation received. Embedding scan.'
            warnings.warn(warnMsg,SyntaxWarning)
            self.__segmentation = octant.OCTvolumeSegmentation();
            self.__segmentation.addScanSegmentations(newSegmentation)
        else:
            warnMsg = self.getClassName() + ':segmentation: Unexpected segmented scan type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None



        

    @property
    def folderName(self): #folderName getter
        """
        Folder where the document is currently stored.
        
        ..note: Also retrieve the py:attr:`fileName` to build the full path.

        :getter: Gets the study folder name.
        :setter: Sets the study folder name. If new folder is None,
            the current directory '.' is chosen.
        :type: str
        """
        return self.__folderName

    @folderName.setter
    def folderName(self,d): #name setter
        if d is None:
            d = '.' #Set to current folder
        if (type(d) is str):
            self.__folderName = d
        else:
            warnMsg = self.getClassName() + ':name: Unexpected folderName type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        

    @property
    def fileName(self): #fileName getter
        """
        The filename of the document.
        
        
        ..note: Also retrieve the py:attr:`folderName` to build the full path.
        
        :getter: Gets the the filename of the document.
        :setter: Sets the The filename of the document. If new name is None,
            a default name is given.
        :type: str
        """
        return self.__folderName

    @fileName.setter
    def fileName(self,newFilename): #fileName setter
        if newFilename is None:
            newFilename = self.defaultName #Set to default name
        if (type(newFilename) is str):
            self.__fileName = newFilename
        else:
            warnMsg = self.getClassName() + ':name: Unexpected fileName type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        

    @property
    def name(self): #name getter
        """
        A logical name for the study.
        
        :getter: Gets the OCT study name.
        :setter: Sets the OCT study name.
        :type: str
        """
        return self.__name

    @name.setter
    def name(self,newName): #name setter
        if (newName is None or type(newName) is str):
            self.__name = newName
        else:
            warnMsg = self.getClassName() + ':name: Unexpected name type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        


    #Private methods
        
    
    #Public methods
    def getClassName(self):
        return type(self).__name__
    

    def getCurrentScan(self): 
        """Get the current working OCT scan
        
        Change the current selection using :func:`pickScan`
        
        :returns: The current working OCT scan.
        :rtype: :class:`octant.data.OCTscan` or None if the study contains no scans
        """
        if self.docsettings.selectedScan is None:
            self.docsettings.selectedScan = 0
        res = None
        if len(self.__study.scans) > 0:
            res = self.__study.scans[self.docsettings.selectedScan]
        return res

    def setCurrentScan(self,newScan): 
        """Sets the current working OCT scan
        
        Change the current selection using :func:`pickScan`
        
        :param newScan: An OCT scan to be assigned to the current working OCT scan.
        :type newScan: :class:`octant.data.OCTscan`
        """
        if self.docsettings.selectedScan is None:
            self.docsettings.selectedScan = 0
        if newScan is None:
            if self.__study.getNScans() == 0:
                #do nothing.
                pass
            else:
                warnMsg = self.getClassName() + ':setcurrentscan: Unexpected scan type NoneType.'
                warnings.warn(warnMsg,SyntaxWarning)
        if (type(newScan) is octant.OCTscan):
            self.__study.scans[self.docsettings.selectedScan] = newScan
        else:
            warnMsg = self.getClassName() + ':setcurrentscan: Unexpected scan type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        


    def pickScan(self,i):
        """Pick the i-th OCT scan (and its segmentation) for working.
        
        Sets the docsetting.selectedScan to i checking that it does exist.
        
        :param i: The selected scan index
        :type i: int
        :return: None
        """
        if type(i) is int and i<self.study.getNScans() and i>=0:
            self.docsettings.selectedScan = i
        else:
            warnMsg = self.getClassName() + ':pickScan: Selected scan does not exist.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
    
    
    
    def getCurrentScanSegmentation(self):
        """Get the current working OCT scanSegmentation
        
        Change the current selection using :func:`pickScan`
        
        :returns: The current working OCT scanSegmentation.
        :rtype: :class:`octant.data.OCTscanSegmentation`
        """
        if self.docsettings.selectedScan is None:
            self.docsettings.selectedScan = 0
        res = None
        if len(self.__segmentation.scanSegmentations) > 0:
            res = self.__segmentation.scanSegmentations[self.docsettings.selectedScan]
        return res


    def setCurrentScanSegmentation(self,newScan): 
        """Sets the current working OCT scanSegmentation
        
        Change the current selection using :func:`pickScan`
        
        :param newScan: An OCT scan to be assigned to the current working OCT scan.
        :type newScan: :class:`octant.data.OCTscanSegmentation`
        """
        if self.docsettings.selectedScan is None:
            self.docsettings.selectedScan = 0
        if newScan is None:
            if self.__segmentation.getNScans() == 0:
                #do nothing.
                pass
            else:
                warnMsg = self.getClassName() + ':setcurrentscansegmentation: Unexpected scan type NoneType.'
                warnings.warn(warnMsg,SyntaxWarning)
        if (type(newScan) is octant.OCTscanSegmentation):
            self.__segmentation.scanSegmentations[self.docsettings.selectedScan] = newScan
        else:
            warnMsg = self.getClassName() + ':setcurrentscansegmentation: Unexpected scan type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        

    def readFile(self,filename):
        """Reads an OCTant document file.

        This method is currently a sham, and it will be updated
        when serialization is incorporated to OCTant. Currently,
        it returns an empty document. Nevertheless, it already
        updates the document, clearing all fields to default values,
        and updates the filename and folder
        
        The file must exist or an error is generated.
        The file must be in OCTant file format.

        :param fileName: The file name
        :type fileName: str
        :return: This document
        :rtype: :class:`octant.data.Document`
        """
        self = Document()
        self.folderName, self.fileName = os.path.split(filename)
        return self