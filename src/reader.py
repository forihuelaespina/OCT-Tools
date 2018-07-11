9# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 20:43:28 2018

@author: Aleida
"""
import numpy as np
import matplotlib.pyplot as plt
import os    

def fread(fid, nelements, dtype):

    """Equivalent to Matlab fread function"""

    if dtype is np.str:
        dt = np.uint16  # WARNING: assuming 8-bit ASCII for np.str!
    else:
        dt = dtype
    data_array = np.fromfile(fid, dt, nelements)
    data_array.shape = (1,nelements)

    return data_array
 
def findField(file, fieldName):
    k = -1
    lineString = '';
    while isinstance(lineString, str) and k == -1:
        lineString = file.readline()
        k = lineString.find(fieldName)
    return lineString.lstrip("# "+fieldName+" ")

def findStruct(file, structName):
    lineString = findField(file, structName+" {")
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

class AmiraReader(object):
    def __init__(self, fn):
        self.filename = fn
        self.readAmira()
 
    def readAmira(self):
        filename = self.filename
        nDims = 0
        formatFile = ''
        version = ''
        parameters = []
        dataType = []
        
        #abrimos el archivo
        #filename = "D:\Documentos\OCT\git\src\code\OCT\MMH48_20170817_115332_3DOCT00_L_01.am"
        #filename = "D:\Documentos\OCT\git\src\code\OCT\SHC38_20171211_145008_3DOCT00_L_01.am"    
        with open(filename, 'r') as file:
            lineString = findField(file,'AmiraMesh');
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
            lineString = findField(file,'define')
            lineString = lineString.lstrip("Lattice ")
            sizes = lineString.split(" ")
            sizes[0] = int(sizes[0])
            sizes[1] = int(sizes[1])
            sizes[2] = int(sizes[2])
            
            #Parámetros
            parameters = findStruct(file, "Parameters")
            dataType = findStruct(file, "Lattice")
            
            temp = findField(file, "Data section")
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
            
            nRows=2;
            nCols=sizes[2]/nRows;
            for kk in range(1,sizes[2]+1):
#                plt.subplot(nRows,int(nCols), kk);
#                im = plt.imshow(np.rot90(A[:,:,kk-1], 3), aspect='auto', interpolation='none', origin='upper');
                plt.imsave('D:\Documentos\OCT\expedientes\\new\\scan'+str(kk)+'.png', np.rot90(A[:,:,kk-1], 3) , format ='png')
            
            self.carpeta = 'D:\\Documentos\\OCT\\expedientes\\new\\'
            
            #plt.title(gca,['Plane z=' num2str(kk)]);
        
#expediente = AmiraReader('D:\Documentos\OCT\git\src\code\OCT\MMH48_20170817_115332_3DOCT00_L_01.am')
#carpeta = expediente.carpeta
    
        
    