# File: IOT_Operation.py
#
# A general class for operations.
# 
# IOT stands for INAOE OCT Tools
#
# By now it is just an empty class to be the superclass of other image
#operations.
#
# Known subclasses:
#   * IOT_OperationEditSegmentation
#   * IOT_OperationFlattening
#   * IOT_OperationMeasureLayerThickness
#   * IOT_OperationPerfilometer
#   * IOT_OperationSegmentation
#   * IOT_OperationStitch
#
#
# @dateCreated: 4-Aug-2018
# @authors: Felipe Orihuela-Espina
# @dateModified: 22-Aug-2018
#
# See also:
# 


## Log
#
# 4-Aug-2018: FOE:
#   * Isolated minimal solution.
#   * Encapsulated in class.
#
# 22-Aug-2018: FOE:
#   * Rebranded to capital "O" in operation; IOT_Operation
#   * Updated known subclasses
#   * Defined method getClassName
#   * _arity attribute "downgraded" from class to instance attribute
#   * _arity get/set methods added
#



## Import



## Class definition
class IOT_Operation(object):
    
    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self,arity):
        #Initialize attributes
        self._arity = arity #Set arity of the operation
  
  
    #Private methods
    
    #Public methods
    def getClassName(self):
        return type(self).__name__

    def getArity(self):
        return self._arity

    def setArity(self,a):
        if d is None:
            d = 1
        self._arity = d;
        return
  

    