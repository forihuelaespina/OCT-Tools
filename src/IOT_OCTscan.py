"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: IOT_OCTscan.py

Class IOT_OCTscan

A single (grayscale) OCT scan

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 25-Aug-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 26-Aug-2018 | FOE    | - Added property scantype.                           |
|             |        | - Added __repr__ and __str__ methods                 |
+-------------+--------+------------------------------------------------------+
| 20-Jan-2019 | FOE    | - Default scan is now NOT empty, but a default black |
|             |        |   image of an arbitrary size 480(H)x640(W) pixels.   |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import warnings

import numpy as np
from skimage import color


## Class definition
class IOT_OCTscan(object):
    #Sphinx documentation
    """A single OCT scan.

    A single OCT scan. A scan is a grayscale image.
    
    Check .scantype property for the scan type (A, B or C)

    .. seealso:: :class:`IOT_OCTvolume`
    .. note:: None
    .. todo:: Upgrade to color scans.

    """

    #Class constructor
    def __init__(self,*args):
        """The class constructor.

        The class constructor.

        tmp = IOT_OCTscan() - Creates an black scan sized 480x640.
        tmp = IOT_OCTScan(img) - Creates scan from the (grayscale) image. Assumed to be an A scan.
        tmp = IOT_OCTScan(img,type) - Creates scan from the (grayscale) image.

        :param img: The scan image
        :type img: numpy.ndarray
        :param type: The scan type ('A' -default-, 'B' or 'C')
        :type type: char
        
        """
        if (len(args)>1):
            warnMsg = self.getClassName() + ':__init__: Unexpected number of input arguments.'
            warnings.warn(warnMsg,SyntaxWarning)

        #Initialize attributes (without decorator @property)

        #Initialize properties (with decorator @property)
        self.data = np.zeros(shape = (480,640), dtype = np.uint8 ) #The default scan image
        self.scantype = 'A'

        if (len(args)>0):
            self.data=args[0]
        if (len(args)>1):
            self.scantype=args[1]
            
        return

    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def data(self): #data getter
        """
        The (grayscale) scan image. The image is expected to be
        a grayscale image. Colour images will be converted to grayscale.

        :getter: Gets the OCT scan image
        :setter: Sets the OCT scan image. 
        :type: numpy.ndarray shaped [width,height]
        """
        return self.__data

    @data.setter
    def data(self,img): #data setter
        if img is not None:
            #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
            #and convert to grayscale if necessary
            if img.ndim == 2:
                #Dimensions are only width and height. The image is already in grayscale.
                pass
            elif img.ndim == 3:
                #Image is in RGB. Convert.
                img=color.rgb2gray(img);
            else: #Unexpected case. Return warning
                warnMsg = self.getClassName() + ':data: Unexpected image shape.'
                warnings.warn(warnMsg,SyntaxWarning)
            self.__data = img;
        return None

    @property
    def shape(self): #shape getter
        """
        The scan shape [width,height].
        
        :getter: Gets the scan shape
        :setter: None. This is a read-only property.
        :type: Tuple [width,height]
        """
        return self.__data.shape


    @shape.setter
    def shape(self,*args): #shape setter
        #Catching attempts to set the shape of the scan
        warnMsg = self.getClassName() + ':shape: shape is a read-only property.'
        warnings.warn(warnMsg,UserWarning)
        return

    @property
    def scantype(self): #scantype getter
        """
        The scan type; 'A', 'B' or 'C'.

        :getter: Gets the scan type.
        :setter: Sets the scan type.
        :type: char 'A', 'B' or 'C'.
        """
        return self.__scantype


    @scantype.setter
    def scantype(self,*args): #shape setter
        stype=args[0].upper() #Uppercase
        if (not stype in ('A','B','C')):
            warnMsg = self.getClassName() + ':scantype: Scan type can only be ''A'', ''B'' or ''C''.'
            warnings.warn(warnMsg,SyntaxWarning)
        self.__scantype = stype;
        return None

    #Private methods
    def __str__(self):
        s = '<' + self.getClassName() + '([' \
            + '  data: ' + format(self.data) + ',' \
            + '  shape: ' + format(self.shape) + ',' \
            + '  scantype: ' + self.scantype + '])>'
        return s


    #Public methods
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

        
    