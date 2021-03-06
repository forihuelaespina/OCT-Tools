"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: Operation.py

Class Operation

A general abstract class for operations. Operations are functions over some
objects of the data model e.g. over an :class:`octant.data.OCTscan` or a
:class:`octant.data.OCTscanSegmentation`.

An operation can have any number of operands , and can be:

    * internal i.e. produce an object of the same type as the operands, or
    * external i.e. produce an object of different type as the operands.

In addition, since v0.3 the :class:`octant.op.Operation` also provides
support for operation parameters (e.g. the betas of a regression model).
The difference between operands and parameters from the mathematical point
of view is merely conceptual, as parameters when present are nothing
more than additional operands. However, the distinction is important
for the arity; only operands count towards the arity of the function.

Subclasses are encourage to follow the following class name convention:

'Op' + <MainOperandType> + <OperationName>

For instance;

    * :class:`octant.data.OpScanFlattening` which flattens an OCT scan.
    * :class:`octant.data.OpSegmentationEdit` which edits an OCT scan segmentation.


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
|             |        | - _arity attribute "upgraded" from attribute to      |
|             |        |   property arity and property getter/setter added    |
|             |        | - _arity get/set methods deprecated.                 |
+-------------+--------+------------------------------------------------------+
| 26-Sep-2018 | FOE    | - The class becomes abstract and a new abstract      |
|             |        |   method execute is provided.                        |
|             |        | - Added support to hold operands.                    |
|             |        | - Arity now becomes only the number of the operands. |
|             |        |   get/setArity methods are now deprecated            |
+-------------+--------+------------------------------------------------------+
|  1-Dec-2018 | FOE    | - Signature of execute() method now accepts          |
|             |        |   parameters and return result instead of None.      |
+-------------+--------+------------------------------------------------------+
| 20-Jan-2018 | FOE    | - Added method setOperand.                           |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded Operation. The prefix              |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
|             |        | - New support for operations parameters.             |
|             |        | - Added new comments on the class description.       |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import warnings
from abc import ABC, abstractmethod



## Class definition
class Operation(ABC):
    #Sphinx documentation
    """An abstract base class for operations on :class:`octant.data.OCTvolume` and :class:`octant.data_OCTscan` .

    An abstract base class for operations on :class:`octant.data.OCTvolume` and
    :class:`octant.data.OCTscan`.

    :Example:

        tmp = octant.data.OCTscan(img)
        o = octant.op.OpScanFlattening()
        o.addOperand(tmp)
        o.arity() #return 1
        o.execute() #Flattens the image


    :Known subclasses:

    * :class:`OpScanFlattening`
    * :class:`OpScanMeasureLayerThickness`
    * :class:`OpScanPerfilometer`
    * :class:`OpScanSegment`
    * :class:`OpScanStitch`
    * :class:`OpSegmentationBrush`
    * :class:`OpSegmentationEdit`

    .. seealso:: None
    .. note:: None
    .. todo::
        * Support to hold operand names.

    """




    #Private class attributes shared by all instances

    #Class constructor
    #
    def __init__(self,**kwargs):
        """The class constructor.

        The class constructor. Creates an empty operation

        """
        super().__init__()

        #Initialize attributes (without decorator @property)

        #Initialize properties (with decorator @property)
        self.name = 'Operation' #The operation name
        self.operands = list() #Operands
        self.parameters = list() #Parameters
        self.result = None #Operation outputs (a list in case it is multivalued).
                           #None until executed or cleared.

        if kwargs is not None:
            for key, value in kwargs.items():
                if (key=='name'):
                    self.name = value

        return

    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def operands(self): #operands getter
        """
        The list of operands.

        :getter: Gets the list of operands
        :setter: Sets the list of operands.
        :type: list
        """
        return self.__operands


    @operands.setter
    def operands(self,opList): #operands setter
        #if (not isinstance(opList,(list,))):
        if type(opList) is not list:
            warnMsg = self.getClassName() + ':operands: Unexpected type. ' \
                            'Please provide operands as a list.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__operands = opList;
        return None

    @property
    def name(self): #name getter
        """
        The operation name

        :getter: Gets the operation name
        :setter: Sets the operation name.
        :type: string
        """
        return self.__name

    @name.setter
    def name(self,opName): #name setter
        #if (not isinstance(opName,(str,))):
        if type(opName) is not str:
            warnMsg = self.getClassName() + ':name: Unexpected type. ' \
                            'Operations name must be a string.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__name = opName;
        return None


    @property
    def parameters(self): #operands getter
        """
        The list of parameters.

        :getter: Gets the list of parameters
        :setter: Sets the list of parameters.
        :type: list
        """
        return self.__parameters


    @parameters.setter
    def parameters(self,opList): #operands setter
        #if (not isinstance(opList,(list,))):
        if type(opList) is not list:
            warnMsg = self.getClassName() + ':parameters: Unexpected type. ' \
                            'Please provide operands as a list.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__parameters = opList;
        return None


    @property
    def result(self): #result getter
        """
        The list of results.

        This is a read only property. There is no setter method.

        :getter: Gets the list of results
        :setter: Sets the list of results
        :type: list
        """
        return self.__result


    @result.setter
    def result(self,rList): #result setter
        self.__result = rList;
        return None


    #Private methods
    def __str__(self):
        tmp = '['
        for x in self.operands:
            tmp += format(x) + ','
        tmp+=']'
        s = '<' + self.getClassName() + '([' \
            + 'name: ' + self.name + ';' \
            + ' operands: ' + tmp + '])>'
        return s

    #Public methods
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

    def addOperand(self,op,i=None):
        """
        Add a new operand.

        :param op: The operand.
        :type op: object
        :param i: (optional) The operand order. If given it may shift the
            order of other operands already set. If not given, the operand
            is appended at the end of the list of operands.
        :type op: int
        :return: None
        """
        if (i is None):
            self.__operands.append(op)
        else:
            self.__operands.insert(i,op)
        return None

    def setOperand(self,op,i):
        """
        Set an operand; substitutes an existing operand with a new one.

        Calling setOperand when the :py:attr:`i`-th operand has not been
        previously set will result in an out-of-range error.

        :param op: The new operand.
        :type op: object
        :param i: The operand order. Operand index is zero-base i.e. the
            first operand occupies i=0
        :type op: int
        :return: None
        """
        self.__operands[i] = op
        return None

    def addParameter(self,param,i=None):
        """
        Add a new parameter.

        :param op: The parameter.
        :type op: object
        :param i: (optional) The paremeter order. If given it may shift the
            order of other parameters already set. If not given, the parameter
            is appended at the end of the list of parameters.
        :type op: int
        :return: None
        """
        if (i is None):
            self.__parameters.append(op)
        else:
            self.__parameters.insert(i,op)
        return None

    def setParameter(self,op,i):
        """
        Set a parameter; substitutes an existing parameter with a new one.

        Calling setParameter when the :py:attr:`i`-th parameter has not been
        previously set will result in an out-of-range error.

        :param op: The new operand.
        :type op: object
        :param i: The operand order. Operand index is zero-base i.e. the
            first operand occupies i=0
        :type op: int
        :return: None
        """
        self.__operands[i] = op
        return None

    def arity(self):
        """Gets the operation arity (number of operands).

        :return: The operation arity
        :rtype: int
        """
        return len(self.__operands)

    def clear(self):
        """
        Clears the operands; Removes all operands.

        :return: None
        """
        self.__operands = list()
        return None

    #@abstractmethod
    def execute(self,*args,**kwargs):
        """Executes the operation on the operands.

        This is an abstract method. Executes the operation on the .operands
        and stores the outcome in .result

        Operation meta-parameters may be also passed.

        :returns: Result of executing the operation.
        :rtype: Type of result -depends on subclass implementation-.
        """
        pass
