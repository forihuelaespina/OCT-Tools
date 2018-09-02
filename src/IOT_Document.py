# -*- coding: utf-8 -*-

# File: IOT_Document.py
#
# The document class for OCT-Tools.
# IOT stands for INAOE OCT Tools
# 
# This class represents a document in OCT-Tools. A document holds information
#about a study plus some additional metadata.
#
# Currently, a study is only an OCT image (with several scans) with or without
#segmentation information.
#
#
#
# @dateCreated: 21-Aug-2018
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 22-Aug-2018
#
# See also:
# 


## Log
#
# 21-Aug-2018: FOE: 
#  * Class created. 
#
# 22-Aug-2018: FOE: 
#   * Defined method _getClassName
#   * Improved verbosity; now using class name
#


## Import




## Class definition
class IOT_Document():

    #Private class attributes shared by all instances
    defaultName = 'IOTDocument'

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        
        
        #Initialize private attributes unique to this instance
        self._study = None #The current study.
                #Currently, an OCT scan
        self._segmentedScan = None
                
        #Document metadata
        self._folderName = '.' #Folder where the document is currently stored
        self._fileName = self.defaultName #The filename of the document
        self._name = self.defaultName #A logical name for the study
        
        
        
        
        
    #Private methods
        
    
    #Public methods
    def getClassName(self):
        return type(self).__name__
    
    def getFolderName(self):
        return self._folderName

    def setFolderName(self,d):
        if d is None:
            d = '.' #Set to current folder
        self._folderName = d;
        return

    def getFileName(self):
        return self._fileName

    def setFileName(self,newName):
        if newName is None:
            newName = self.defaultName #Set to a default filename
        self._fileName = newName;
        return

    def getName(self):
        return self._folder

    def setName(self,newName):
        if newName is None:
            newName = self.defaultName #Set to a default name
        self._name = newName;
        return

    def getStudy(self):
        return self._study

    def setStudy(self,newStudy):
        self._study = newStudy;
        #...and reset scan
        self._segmentedScan = None
        return

    def getScanSegmentation(self):
        return self._segmentedScan

    def setScanSegmentation(self,newSegmentation):
        #print(self.getClassName(),':setScanSegmentation: Setting scan segmentation; ', self._study)
        if self._study is None:
            print(self.getClassName(),':setScanSegmentation: Warning: No reference image.')
            self._segmentedScan = newSegmentation          
        if newSegmentation.shape == self._study.shape[0:2]:
            #print(self.getClassName(),':setScanSegmentation: Setting new segmentation for current scan.')
            self._segmentedScan = newSegmentation
        else:
            print(self.getClassName(),':setScanSegmentation: Error: Unexpected segmented scan size.')
            print(self._study.shape[0:2])
            print(newSegmentation.shape)
            self._segmentedScan = None
        return










    