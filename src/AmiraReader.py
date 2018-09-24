"""
-*- coding: utf-8 -*-

File: AmiraReader.py

Class AmiraReader

The original code was created from a web example by Felipe in Matlab and
then "translated" to Python between Felipe and Arlem.

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 4-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
|             |        | - Class name updated to AmiraReader.                 |
|             |        | - Added comments and declared attributes.            |
|             |        | - Methods fread, findField and findStruct are now    |
|             |        |   private.                                           |
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


import numpy as np
import matplotlib.pyplot as plt
import os



class AmiraReader(object):
    #Sphinx documentation
    """A class to read Amira formatted files.

    A class to read Amira formatted files.


    :Known issues:

    * Currently it only returns the first scan

    .. seealso::
    .. note::
    .. todo::

    """

    #Private class attributes shared by all instances



    #Class constructor
    def __init__(self):
        #Initialize private attributes unique to this instance
        self._filename = "" #File name
        #self._fileFolder = "" #File folder



    #some private methods
    def _fread(self,fid, nelements, dtype):
        """Equivalent to Matlab fread function"""
        if dtype is np.str:
            dt = np.uint16  # WARNING: assuming 8-bit ASCII for np.str!
        else:
            dt = dtype
        data_array = np.fromfile(fid, dt, nelements)
        data_array.shape = (1,nelements)
        return data_array



    def _findField(self,file, fieldName):
        k = -1
        lineString = '';
        while isinstance(lineString, str) and k == -1:
            lineString = file.readline()
            k = lineString.find(fieldName)
        return lineString.lstrip("# "+fieldName+" ")



    def _findStruct(self,file, structName):
        lineString = self._findField(file, structName+" {")
        parameters = []
        if len(lineString.strip("\n"))>0:
            k = lineString.find("}")
            if k != -1:
                parameters += [lineString[:(k-1)]]
        else:
            lineString = file.readline()
            while lineString.find("}") == -1:
                parameters += [lineString.lstrip("\t").rstrip(",")]
                lineString = file.readline()
        return parameters



    #Public methods
    def readAmiraImage(self,filename):
        self._filename = filename
        nDims = 0
        formatFile = ''
        version = ''
        parameters = []
        dataType = []

        #abrimos el archivo
        with open(filename, 'r') as file:
            lineString = self._findField(file,'AmiraMesh');
            #Encuentra el número de dimensiones
            k = lineString.find('2D ')
            if k != -1:
                nDims = 2
                lineString = lineString.lstrip("2D ")
            else:
                k = lineString.find("3D ")
                if k != -1:
                    nDims = 3
                    lineString = lineString.lstrip("3D ")
                else:
                    raise ValueError('Unexpected Data Type')

            #Encuentra el formato del archivo
            k = lineString.find('BINARY')
            if k != -1:
                formatFile = 'binary'
                lineString = lineString.lstrip('BINARY ')
            else:
                raise ValueError('Unexpected Data Type')

            version = lineString

            #Definiciones
            lineString = self._findField(file,'define')
            lineString = lineString.lstrip("Lattice ")
            sizes = lineString.split(" ")
            sizes[0] = int(sizes[0])
            sizes[1] = int(sizes[1])
            sizes[2] = int(sizes[2])

            #Parámetros
            parameters = self._findStruct(file, "Parameters")
            dataType = self._findStruct(file, "Lattice")

            temp = self._findField(file, "Data section")
            temp = file.readline()
            while temp.find("@1") == -1:
                temp = file.readline()

            pos = file.tell()
            file.seek(pos, os.SEEK_SET)

            NumToRead = sizes[0] * sizes[1] * sizes[2]
            pos=file.tell()
        #    A = fread(file, NumToRead, np.uint16)
        #    A = A.reshape((sizes[2], sizes[1], sizes[0]))
            A = np.fromfile(file, np.uint16, NumToRead).reshape((sizes[2], sizes[1], sizes[0])).transpose()



        #By now return just the first scan. THIS IS A BUG
        return A[:,:,1]


#             nRows=2;
#             nCols=sizes[2]/nRows;
#             for kk in range(1,sizes[2]+1):
# #                plt.subplot(nRows,int(nCols), kk);
# #                im = plt.imshow(np.rot90(A[:,:,kk-1], 3), aspect='auto', interpolation='none', origin='upper');
#                 plt.imsave('D:\Documentos\OCT\expedientes\\new\\scan'+str(kk)+'.png', np.rot90(A[:,:,kk-1], 3) , format ='png')
#
#             self.fileFolder = 'D:\\Documentos\\OCT\\expedientes\\new\\'

            #plt.title(gca,['Plane z=' num2str(kk)]);

#expediente = AmiraReader('D:\Documentos\OCT\git\src\code\OCT\MMH48_20170817_115332_3DOCT00_L_01.am')
#carpeta = expediente.carpeta
