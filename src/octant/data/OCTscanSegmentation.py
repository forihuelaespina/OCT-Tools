"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: OCTscanSegmentation.py

Class :class:`octant.data.OCTscanSegmentation`

A retinal layer segmentation over a :class:`octant.data.OCTscan`

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 18-Oct-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
|  2-Dec-2018 | FOE    | - Minor debugging.                                   |
|             |        | - Added read only property shape                     |
+-------------+--------+------------------------------------------------------+
| 20-Dec-2018 | FOE    | - Minor debugging. Assigment of property classMap    |
|             |        |   in property setter was being "assigned" to cm.     |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded OCTscanSegmentation. The prefix    |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
+-------------+--------+------------------------------------------------------+
|  4-Apr-2019 | FOE    | - Minor debugging. Updated call from `IOT_OCTScan` to|
|             |        |   :class:`octant.data.OCTscan` in class constructor. |
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
#from skimage import color

from octant import version
import octant.data as octant


## Class definition
class OCTscanSegmentation(object):
    #Sphinx documentation
    """A retinal layer segmentation over a :class:`octant.data.OCTscan`

    A retinal layer segmentation over a :class:`octant.data.OCTscan`. A segmentation 
    assigns every pixel of the scan a class label.
    
    Please note that this is a data model class; it keeps the segmentation
    but it is NOT capable of "computing" such segmentation. To compute a
    segmentation please refer to :class:`octant.op.OpScanSegment`.
    
    The segmentation is sized and shaped equal to its base
    :class:`octant.data.OCTscan`.
    
    A default segmentation sets the whole segmentation to BACKGROUND.
    
    .. seealso:: :class:`octant.data.OCTscan`, :class:`octant.op.OpScanSegment`
    .. note:: None
    .. todo:: None

    """

    _BACKGROUND = 0 #The background label identifier


    #Class constructor
    def __init__(self,*args):
        """The class constructor.

        The class constructor.

        tmp = OCTscanSegmentation(theOCTScan) - Creates a default 
            segmentation for the given :class:`octant.data.OCTscan`

        :param theOCTScan: The OCT scan to be segmented
        :type img: :class:`octant.data.OCTscan`
        
        """
        refImage = octant.OCTscan(); #Dummy reference
        if (len(args)==0):
            warnMsg = self.getClassName() + ':__init__: Unexpected number of input arguments. Generating a dummy reference scan.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            refImage = args[0]
            # if type(refImage) is not octant.OCTscan:
            #     raise ErrorValue #Throw error

        #Initialize attributes (without decorator @property)

        #Initialize properties (with decorator @property)
        self.scan = refImage #The OCT scan over which the segmentation is made
        self.data = self._BACKGROUND*np.ones(refImage.shape) #The segmentation itself
        self.classMap = octant.RetinalLayers().layers #The map of class labels
        
        return

    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def data(self): #data getter
        """
        The segmentation labels map. Please refer to :py:attr:`classMap` for
        classes.
        
        ..note: WARNING! This method is not currently checking whether the
            data is sized equal to the scan. This may become a problem later.
            The problem is that trying to check scan.shape will raise an
            error during object creation, when attemting to set the data
            but because the object has not been created yet, it still lacks
            the scan property even if declared in advance. 

        :getter: Gets the segmentation map
        :setter: Sets the segmentation map 
        :type: numpy.ndarray shaped [width,height]
        """
        return self.__data

    @data.setter
    def data(self,segmentedImg): #data setter
        self.__data = segmentedImg;
        # if segmentedImg is not None:
        #     #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
        #     #and convert to grayscale if necessary
        #     if ((segmentedImg.ndim == 2) & (segmentedImg.shape == self.scan.shape)):
        #         #Dimensions are only width and height, and matches that of
        #         #the scan.
        #         self.__data = segmentedImg;
        #     else: #Unexpected case. Return warning
        #         warnMsg = self.getClassName() + ':data: Unexpected segmentation shape.'
        #         warnings.warn(warnMsg,SyntaxWarning)
        return None


    @property
    def scan(self): #scan getter
        """
        The base OCT scan. Please refer to :py:attr:`data` for
        the segmentation map.

        :getter: Gets the base OCT scan
        :setter: Sets the base OCT scan
        :type: :class:`octant.data.OCTscan`
        """
        return self.__scan

    @scan.setter
    def scan(self,octScan): #scan setter
        if octScan is not None:
            #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
            #and convert to grayscale if necessary
            if type(octScan) is octant.OCTscan:
                #Dimensions are only width and height, and matches that of
                #the scan.
                self.__scan = octScan;
                self.clear()                
            else: #Unexpected case. Return warning
                warnMsg = self.getClassName() + ':data: Unexpected type for OCT scan.'
                warnings.warn(warnMsg,SyntaxWarning)
        return None


    @property
    def shape(self): #shape getter
        """
        The scan segmentation shape [width,height].
        
        :getter: Gets the scan segmentation shape
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
    def classMap(self): #classMap getter
        """
        The map of classes.
        
        The map of classes; the list of class names associated to each
        value in the segmentation map.
        
        ..note: This list does NOT include the BACKGROUND class.

        :getter: Gets the base OCT scan
        :setter: Sets the base OCT scan
        :type: :class:`octant.data.OCTscan`
        """
        return self.__classMap

    @classMap.setter
    def classMap(self,cm): #classMap setter
        if cm is not None:
            #Check that we are receiving the correct type
            if type(cm) is dict:
                self.__classMap = cm;
            else: #Unexpected case. Return warning
                warnMsg = self.getClassName() + ':classMap: Unexpected type for classMap.'
                warnings.warn(warnMsg,SyntaxWarning)
        return None



    #Private methods
    def __str__(self):
        s = '<' + self.getClassName() + '([' \
            + '  scan: ' + format(self.scan) + ',' \
            + '  data: ' + format(self.data) + ',' \
            + '  classMap: ' + format(self.classMap) + '])>'
        return s


    #Public methods
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

        
    def clear(self):
        """Clears/Resets the segmentation map to _BACKGROUND.
        
        Clears/Resets the segmentation map to _BACKGROUND. All pixels are
        assigned the background label.
        
        """
        self.data = self._BACKGROUND*np.ones(self.scan.shape)
        return None