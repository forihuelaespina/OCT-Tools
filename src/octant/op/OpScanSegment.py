"""
-*- coding: utf-8 -*-

File: OpSegmentScan.py

Class OpSegmentScan

A class for automatic segmentation of retinal layers from an OCT scan

Initial code isolated from previous file segment.py


:Log:

+-------------+--------+------------------------------------------------------+   
| Date        | Author | Description                                          |
+=============+========+======================================================+
| Feb-2018    | AACC   | - Class created.                                     |
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
|             |        |   segmentar.                                         |
+-------------+--------+------------------------------------------------------+
| 18-Oct-2018 | FOE    | - Now using the classes class:`IOT_OCTscan` and      |
|             |        |   class:`IOT_OCTscanSegmentation`.                   |
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
|             |        | - Previously deprecated method segmentar have now    |
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

import numpy as np
from skimage import feature, color
import cv2 #That's OpenCV
#import matlab.engine

#from version import __version__
from octant.data import OCTscan, OCTscanSegmentation
from octant.util import segmentationUtils
from .Operation import Operation



class OpScanSegment(Operation):
    #Sphinx documentation
    """A class for automatic segmentation of retinal layers from an OCT scan.
    
    A class for automatic segmentation of retinal layers from an OCT scan.
    
    The operation represented by this class generates a new
    :class:`octant.data.OCTscanSegmentation` for a :class:`octant.data.OCTscan`.

    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """

    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.

        #Set the operation name
        self.name = "Segmentation"
        
        #Initialize private attributes unique to this instance
        #self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        #self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #The segmented image
    
    
    #Private methods
        

    #Public methods
    def execute(self,*args,**kwargs):
        """Executes the operation on the :py:attr:`operands`.
        
        Executes the operation on the :py:attr:`operands` and stores the outcome
        in :py:attr:`result`. Preload operands using
        :func:`IOT:Operation.addOperand()`.
        
        :returns: Result of executing the operation.
        :rtype: :class:`IOT_OCTscanSegmentation`
        """
        #Ensure the operand has been set.
        if (len(self.operands <1)):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None
        
        imgin = self.operands[0]
        if type(imgin) is OCTscan:
            imgin=imgin.data

        #Define a default output
        segmentedImage = np.zeros(shape = (0,0,0), dtype = np.uint8 );
        
        
        #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
        #and convert to grayscale if necessary
        #img = cv2.cvtColor(self._imgin, cv2.COLOR_BGR2GRAY)
        if imgin.ndim == 2:
            #Dimensions are only width and height. The image is already in grayscale.
            img=imgin
        elif imgin.ndim == 3:
            #Image is in RGB. Convert.
            img=color.rgb2gray(imgin);
        else: #Unexpected case. Return warning
            print(self.getClassName(),": Unexpected image shape.")
            return None
        
        
        
        
        ## Algoritmo 1: Basado en el código de Matlab CASeReL
        # https://pangyuteng.github.io/caserel/
        #
        # Llama externamente a retSegment.exe
        #
        # Requiere de Matlab Runtime environment 
        
        
       #  #Remove external noise from image
       #  img = segmentationUtils.ejecuta_close(img,4,4) #Clausura
       #  #segmentationUtils.mostrar_imagen(img)
       #  
       #  #Generate temporal intermediate image file to be processed externally
       #  tmpFilename = "paso2.tiff"
       #  cv2.imwrite(tmpFilename, img)
       #  
       #  #Rely externally on the matlab algorithm for segmentation
       # # eng = matlab.engine.start_matlab()
       # # eng.retSegment(img)
       #  #segmentationUtils.mostrar_imagen(img)
       #  
       #  #Delete the intermediate image file
       #  segmentationUtils.elimina_imagen(tmpFilename)
        
        
        
        
        ## Algoritmo 2: Arlem
        img2 = img

        #Elimina ruido
        img = segmentationUtils.ejecuta_close(img,4,4)
        
        #Amplifica capas
        img = segmentationUtils.ejecuta_dilate(img,5,20,1)
        
        #Tensor
        Axx, Axy, Ayy = feature.structure_tensor(img)
        
        #Elimina mas ruido
        Ayy = segmentationUtils.ejecuta_close(Ayy,6,1)
        
        #Resalta las capas que sean mayores a la media
        Ayy = segmentationUtils.resalta_bordes(Ayy,True,0)
        
        #Elimina aun mas ruido
        Ayy = segmentationUtils.ejecuta_open(Ayy,1,1)
        
        #Binarizacion
        binary = segmentationUtils.ejecuta_OTSU(Ayy)
        
        #elimina ruido del posible borde superior
        binary = segmentationUtils.ejecuta_elimina_ruido_extremos(True,0,0,binary)
        
        #elimina ruido del posible borde inferior
        binary = segmentationUtils.ejecuta_elimina_ruido_extremos(False,0,0,binary)
        
        #obtiene bordes exteriores
        arraySuperior, arrayInferior = segmentationUtils.obten_bordes_externos(binary)
        
        #elimina ruido a la imagen original
        img2 = segmentationUtils.elimina_desde_arreglos(img2, arraySuperior, arrayInferior)
        img2 = segmentationUtils.ejecuta_close(img2,2,1)
        img2 = feature.canny(img2,sigma = 2.5)
        img2 = segmentationUtils.elimina_ruido_canny(img2,1)
        
                
        print(self.getClassName(),": execute: Finishing retinal layer segmentation")
        
        
        #if isinstance(imgin,(OCTscan,)):
        if type(imgin) is OCTscan:
            self.result=OCTscanSegmentation(imgin)
        else:
            self.result=OCTscanSegmentation(OCTscan(imgin))
        self.result.data = img2

        return self.result    




#    #@deprecated(version='0.2', reason="Deprecated. Use method execute() instead.")
#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Use method execute() instead.")
#    def segmentar(self,image):
#        #Encapsulate the image as an OCTscan
#        tmp=OCTscan(image)
#        self.clear()
#        self.addOperand(tmp)
#        #Execute
#        self.execute()
#        return None

