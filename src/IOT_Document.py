"""
-*- coding: utf-8 -*-

File: IOT_Document.py

Class IOT_Document

The document class for OCT-Tools.

IOT stands for INAOE OCT Tools

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

from version import __version__
from IOT_OCTscan import IOT_OCTscan
from IOT_OCTscanSegmentation import IOT_OCTscanSegmentation
#from IOT_OCTvolume import IOT_OCTvolume



## Class definition
class IOT_Document():
    #Sphinx documentation
    """The document class for OCT-Tools.
    
    The document class for OCT-Tools.
    
    This class represents a document in OCT-Tools. A document holds information
    about a study plus some additional metadata.
    
    Currently, a study is only an OCT image (with several scans) with or without
    segmentation information.
    
    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """

    #Private class attributes shared by all instances
    defaultName = 'IOTDocument'

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        
        
        #Initialize private attributes unique to this instance
        self.study = None #The current study.
                #Currently, an OCT scan
        self.segmentation = None
                
        #Document metadata
        self.folderName = '.' #Folder where the document is currently stored
        self.fileName = self.defaultName #The filename of the document
        self.name = self.defaultName #A logical name for the study
        
        return
        
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def study(self): #study getter
        """
        The OCT scan being processed and analysed.
        
        ..todo: Upgrade to volume. Watch out! This will affect many
            other classess using this method.

        :getter: Gets the OCT scan.
        :setter: Sets the OCT scan. 
        :type: :class:`src.IOT_OCTscan`
        """
        return self.__study

    @study.setter
    def study(self,vol): #study setter
        if (vol is None or type(vol) is IOT_OCTscan):
            self.__study = vol
            #...and reset scan
            self.segmentedScan = None
        else:
            warnMsg = self.getClassName() + ':study: Unexpected study type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
        
        
    @property
    def segmentation(self): #segmentation getter
        """
        The segmentation over the OCT study being processed and analysed.

        ..todo: Upgrade to volume. Watch out! This will affect many
            other classess using this method.

        :getter: Gets the OCT scan segmentation.
        :setter: Sets the OCT scan segmentation. 
        :type: :class:`IOT_OCTscanSegmentation`
        """
        return self.__segmentation

    @segmentation.setter
    def segmentation(self,newSegmentation): #segmentation setter
        if ((newSegmentation is None) or (type(newSegmentation) is IOT_OCTscanSegmentation)):
            self.__segmentation = newSegmentation
            if (newSegmentation is not None):
              if self.study is None:
                warnMsg = self.getClassName() + ':segmentation: No reference image.'
                warnings.warn(warnMsg,SyntaxWarning)
              if(newSegmentation.shape == self.study.shape[0:1]):
                warnMsg = self.getClassName() + ':segmentation: Unexpected size.'
                warnings.warn(warnMsg,SyntaxWarning)
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
    
   # @deprecated(version='0.2', reason="Deprecated. Access property .folderName instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .folderName instead.")
    def getFolderName(self):
        return self.folderName

    #@deprecated(version='0.2', reason="Deprecated. Access property .folderName instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .folderName instead.")
    def setFolderName(self,d):
        self.folderName = d;
        return

    #@deprecated(version='0.2', reason="Deprecated. Access property .fileName instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .fileName instead.")
    def getFileName(self):
        return self.fileName

    #@deprecated(version='0.2', reason="Deprecated. Access property .fileName instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .fileName instead.")
    def setFileName(self,newName):
        self.fileName = newName;
        return

    #@deprecated(version='0.2', reason="Deprecated. Access property .name instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .name instead.")
    def getName(self):
        return self.name

    #@deprecated(version='0.2', reason="Deprecated. Access property .name instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .name instead.")
    def setName(self,newName):
        self._name = newName;
        return

    #@deprecated(version='0.2', reason="Deprecated. Access property .study instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .study instead.")
    def getStudy(self):
        return self.study

    #@deprecated(version='0.2', reason="Deprecated. Access property .study instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .study instead.")
    def setStudy(self,newStudy):
        self.study = newStudy;
        return

    #@deprecated(version='0.2', reason="Deprecated. Access property .segmentation instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .segmentation instead.")
    def getScanSegmentation(self):
        return self.segmentation

    #@deprecated(version='0.2', reason="Deprecated. Access property .segmentation instead.")
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Access property .segmentation instead.")
    def setScanSegmentation(self,newSegmentation):
        self.segmentation = newSegmentation
        return










    