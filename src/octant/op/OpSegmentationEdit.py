"""
-*- coding: utf-8 -*-

File: OpSegmentationEdit.py

Class OpSegmentationEdit

Operation SegmentationEdit



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
| 15-Nov-2018 | FOE    | - Dummy segmentation now results in a full           |
|             |        |   segmentation and returns an IOT_OCTscanSegmentation|
+-------------+--------+------------------------------------------------------+
|  1-Dec-2018 | FOE    | - Adapted to IOT_Operation becoming abstract and new |
|             |        |   capabilities. Added method .execute, integration of|
|             |        |   operands, given operation name, deprecated method  |
|             |        |   initEditSegmentation.                              |
|             |        | - Updated attributes activeROI and activeCOI to      |
|             |        |   properties.                                        |
|             |        | - ROISelect method now searches for a labelled ROI   |
|             |        |   within a neighobourhood.                           |
+-------------+--------+------------------------------------------------------+
|  9-Jan-2019 | FOE    | - Bug detected. Variable imgin in method execute had |
|             |        |   not been set.                                      |
+-------------+--------+------------------------------------------------------+
| 13-Dec-2018 | FOE    | - Updated deprecation package to "deprecation" due   |
|             |        |   compilation problems with package "deprecated".    |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded Operation. The prefix              |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        |   Also, the subprefix Operation is reduced to Op     |
|             |        |   only, the class name extended with the main        |
|             |        |   operand type.                                      |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
+-------------+--------+------------------------------------------------------+
|  3-Feb-2019 | FOE    | - Debugging of errors left during transition to new  |
|             |        |   package OCTant structure; wrong imports and        |
|             |        |   unupdated classes names.                           |
+-------------+--------+------------------------------------------------------+
|  4-Apr-2019 | FOE    | - Bug fixing. References to                          |
|             |        |   :class:`octant.data.OCTscan` updated.              |
|             |        | - Bug fixing. Call update from                       |
|             |        |   OpEditSegmentation._BACKGROUND to                  |
|             |        |   OpSegmentationEdit._BACKGROUND in method           |
|             |        |   _generateDummySegmentation.                        |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None

    
.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import

import warnings
#from deprecated import deprecated
import deprecation

import numpy as np
#from skimage import feature, color
#import cv2 #That's OpenCV
#import segmentationUtils

from scipy import ndimage
from skimage import io, color, morphology

from octant import __version__
from octant.data import OCTscan, OCTscanSegmentation, RetinalLayers
from .Operation import Operation


## Class definition
class OpSegmentationEdit(Operation):
    #Sphinx documentation
    """Operation Edit Segmentation
    
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
    
    
    .. seealso:: None
    .. note:: Operand is an class:`octant.data.OCTscanSegmentation`, but a reference
        image can be hold as the class:`octant.data.OCTscanSegmentation` attribute
        :py:attr:`scan`
    .. todo:: None
        
    """

    #Private class attributes shared by all instances
    _BACKGROUND = 0
    
    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = OpEditSegmentation() - Creates an empty SegmentationEdit operation
        

        :param img: The scan image
        :type img: numpy.ndarray
        :param type: The scan type ('A' -default-, 'B' or 'C')
        :type type: char
        
        """
        #Call superclass constructor
        super().__init__()

        #Set the operation name
        self.name = "SegmentationEdit"

        #Initialize private attributes unique to this instance

        self.activeROI = (0,0) #Currently active ROI.
        self.activeCOI = OpSegmentationEdit._BACKGROUND #Currently active COI. 
    
        return
        
        
        
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def activeROI(self): #activeROI getter
        """
        Currently active ROI.
        
        The ROI is identified by a position
        tuple (x,y[,z]) indicating any pixel ROI. The ROI itself is
        all the connected of the component to this pixel. The class
        of the ROI corresponds the label at (x,y[,z])
        
        :getter: Gets the active ROI
        :setter: Sets the active ROI to (x,y[,z]).
        :type: tuple
        """
        return self.__activeROI

    @activeROI.setter
    def activeROI(self,newROI): #activeROI setter
        if type(newROI) is tuple and len(newROI) >= 2 and len(newROI) <= 3:
            #It might be more correct to also check for the internal type to be
            #scalars.
            self.__activeROI = newROI
        elif type(newROI) is list and len(newROI) >= 2 and len(newROI) <= 3: #Unexpected case. Return warning
            warnMsg = self.getClassName() + ':activeROI: List [x,y[,z]] will be recasted to tuple (x,y[,z]).'
            warnings.warn(warnMsg,SyntaxWarning)
            self.__activeROI = tuple(newROI)            
        else: #Unexpected case. Return warning
            warnMsg = self.getClassName() + ':activeROI: Value must be a tuple (x,y[,z]).'
            warnings.warn(warnMsg,SyntaxWarning)
        return None

    @property
    def activeCOI(self): #activeCOI getter
        """
        Currently active COI.
        
        The COI is identified by its class ID.
        
        :getter: Gets the active COI
        :setter: Sets the active COI
        :type: tuple
        """
        return self.__activeCOI

    @activeCOI.setter
    def activeCOI(self,newCOI): #activeCOI setter
        self.__activeCOI = newCOI
        return None


    #Private methods



    def _generateDummySegmentation(self,height,width):
        """Define a dummy segmentation.
        
        Generates a dummy segmentation.
        
        :returns: An OCT scan segmentation
        :rtype: :class:`octant.data.OCTscanSegmentation`.
        """
        #Define a dummy segmentation
        #print(self.getClassName(),": _generateDummySegmentation: Generating dummy segmentation.")
        r= RetinalLayers()
        nLayers = r.getNumLayers()
        tmp = r.getAllLayersIndexes()
        
        #Generate a dummy refImage of the appropiate size
        refImage = OCTscan(np.zeros(shape = (height,width), dtype = np.uint8 ));
        
        
        #Define a default output -simple nLayers lines (one per layer)
        imageSegmented = OpSegmentationEdit._BACKGROUND * np.ones((height,width), dtype = np.uint8 )
        stepHeight = round(0.7*(height/(nLayers+1)))
        offset = round((0.3*height/(nLayers+1))/2)
        for ii in range(1,nLayers+1):
            #print ('Layer' + str(ii))
            kk = offset + ii*stepHeight
            #imageSegmented[kk-2:kk+2,:] = tmp[ii-1] #5 pixels thick
                #Watch out! Lines thinner than 3-5 pixels thick may not
                #be visible when rendered on the screen (depending on
                #the resolution).
            imageSegmented[kk:kk+stepHeight,:] = tmp[ii-1] #Segment the full
                #band until the next layer.
            #print(kk, ii)
        
        #Encapsulate
        dummySegmentation = OCTscanSegmentation(refImage)
        dummySegmentation.data = imageSegmented 
        
        #print(dummySegmentation.data)
        
        return dummySegmentation


    

    #Public methods 
    def execute(self,*args,**kwargs):
        """Executes the operation on the :py:attr:`operands`.
        
        Executes the operation on the :py:attr:`operands` and stores the 
        outcome in :py:attr:`result`. Preload operands using
        :func:`IOT:Operation.addOperand()`.
        
        :param editType: A string indicating the type of edition
        :type editType: String
        :returns: Result of executing the operation.
        :rtype: :class:`IOT_OCTscanSegmentation`
        """
        #print(self._getClasName(),": editSegmentation: Starting edit segmentation")
        
        #Define a default result
        self.result = self._generateDummySegmentation(480,640);
        
        #Ensure the operand has been set.
        if (self.arity() <1):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return self.result

        imgin = self.operands[0]
        self.result = imgin; #Start by copying operand into result
        
        # if isinstance(imgin,(IOT_OCTscanSegmentation,)):
        #     imgin=imgin.data

        #Indirect call to the operation
        #See: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string    
        theOperationName = args[0]
        params = [args[1:],kwargs]
        theOp = getattr(self, theOperationName) 
        if params is None:
            imSegmented = theOp()
        else:
            imSegmented = theOp(*params)

            
        #if isinstance(imgin,(OCTscan,)):
        if type(imgin) is OCTscan:
            self.result=OCTscanSegmentation(imgin)
        else:
            self.result=OCTscanSegmentation(OCTscan(imgin))
        self.result.data = imSegmented
        
        return self.result   
    
    # See: https://pypi.org/project/pynput/
    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
                        current_version=__version__,
                        details="Use method addOperand() and add reference image as scan property of class:`IOT_OCTscanSegmentation`.")
    def initEditSegmentation(self,refImage,imageSegmented = None):
        """Initialize segmentation for editing from reference :class:`IOT_OCTscan`.
        
        :param refImage: A reference OCT scan
        :type refImage: :class:`octant.data.OCTscan`
        :param imageSegmented: The operand. A segmentation over parameter refImage.
        :type imageSegmented: :class:`octant.data.OCTscanSegmentation`
        :returns: An initialized edit segmentation operation.
        :rtype: :class:`octant.data.OCTscanSegmentation`
        """
        
        if type(refImage) is not OCTscan:
            #Encapsulate
            refImage=OCTscan(refImage)
            
        #Operand is the image to be segmented

        #print("OCT-Tools: octant.OpEditSegmentation: Starting manual editing of retinal layer segmentation")
        tmp=OCTscanSegmentation(refImage)
        
        #Second parameter is a seed segmentation. If none provided, generate a dummy one on the fly.
        if imageSegmented is None:
            #print("OCT-Tools: IOT_operationSegmentation: Segmentation not found.")
            tmpImgSize = refImage.shape
            imageSegmented = self._generateDummySegmentation(tmpImgSize[0],tmpImgSize[1])
            #Update the segmentation but keep the reference image in tmp. In
            #other words, ignore the dummy "reference" image.
            tmp.data = imageSegmented.data
        elif type(imageSegmented) is OCTscanSegmentation:
            tmp = imageSegmented
        else:
            warnMsg = self.getClassName() + ':initEditSegmentation: Unexpected type for imageSegmented.'
            warnings.warn(warnMsg,SyntaxWarning)
            
        self.addOperand(tmp)
        return tmp    


    #Manipulation of ROI
    def getROIPixels(self):
        """Retrieves the indexes of all the pixels in the connected component of the current ROI.

        :returns: Indexes of connected pixels in the ROI
        :rtype: np.array
        """
        tmpOperand = self.operands[0] #Access operand
        
        #skimage.morphology.label does not split BG regions. So start
        #checking whether the active region is in the background
        
        imSegmented = tmpOperand
        isBG = tmpOperand.data[self.activeROI] == OpSegmentationEdit._BACKGROUND
        if isBG:
            #Trick skimage.morphology.label into believing the background is NOT the backgrond
            tmpDummy = tmpOperand.data==OpSegmentationEdit._BACKGROUND
            imSegmented = tmpDummy.astype(np.int) #Now change from boolean to integers

        
        #Get connected components (background is not counted)
        tmpConnectedComponents,numComponents = morphology.label(imSegmented,
                    neighbors=4,
                    background=OpSegmentationEdit._BACKGROUND,
                    return_num=True)
        #Find component index associated to active ROI
        cIdx=tmpConnectedComponents[self.activeROI]
        #Retrieve the indexes of pixels in the connected component to the active ROI
        idx = np.nonzero(tmpConnectedComponents == cIdx)
        return idx

    def getCOIPixels(self,coi=None):
        """Retrieves the indexes of all the pixels of the current COI

        :returns: Indexes of pixels in the COI
        :rtype: np.array
        """
        tmpOperand = self.operands[0]; #Access operand
        
        idx=None
        if coi is None:
            #Check active COI
            idx = nd.nonzero(tmpOperand.data == self.activeCOI)
        elif coi==OpEditSegmentation.BACKGROUND:
            idx = not nd.nonzero(tmpOperand.data)
        else:
            idx = nd.nonzero(tmpOperand.data == coi)
        return idx

    
    def getROILabel(self):
        """Retrieves the class or label of the current ROI.
        
        :returns: The class or label of the current ROI
        :rtype: int
        """
        tmpOperand = self.operands[0]; #Access operand
        return tmpOperand.data[self.activeROI]
    
    def ROISelect(self,pos,radius = 10):
        """Select the closest labelled ROI within some radius (in pixels) of pos.
        
        Select the closest labelled ROI within some radius (in pixels) of pos
        or the BACKGROUND if no labelled region is found.
        
        If pos correspond to a labelled region, then it becomes the 
        py:attr:`activeROI`, and True is returned.
        
        If pos is in the BACKGROUND, and it is at the same distance
        of more than one labelled regions, then the selected ROI is pick
        at random (actually it selects the first found from the top left)
        and True is returned.
        
        If pos is in the BACKGROUND, and no labelled region is found in the
        neighbourhood, then pos becomes the new py:attr:`activeROI` and
        False is returned.
        
        ..note: To select a specific ROI regardless of its class ID (e.g.
            enforce selection of a BACKGROUND pixel), simply assign some
            value to property py:attr:`activeROI`
        
        :param pos: A pixel/voxel of the ROI; (x,y) or (x,y,z)
        :type pos: tuple or list
        :param radius: Radius in pixels. Default value is 10 pixels
        :type radius: uint
        :returns: True if a labelled ROI has been found or False otherwise
        :rtype: bool
        """
        tmpOperand = self.operands[0]; #Access operand
                        
        #print(self.getClassName(),":ROISelect: Selecting ROI connected to pixel ",pos)
        flagFound = False
        #Check whether there is some region in the area
        if tmpOperand.data[pos] == OpSegmentationEdit._BACKGROUND:
            #pos is in BACKGROUND. Look for nearby labelled regions
            r=0
            while r <= radius and not flagFound:
                r += 1
                #Extract squared subimage around pos (without exceeding borders).
                xmin = max(tmpOperand.shape[0],pos[0]-r)
                xmax = min(tmpOperand.shape[0],pos[0]+r+1)
                ymin = max(tmpOperand.shape[1],pos[1]-r)
                ymax = min(tmpOperand.shape[1],pos[1]+r+1)
                ixgrid = np.ix_(np.arange(xmin,xmax),
                                np.arange(ymin,ymax))
                if len(pos)>2:
                    zmin = max(tmpOperand.shape[2],pos[2]-r)
                    zmax = min(tmpOperand.shape[2],pos[2]+r+1)
                    ixgrid = np.ix_(np.arange(xmin,xmax),
                                    np.arange(ymin,ymax),
                                    np.arange(zmin,zmax))
                tmpRegion = tmpOperand.data[ixgrid]
                labelledRegions = tmpRegion != OpSegmentationEdit._BACKGROUND
                if (labelledRegions).any():
                    #Update pos to nearest labelled region
                    tmp = np.where(labelledRegions==True) #Indexes pairs
                    pos = (tmp[0][0],tmp[1][0]) #Choose the first index pair
                    if len(tmp) == 3:
                        pos = (tmp[0][0],tmp[1][0],tmp[2][0]) #Choose the first index pair
                    flagFound = True
        else:
            #pos is in a labelled region
            flagFound = True
        
        self.activeROI = pos
        return flagFound

    def ROIChangeLabel(self, newClassID, pos=None):
        """Updates the label of the current active ROI
        
        Updates the label of the current active ROI or the selected ROI (if
        argument pos is provided).
        
        If provided, pos becomes the new py:attr:`activeROI`
        
        ..note: This removes the current active ROI from the segmentation, 
            since no pixel with the current label will remain in
            the segmentation. If you only want to affect some ROI, then
            use ROIChangeLabel instead.

        :param newClassID: A reference OCT scan
        :type newClassID: :class:`octant.data.OCTscan`
        :param pos: A pixel/voxel of the ROI; (x,y) or (x,y,z). Default None.
        :type pos: tuple or list
        :returns: The modified segmentation.
        :rtype: :class:`octant.data.OCTscanSegmentation`
        """

        self.result = self.operands[0]; #Start by copying operand into result
        
        if pos is not None:
            self.activeROI = pos
        
        if self.activeROI is None: #This may occur if trying to call the
                                   #operation right after creating this
                                   #object instance (when activeROI is None),
                                   #but still calling to execute operation
                                   #without parameters
            print(self.getClassName(),":ROIChangeLabel: No ROI selected. Passing...")
        else:
            print(self.getClassName(),":ROIChangeLabel: activeROI: ",
                    self.activeROI," with class ", self.getROILabel(),"; newClassID:",newClassID)
            idx = self.getROIPixels()
            #print(idx)
            self.result.data[idx] = newClassID
        return self.result


        
    def ROIDelete(self, pos = None):
        """Deletes the current active ROI and sets it to BACKGROUND
       
        Sets the label of the current active ROI or the selected ROI (if
        argument pos is provided) to BACKGROUND.
        
        If provided, pos becomes the new py:attr:`activeROI`

        :param pos: A pixel/voxel of the ROI; (x,y) or (x,y,z). Default None.
        :type pos: tuple or list
        :returns: The modified segmentation.
        :rtype: :class:`octant.OCTscanSegmentation`
        """
        self.result = self.operands[0]; #Start by copying operand into result
        
        if pos is not None:
            self.activeROI = pos
            
        if self.activeROI is None: #This may occur if trying to call the
                                   #operation right after creating this
                                   #object instance (when activeROI is None),
                                   #but still calling to execute operation
                                   #without parameters
            print(self.getClassName(),":ROIDelete: No ROI selected. Passing...")
        else:
            print(self.getClassName(),":ROIDelete: Deleting activeROI: ",
                    self.activeROI," with class ", self.getROILabel())
            idx = self.getROIPixels()
            #print(idx)
            self.result.data[idx] = OpSegmentationEdit._BACKGROUND
        return self.result
        



    #Manipulation of COI
    def COISelect(self,classID):
        """Select a COI by its label.
        
        Select a COI by its label. If the classID is not found in the
        segmentation, then the BACKGROUND is selected.
                
        :param classID: A class ID.
        :type classID: int
        :returns: True if the class ID is present in the segmentation or False
            otherwise (BACKGROUND selected).
        :rtype: bool
        """
        print(self.getClassName(),":COISelect: Selecting layer ", classID)
        
        tmpOperand = self.operands[0]; #Access operand
        
        self.activeCOI = OpSegmentationEdit._BACKGROUND
        idx = np.nonzero(tmpOperand.data == classID)
        if len(idx) != 0:
            self.activeCOI = classID
        
        return len(idx) != 0
        
    def COIDelete(self, classID = None):
        """Deletes the COI identified by classID.
        
        Deletes the COI identified by classID. Sets the COI to BACKGROUND
        If classID is None, then it works over the current active COI.
                
        :param classID: A class ID. Default None
        :type classID: int
        :returns: The modified segmentation.
        :rtype: :class:`octant.data.OCTscanSegmentation`
        """    
        self.result = self.operands[0]; #Start by copying operand into result
        
        if classID is None:
            #Operate over current active COI
            idx = np.nonzero(self.result.data == self.activeCOI)
                #WATCH OUT!
                #Distinctly from MATLAB, here I do not get a "list" of locations
                #indexing the array form 1 to numel(self.result). Instead,
                #a "coupled" pair of lists for the xIdx and yIdx are obtained.
                #
                #So to check whether it is "empty" I cannot do:
                #   len(idx)
                #...as this is equal to 2.
                #I must question "along a single dimension; e.g. len(idx[0])
                
            if len(idx[0]) == 0:
                print(self.getClassName(),":COIDelete: Layer ", self.activeCOI," not found. Skipping.")
            else:
                print(self.getClassName(),":COIDelete: Layer ", self.activeCOI," found. Deleting layer ", self.activeCOI)
                self.result.data[idx] = OpSegmentationEdit._BACKGROUND
                self.activeCOI = OpSegmentationEdit._BACKGROUND
        else:
            self.COISelect(classID)
            self.COIDelete()
        return self.result
        
    def COIChangeLabel(self, newClassID, coi=None):
        """Updates the label of the current active COI
        
        Updates the label of the current active COI or the selected COI (if
        argument coi is provided).
        
        The newClassID becomes the new updated COI.
        
        ..note: This removes the current active COI from the segmentation, 
            since no pixel with the current label will remain in
            the segmentation. If you only want to affect some ROI, then use
            func:`ROIChangeLabel` instead
                
        :param newClassID: The new class ID.
        :type newClassID: int
        :param coi: The class ID to be changed. Default None
        :type coi: int
        :returns: The modified segmentation.
        :rtype: :class:`octant.data.OCTscanSegmentation`
        """    
    
        self.result = self.operands[0]; #Start by copying operand into result
        
        if coi is not None:
            self.COISelect(coi)
            
        print(self.getClassName(),":COIChangeLabel: activeCOI:", self.activeCOI,"; newClassID:",newClassID)
        idx = np.nonzero(self.result.data == self.activeCOI)
        self.result.data[idx] = newClassID
        self.activeCOI = newClassID
        return self.result
        
        
        
