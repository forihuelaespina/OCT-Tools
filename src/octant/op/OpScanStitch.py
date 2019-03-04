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

#from pyimagesearch.panorama import Stitcher
#import argparse
import numpy as np
import imutils
import cv2 #That's OpenCV

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

            #Panorama works only from RGB images
            #...so convert to RGB if grayscales
            if(len(imageA.shape)<3):
                #print('**Converting to RGB')
                #print(imageA)
                imageA = np.dstack((imageA, imageA, imageA))
                #print(imageA)
            
            if(len(imageB.shape)<3):
                imageB = np.dstack((imageB, imageB, imageB))
                

            
            # stitch the images together to create a panorama
            stitcher = Stitcher()
            #print(imageA)
            #print(imageB)
            (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
            
            #Remove the "black" unused region on the "right" due to
            #shifting imageB over imageA
            width = result.shape[1]
            flagStop = False
            col=width-1
            while not flagStop:
                if (result[:,col,:]==0).all():
                    result=np.delete(result,col,1)
                else:
                    flagStop=True
                col = col - 1
                    
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
