"""
-*- coding: utf-8 -*-

File: OpScanStitch.py

Class OpScanStitch

This class makes a mosaic from several images.

Initial code isolated from previous file stitch.py


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 3-Aug-2018  | FOE    | - Added a comment section.                           |
|             |        | - Removed importing pyimagesearch.panorama (this was |
|             |        |   actually a function defined in the original        |
|             |        |   example)                                           |
|             |        | - Removed default values for parameters of function  |
|             |        |   stitch, and added an internal parameter check on   |
|             |        |   the function.                                      |
+-------------+--------+------------------------------------------------------+   
| 5-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
+-------------+--------+------------------------------------------------------+   
| 22-Aug-2018 | FOE    | - Rebranded to capital "O" in operation;             |
|             |        |   IOT_Operation                                      |
|             |        | - Improved verbosity; now using class name           |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx                  |
|             |        |   documentation to the class                         |
+-------------+--------+------------------------------------------------------+
| 17-Oct-2018 | FOE    | - Adapted to IOT_Operation becoming abstract and new |
|             |        |   capabilities. Added method .execute, integration of|
|             |        |   operands, given operation name, deprecated method  |
|             |        |   stitch.                                            |
+-------------+--------+------------------------------------------------------+
|  5-Nov-2018 | FOE    | - Minor debugging                                    |
+-------------+--------+------------------------------------------------------+
|  1-Dec-2018 | FOE    | - Adapted to new signature of inherited execute()    |
|             |        |   method to accept parameters.                       |
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
|             |        | - Previously deprecated method stitch has now        |
|             |        |   been fully removed.                                |
+-------------+--------+------------------------------------------------------+
|  3-Feb-2019 | FOE    | - Debugging of errors left during transition to new  |
|             |        |   package OCTant structure; wrong imports and        |
|             |        |   unupdated classes names.                           |
+-------------+--------+------------------------------------------------------+
|  5-May-2019 | FOE    | - Adapted call to panorama to work correctly with    |
|             |        |   latest changes.                                    |
+-------------+--------+------------------------------------------------------+
| 19-May-2019 | FOE    | - Added property homographyMatrix to hold the        |
|             |        |   homography matrix resulting from the stitching.    |
+-------------+--------+------------------------------------------------------+
|  1-Jun-2019 | FOE    | - Added property switchedOperands to flag whether    |
|             |        |   switching the order of the operands was needed.    |
|             |        |   during stitching.                                  |
|             |        | - Added property sparedCols to mark the size of the  |
|             |        |   "black" spared region.                             |
|             |        | - Added method applyStitch to repeat a known         |
|             |        |   sticthing to operands. This can be used to apply   |
|             |        |   the same stitch to a different set of scans. In    |
|             |        |   practical terms, it can be used to apply the same  |
|             |        |   panoramic stitching to segmentation scans after    |
|             |        |   it has been precalculated to anatomical scans.     |
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
#import deprecation

#from pyimagesearch.panorama import Stitcher
#import argparse
import numpy as np

#from version import __version__
from octant.data import OCTscan
from octant.util.panorama import Stitcher
from .Operation import Operation


## Class definition
class OpScanStitch(Operation):
    #Sphinx documentation
    """This class makes a mosaic from two :class:`octant.data.OCTscan` .
    
    This class makes a mosaic from two :class:`octant.data.OCTscan` .
    
    The operation represented by this class corresponds to a binary
    operation by which a mosaic is created from two images by shifting
    one over the other until optimal matching.

    :Usage:
      python stitch.py --first images/bryce_left_01.png --second images/bryce_right_01.png 
      Original example imported from web. Likely from:
      https://github.com/haurbano/PythonPanorama
      or
      https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
    
    
    .. seealso:: None
    .. note:: The result will have a different shape from the operands.
    .. todo:: Currently it can only stitch two images. This should be generalized to n
        images. In the meantime, stitching more than two images requires
        instatiating this class several times.

        
    """

    #Private class attributes shared by all instances
    

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__()
        
        #Set the operation name
        self.name = "Stitching"
        
        #Initialize private attributes unique to this instance
        self.homographyMatrix = None
        self.sparedCols = 0
        self.switchedOperands = False
        
        return
    

    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def homographyMatrix(self): #property getter
        """
        The homography matrix of the most recent execution of the
        stitching operation.

        :getter: Gets the homography matrix.
        :setter: Sets the homography matrix.
        :type: np.array
        """
        return self.__homographyMatrix


    @homographyMatrix.setter
    def homographyMatrix(self,H): #property setter
        #if (not isinstance(opList,(list,))):
        if H is None:
            self.__homographyMatrix = None;
        elif type(H) is not np.ndarray:
            warnMsg = self.getClassName() + ':homographyMatrix: Unexpected type. ' \
                            'Please provide homographyMatrix as a np.ndarray.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__homographyMatrix = H;
        return None

    @property
    def sparedCols(self): #property getter
        """
        Last valid pixel column before the spared region resulting from the stitching.
        
        :getter: Gets the sparedCols.
        :setter: Sets the sparedCols.
        :type: int
        """
        return self.__sparedCols


    @sparedCols.setter
    def sparedCols(self,val): #property setter
        #if (not isinstance(opList,(list,))):
        if type(val) is not int:
            warnMsg = self.getClassName() + ':sparedCols: Unexpected type. ' \
                            'Please provide sparedCols as a int.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__sparedCols = val;
        return None

    @property
    def switchedOperands(self): #property getter
        """
        The flag for operand switching of the most recent execution of the
        stitching operation.
        
        The flag indicates whether operands were switched during stitching.
        
        :getter: Gets the switchedOperands.
        :setter: Sets the switchedOperands.
        :type: bool
        """
        return self.__switchedOperands


    @switchedOperands.setter
    def switchedOperands(self,flag): #property setter
        #if (not isinstance(opList,(list,))):
        if type(flag) is not bool:
            warnMsg = self.getClassName() + ':switchedOperands: Unexpected type. ' \
                            'Please provide switchedOperands as a bool.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__switchedOperands = flag;
        return None

    # #Private methods


    #Public methods
    def execute(self,*args,**kwargs):
        """Executes the operation on the :py:attr:`operands`.
        
        Executes the operation on the :py:attr:`operands` and stores the outcome
        in :py:attr:`result`. Preload operands using
        :func:`octant.data.Operation.addOperand()`.
        
        :returns: Result of executing the operation.
        :rtype: :class:`octant.data.OCTscan`
        """
        #print(self._getClasName(),": flattening: Starting flattening")
        
        #Ensure the operand has been set.
        if (self.arity() <2):
            warnMsg = self.getClassName() + ':execute: Operands not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None
        
        imageA = self.operands[0]
        if type(imageA) is OCTscan:
            imageA=imageA.data
        
        imageB = self.operands[1]
        if type(imageB) is OCTscan:
            imageB=imageB.data
        
        if ( imageA is None and imageB is None ):
            print(self.getClassName(),": No images selected. Generating a default empty stitch of arbitrary size.")
            result = np.zeros((100,100,3),dtype=np.uint8)
    
        elif ( imageA is None ):
            print(self.getClassName(),": First image not selected. Returning second image unmodified.")
            result = imageB
    
        elif ( imageB is None ):
            print(self.getClassName(),": Second image not selected. Returning first image unmodified.")
            result = imageA
        
        else:
            #Normal behaviour of the function
            
            # stitch the images together to create a panorama
            stitcher = Stitcher()
            (result, vis) = stitcher.stitch([imageB, imageA], ratio=0.9, showMatches=True)
            print('Img 1 (' + str(imageA.shape) +')' \
                  'Img 2 (' + str(imageB.shape) +')' \
                  ' -> Res (' + str(result.shape) +')')
            print('Matches; ' + str(vis.shape))
            self.homographyMatrix = stitcher.homographyMatrix
            self.switchedOperands = stitcher.switchedOperands
            print('Switched operands? ' + str(self.switchedOperands))
            
            #Remove the "black" spared region on the "right" due to
            #shifting imageB over imageA
            width = result.shape[1]
            flagStop = False
            col=width-1
            self.sparedCols = width #By default there is no spared region
            while not flagStop:
                if (result[:,col,:]==0).all():
                    result=np.delete(result,col,1)
                    self.sparedCols = col
                else:
                    flagStop=True
                col = col - 1
        print("Spared cols: " +str(self.sparedCols))
        #self.result = OCTscan(vis) #In case I want to see the matches
        self.result = OCTscan(result)
        
        return self.result

#    #@deprecated(version='0.2', reason="Deprecated. Use method execute() instead.")
#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Use method execute() instead.")
#    def stitch(self,imageA, imageB):
#        #Encapsulate the image as an OCTscan
#        tmp1=OCTscan(imageA)
#        tmp2=OCTscan(imageB)
#        self.clear()
#        self.addOperand(tmp1)
#        self.addOperand(tmp2)
#        #Execute
#        self.execute()


    def applyStitch(self, scanA, scanB):
        """Apply the current stitching (see property homographyMatrix) to the
        given scans.
        
        Instead of calculating the homography matrix needed for the
        stitching, this method applies a known homography matrix to
        the current set of operands.
        
        If operands were switched during the last call to :func:`execute()`
        the parameters here will also be switched.
        
        The result is NOT stored in :py:attr:`result`.
        
        :param scanA: First image to stitch.
        :type scanA: :class:`octant.data.OCTscan`
        :param scanB: First image to stitch.
        :type scanB: :class:`octant.data.OCTscan`
        :returns: Result of repeating the last stitching the operation onto
             parameters scanA and scanB .
        :rtype: :class:`octant.data.OCTscan`
        """
        
        if type(scanA) is OCTscan:
            scanA=scanA.data
        
        if type(scanB) is OCTscan:
            scanB=scanB.data
        
        stitcher = Stitcher()
        if self.switchedOperands:
            print('Applying stitch over switched operands')
            result = stitcher.applyStitch([scanA, scanB],
                        H=self.homographyMatrix, switchedOperands=False)
        else:
            result = stitcher.applyStitch([scanB, scanA],
                        H=self.homographyMatrix, switchedOperands=False)
        
        #Finally, remove the spared black region
        width = result.shape[1]
        result=np.delete(result,range(self.sparedCols,width),1)
        print('Applying Stitch: Img 1 (' + str(scanA.shape) +')' \
              'Img 2 (' + str(scanB.shape) +')' \
              ' -> Res (' + str(result.shape) +')')
        return OCTscan(result)
