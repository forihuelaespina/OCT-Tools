"""
-*- coding: utf-8 -*-

File: IOT_OperationStitch.py

Class IOT_OperationStitch

This class makes a mosaic from several images

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

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
from IOT_Operation import IOT_Operation

#from pyimagesearch.panorama import Stitcher
from panorama import Stitcher
#import argparse
import numpy as np
import imutils
import cv2 #That's OpenCV



## Class definition
class IOT_OperationStitch(IOT_Operation):
    #Sphinx documentation
    """This class makes a mosaic from several OCT scans.
    
    This class makes a mosaic from several OCT scans.
    
    :Usage:
    python stitch.py --first images/bryce_left_01.png --second images/bryce_right_01.png 
    Original example imported from web. Likely from:
    https://github.com/haurbano/PythonPanorama
    or
    https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
    
    
    :Known issues:
    + Currently it can only stitch two images. This shod be generalized to n
    images. In the meantime, stitching more than two images requires
    instatiating this class several times.
    

    .. seealso:: 
    .. note:: 
    .. todo:: 
        
    """

    #Private class attributes shared by all instances
    

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(2) #Set operation arity to 2.
        #Initialize private attributes unique to this instance
        self._inimgA  = np.zeros(shape = (0,0,0), dtype = np.uint8 ) #input image A
        self._inimgB  = np.zeros(shape = (0,0,0), dtype = np.uint8 ) #input image B
        self._outimg = np.zeros(shape = (0,0,0), dtype = np.uint8 ) #output image result from the operation
    
    

    # #Private methods


    #Public methods
    def stitch(self,imageA, imageB):
        
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
            (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
        
        self._outimg = result
        return result

