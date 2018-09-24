"""
-*- coding: utf-8 -*-

File: IOT_Operation.py

Class IOT_Operation

A general class for operations.

IOT stands for INAOE OCT Tools

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 4-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
+-------------+--------+------------------------------------------------------+
| 22-Aug-2018 | FOE    | - Rebranded to capital "O" in operation;             |
|             |        |   IOT_Operation                                      |
|             |        | - Updated known subclasses                           |
|             |        | - Defined method getClassName                        |
|             |        | - _arity attribute "downgraded" from class to        |
|             |        |   instance attribute                                 |
|             |        | - _arity get/set methods added                       |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx documentation to |
|             |        |   the class.                                         |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import warnings



## Class definition
class IOT_Operation(object):
    #Sphinx documentation
    """A base class for operations on IOT_OCTvolumes and IOT_OCTscans.

    A base class for operations on IOT_OCTvolumes and IOT_OCTscans.



    :Known subclasses:
    * IOT_OperationEditSegmentation
    * IOT_OperationFlattening
    * IOT_OperationMeasureLayerThickness
    * IOT_OperationPerfilometer
    * IOT_OperationSegmentation
    * IOT_OperationStitch

    .. seealso::
    .. note::
    .. todo::

    """




    #Private class attributes shared by all instances

    #Class constructor
    #
    def __init__(self,*args):
        """The class constructor.

        The IOT_Operation class constructor

        tmp = IOT_Operation() - Creates an operation of arity 1.
        tmp = IOT_Operation(n) - Creates an operation of arity n.

        :param n: the arity of the operation

        """
        if (len(args)>1):
            warnMsg = self.getClassName() + ':__init__: Unexpected number of input arguments.'
            warnings.warn(warnMsg,SyntaxWarning)

        #Initialize attributes (without decorator @property)

        #Initialize properties (with decorator @property)
        n=1
        if (len(args)>0):
            n=args[0]
        self.arity = n #Set arity of the operation


    #Properties getters/setters
    @property
    def arity(self): #arity getter
        """Gets the operation arity.

        Property arity getter. Gets the operation arity.

        :returns: The operation arity.
        :rtype: int
        """
        return self.__arity

    @arity.setter
    def arity(self,d): #arity setter
        """Sets the operation arity.

        Property arity setter. Sets the operation arity. Arity of the operation
        has to be bigger or equal than 1.

        :param d: Operation arity
        :type d: int
        :returns: None

        """
        if d is None:
            d = 1
        elif d<1:
            warnMsg = self.getClassName() + ':getArity: ' \
                      + 'Arity must be a positive integer. Setting it to 1.'
            warnings.warn(warnMsg,SyntaxWarning)
            d = 1

        self.__arity = d;
        return

    #Private methods

    #Public methods
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

    def getArity(self):
        """Get the operation arity.

        Get the operation arity.


        .. deprecated:: 0.2
           Use property .arity instead.
        """
        warnMsg = self.getClassName() + ':getArity: Deprecated. ' \
                 + 'Use ' + self.getClassName() + '.arity instead.'
        warnings.warn(warnMsg,DeprecationWarning)
        return self.arity

    def setArity(self,d):
        """Set the operation arity.

        Set the operation arity.


        .. deprecated:: 0.2
           Use property .arity instead.
        """
        warnMsg = self.getClassName() + ':getArity: Deprecated. ' \
                 + 'Use ' + self.getClassName() + '.arity instead.'
        warnings.warn(warnMsg,DeprecationWarning)
        self.arity = d
        return
