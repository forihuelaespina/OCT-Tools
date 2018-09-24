"""
-*- coding: utf-8 -*-

File: IOT_OperationEditSegmentation.py

Class IOT_OperationEditSegmentation

Operation EditSegmentation



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 5-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
+-------------+--------+------------------------------------------------------+
| 22-Aug-2018 | FOE    | - Class name rebranded to capital "O" in operation   |
|             |        | - Improved verbosity; now using class name           |
+-------------+--------+------------------------------------------------------+
| 26-Aug-2018 | FOE    | - Dummy segmentation now takes into account          |
|             |        |   IOT_RetinalLayers                                  |
|             |        | - Added constant for background                      |
|             |        | - Incorporated the initial functionality; ROISelect, |
|             |        |   ROIDeselect, ROIDelete, ROIRelabel                 |
|             |        | - Debugged getROIPixels; it now correctly parcellates|
|             |        |   background connected components                    |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx documentation to |
|             |        |   the class.                                         |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None

    

@dateCreated: Feb-2018
@dateModified: 23-Sep-2018

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import

import numpy as np
#from skimage import feature, color
#import cv2 #That's OpenCV
#import segmentationUtils

from scipy import ndimage
from skimage import io, color, morphology



# #So that the FigureCanvas is also a Qt object where Events can be listenes
# #Make it valid for Qt4 or Qt5
# from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
# if is_pyqt5():
#     from matplotlib.backends.backend_qt5agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# else:
#     from matplotlib.backends.backend_qt4agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.figure import Figure
# 
# #from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QKeyEvent, QMouseEvent


from IOT_Operation import IOT_Operation
from IOT_RetinalLayers import IOT_RetinalLayers


## Class definition
class IOT_OperationEditSegmentation(IOT_Operation):
    #Sphinx documentation
    """Operation EditSegmentation
    
    This class permits manual manipulation of a segmentation of retinal layers
    from an OCT image. The class provides its functionality by manipulating
    local regions of interest (ROI) and or Classes of interest (COI) in the
    segmentation.
    A ROI is just a connected set of pixels with the same label. A COI is the
    set of all ROIs sharing the same label.
    
    The class provides a set of basic operations for selecting and
    then maniplating some ROI or COI in a segmentation; including:
    
    * Delete
    * Change label
    
    Whether working with ROI or COI always select the active COI or ROI
    before applying an operation.
    
    
    .. seealso:: 
    .. note:: 
    .. todo:: 
        
    """

    #Private class attributes shared by all instances
    BACKGROUND = 0
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.
        #Initialize private attributes unique to this instance
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #The segmented image
        #self._fig = None #The figure canvas
        #self._flagListening = False #Flag for listening to mouse events
        self._activeROI = None #Currently active ROI. The ROI is identified by
                                #a position tuple [x,y[,z]] indicating any pixel
                                #ROI. The ROI itself is all the connected
                                #of the component to this pixel. The class of
                                #the ROI corresponds the label at [x,y[,z]]
        self._activeCOI = IOT_OperationEditSegmentation.BACKGROUND #Currently active COI. The COI is identified by
                                #its class ID.
    
    
    #Private methods



    def _generateDummySegmentation(self,height,width):
    #Define a dummy segmentation
        #print(self.getClassName(),": _generateDummySegmentation: Generating dummy segmentation.")
        r= IOT_RetinalLayers()
        nLayers = r.getNumLayers()
        tmp = r.getAllLayersIndexes()
        
        
        #Define a default output -simple nLayers lines (one per layer)
        imageSegmented = IOT_OperationEditSegmentation.BACKGROUND * np.ones((height,width), dtype = np.uint8 )
        stepHeight = round(0.9*(height/(nLayers+1)))
        offset = round((0.1*height/(nLayers+1))/2)
        for ii in range(1,nLayers):
            kk = offset + ii*stepHeight
            imageSegmented[kk-2:kk+2,:] = tmp[ii-1] #5 pixels thick
                #Watch out! Lines thinner than 3-5 pixels thick may not
                #be visible when rendered on the screen (depending on
                #the resolution).
            #print(kk, ii)
        return imageSegmented


    

    #Public methods 
    
    # See: https://pypi.org/project/pynput/
    def initEditSegmentation(self,image,imageSegmented = None):
        #Initialize segmentation for editing
        
        #self._fig = figCanvas
        
        #print("OCT-Tools: IOT_operationSegmentation: Starting manual editing of retinal layer segmentation")
        self._imgin = image
        
        if imageSegmented is None:
            #print("OCT-Tools: IOT_operationSegmentation: Segmentation not found.")
            tmpImgSize = image.shape
            imageSegmented = self._generateDummySegmentation(tmpImgSize[0],tmpImgSize[1])

        self._imgout = imageSegmented
        return self._imgout    


    #Manipulation of ROI
    def getROIPixels(self):
    #Retrieves the indexes of all the pixels in the connected component of
    #the current ROI
        
        #skimage.morphology.label does not split BG regions. So start
        #checking whether the active region is in the background
        
        imSegmented = self._imgout
        isBG = self._imgout[self._activeROI] == IOT_OperationEditSegmentation.BACKGROUND
        if isBG:
            #Trick skimage.morphology.label into believing the background is NOT the backgrond
            tmpDummy = imSegmented==IOT_OperationEditSegmentation.BACKGROUND
            imSegmented = tmpDummy.astype(np.int) #Now change from boolean to integers

        
        #Get connected components (background is not counted)
        tmpConnectedComponents,numComponents = morphology.label(imSegmented,
                    neighbors=4,
                    background=IOT_OperationEditSegmentation.BACKGROUND,
                    return_num=True)
        #Find component index associated to active ROI
        cIdx=tmpConnectedComponents[self._activeROI]
        #Retrieve the indexes of pixels in the connected component to the active ROI
        idx = np.nonzero(tmpConnectedComponents == cIdx)
        return idx

    def getCOIPixels(self,coi=None):
    #Retrieves the indexes of all the pixels of the current COI
        idx=None
        if coi is None:
            #Check active COI
            idx = nd.nonzero(self._imgout == self_activeCOI)
        elif coi==IOT_OperationEditSegmentation.BACKGROUND:
            idx = not nd.nonzero(self._imgout)
        else:
            idx = nd.nonzero(self._imgout == coi)
        return idx

    
    def getROILabel(self):
    #Retrieves the class or label of the current ROI
        return self._imgout[self._activeROI]
    
    def ROISelect(self,pos):
    #Select the closest ROI within some radius (in pixel). Return True if a ROI has been found or False otherwise
    #
    # pos: A pixel/voxel of the ROI; (x,y) or (x,y,z)
        print(self.getClassName(),":ROISelect: Selecting ROI connected to pixel ",pos)
        self._activeROI = pos
        #Check whether there is some region in the area
        return True

    def ROIChangeLabel(self, newClassID, pos=None):
    #Updates the label of the current active ROI or the selected COI (if
    #argument pos is provided).
    #
    #The newClassID becomes the new updated ROI.
    #
    #Note that this actually removes the current active ROI from the
    #segmentation, since no pixel with the current label will remain in
    #the segmentation.
    #If you only want to affect some ROI, then use ROIChangeLabel instead
    
        if pos is not None:
            self.ROISelect(pos)
        
        if self._activeROI is None: #This may occur if trying to call the
                                   #operation right after creating this
                                   #object instance (when activeROI is None),
                                   #but still calling to execute operation
                                   #without parameters
            print(self.getClassName(),":ROIChangeLabel: No ROI selected. Passing...")
        else:
            print(self.getClassName(),":ROIChangeLabel: activeROI: ", self._activeROI," with class ", self.getROILabel(),"; newClassID:",newClassID)
            idx = self.getROIPixels()
            print(idx)
            self._imgout[idx] = newClassID
            self._activeROI = newClassID
        return self._imgout


        
    def ROIDelete(self, roiID = None):
    #Deletes the current active COI. Sets it to BACKGROUND
        if roiID is not None:
            self.ROISelect(roiID)
            
        if self._activeROI is None: #This may occur if trying to call the
                                   #operation right after creating this
                                   #object instance (when activeROI is None),
                                   #but still calling to execute operation
                                   #without parameters
            print(self.getClassName(),":ROIDelete: No ROI selected. Passing...")
        else:
            print(self.getClassName(),":ROIDelete: Deleting activeROI: ", self._activeROI," with class ", self.getROILabel())
            idx = self.getROIPixels()
            #print(idx)
            self._imgout[idx] = IOT_OperationEditSegmentation.BACKGROUND
            self._activeROI = None
        return self._imgout
        



    #Manipulation of COI
    def COISelect(self,classID):
    #Select a COI by its label. If the classID is not found in the 
    #segmentation, then the BACKGROUND is selected
        print(self.getClassName(),":COISelect: Selecting layer ", classID)
        
        self._activeCOI = IOT_OperationEditSegmentation.BACKGROUND
        idx = np.nonzero(self._imgout == classID)
        if len(idx) != 0:
            self._activeCOI = classID
        
        return len(idx) != 0
        
    def COIDelete(self, classID = None):
    #Deletes the COI identified by classID. Sets the COI to BACKGROUND
    #If classID is None, then it works over the current active COI. 
    
        if classID is None:
            #Operate over current active COI
            idx = np.nonzero(self._imgout == self._activeCOI)
                #WATCH OUT!
                #Distinctly from MATLAB, here I do not get a "list" of locations
                #indexing the array form 1 to numel(self._imgout). Instead,
                #a "coupled" pair of lists for the xIdx and yIdx are obtained.
                #
                #So to check whether it is "empty" I cannot do:
                #   len(idx)
                #...as this is equal to 2.
                #I must question "along a single dimension; e.g. len(idx[0])
                
            if len(idx[0]) == 0:
                print(self.getClassName(),":COIDelete: Layer ", self._activeCOI," not found. Skipping.")
            else:
                print(self.getClassName(),":COIDelete: Layer ", self._activeCOI," found. Deleting layer ", self._activeCOI)
                self._imgout[idx] = IOT_OperationEditSegmentation.BACKGROUND
                self._activeCOI = IOT_OperationEditSegmentation.BACKGROUND
        else:
            self.COISelect(classID)
            self.COIDelete()
        return self._imgout
        
    def COIChangeLabel(self, newClassID, coi=None):
    #Updates the label of the current active COI or the selected COI (if
    #argument coi is provided).
    #
    #The newClassID becomes the new updated COI.
    #
    #Note that this actually removes the current active COI from the
    #segmentation, since no pixel with the current label will remain in
    #the segmentation.
    #If you only want to affect some ROI, then use ROIChangeLabel instead
    
        if coi is not None:
            self.COISelect(coi)
            
        print(self.getClassName(),":COIChangeLabel: activeCOI:", self._activeCOI,"; newClassID:",newClassID)
        idx = np.nonzero(self._imgout == self._activeCOI)
        self._imgout[idx] = newClassID
        self._activeCOI = newClassID
        return self._imgout
        
        
        
