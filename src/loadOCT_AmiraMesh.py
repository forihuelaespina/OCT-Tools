def loadOCT_AmiraMesh(filename)
#Loads an OCT file in Amira format
#
#
# A simple routine to read an AmiraMesh file
#that defines a scalar/vector field on a uniform grid.
#
# Follows the C code in https://people.mpi-inf.mpg.de/~weinkauf/notes/amiramesh.html
#
#
## Overview of the File Format
# Information obtained from: https://people.mpi-inf.mpg.de/~weinkauf/notes/amiramesh.html
#
# AmiraMesh is the native file format of Amira. The academic version 
#of Amira is developed by the Visualization and Data Analysis Group
#at Zuse Institute Berlin (https://amira.zib.de/download.html), but
#requires getting licences. 
#
# AmiraMesh is a very versatile file format for a large number
#of different data types.
# 
# An AmiraMesh file consists of a header and a data section. The header
#is always ASCII and contains the meta information such as grid type,
#bounding box, etc. The data section may be ASCII or binary. Here,
#we deal with binary data sections only. They are preceded by a
#line # Data section follows and another line @1.
# 
# <header, ASCII>
# # Data section follows
# @1
# <data section, binary>
#
#
### Header
#  The header of an AmiraMesh file looks as follows for a
#two-component vector field defined on a 3D uniform grid:
# 
# # AmiraMesh BINARY-LITTLE-ENDIAN 2.1 <== We have a binary (little-endian) data section.
# 
# define Lattice 4 6 8 <== Defines the uniform grid: number of grid points in x,y,z-direction.
# 
# Parameters {
#     #~ BoundingBox: xmin, xmax, ymin, ymax, zmin, zmax
#     BoundingBox -1 0 0 1 -0.5 0.5, <== Defines the bounding box of the uniform grid.
#     CoordType "uniform" <== We have a uniform grid.
# }
# 
# Lattice { float[2] Data } @1 <== The data section contains two floats for every grid point.
# 
# # Data section follows <== Precedes the data section.
# @1
# <binary data section>
# For a scalar field, the lattice specification reads: Lattice { float Data } @1.
# 
### Data Section
# 
# The binary data section is written with these specifications:
# 
# Little-endian format: This is the memory format of x86 processors
#and others. Hence, the data can be read into memory without any
#modifications on a PC or Intel-based Mac.
#
# x-fastest: To visit all grid points in the same order in
#which they are in memory, one writes three nested loops over
#the z,y,x-axes, where the loop over the x-axis is the innermost,
#and the loop over the z-axis the outermost.
#
# Interleaved components: The components u,v,w of a vector field
#are written interleaved, i.e., [u0, v0, w0], [u1, v1, w1], ...,
#where [u0, v0, w0] represents the first grid point, [u1, v1, w1]
#the second and so on.
#
#
#
#
## Parameters
#
# filename - The OCT data file to import in AmiraMesh format
#
#
# 
# Copyright 2017
# @date: 24-Sep-2017
# @author: Felipe Orihuela-Espina
# @date: 24-Sep-2017
#
# See also 
#



  ## Log
  #
  # 24-Sep-2017: FOE. Function created.



  # Open the data file for conversion
  fidr = fopen(filename, 'r')
  if fidr == -1
    error('OCT:import:UnableToReadFile',
          'Unable to read #s\n', filename)

  # h = waitbar(0,'Reading header...',
  #     'Name','Importing raw data (ETG-4000)')
  #fprintf('Importing raw data (ETG-4000) -> 0##')

  ## Reading the header ================================
  temp=findField(fidr,'AmiraMesh')
  #Parse the line with the defintion of data type
  idx = find(temp==' ')
  tmpToken=temp(idx(2)+1:idx(3)-1) #2D/3D
  switch(tmpToken)
    case '2D'
        theDataType.nDims = 2
    case '3D'
        theDataType.nDims = 3
    otherwise
        error('Unexpected data type.')

  tmpToken=temp(idx(3)+1:idx(4)-1)
  switch(tmpToken)
    case 'BINARY'
        theDataType.format = 'binary'
    otherwise
        error('Unexpected data type.')
  
  tmpToken=temp(idx(4)+1:end) #Data version 
  theDataType.version = tmpToken
  #theDataType

  # Read definitions
  temp=findDefinition(fidr,'Lattice')
  #Parse the line with the defintion of the lattice
  idx = find(temp==' ')
  #number of grid points in x,y,z-direction.
  gridSize.x = str2double(temp(idx(2)+1:idx(3)-1))
  gridSize.y = str2double(temp(idx(3)+1:idx(4)-1))
  gridSize.z = str2double(temp(idx(4)+1:end))
  #gridSize

  temp=findStruct(fidr,'Parameters')
  theParameters=parseStructParameters(temp)

  temp=findStruct(fidr,'Lattice') #Type of the field: scalar, vector
  theLattice=parseStructLattice(temp)



  #Sanity check
  xmin = theParameters.boundingBox(1)
  xmax = theParameters.boundingBox(2)
  ymin = theParameters.boundingBox(3)
  ymax = theParameters.boundingBox(4)
  zmin = theParameters.boundingBox(5)
  zmax = theParameters.boundingBox(6)
  if (gridSize.x <= 0 || gridSize.y <= 0 || gridSize.z <= 0 
        || xmin > xmax || ymin > ymax || zmin > zmax 
        || ~strcmpi(theParameters.coordType,'uniform') || theLattice.numDimensions <= 0)
        error('Something went wrong')
    
    
    
  #x=0.15
  #waitbar(x,h,'Reading Data - 15#')
  #fprintf('\b\b\b15##')

  ## Reading the Data ================================
  temp=findField(fidr,'Data section')
  #Consume the next line, which is "@1"
  temp=fgetl(fidr)

  #Read the data
  # - how much to read
  NumToRead = gridSize.x * gridSize.y * gridSize.z * theLattice.numDimensions
  # - do it
  ActRead = fread(fidr, NumToRead, 'uint16')
  #numel(ActRead)

  # - ok?
  if (NumToRead ~= numel(ActRead))
    error(['Something went wrong while reading the binary data section.',
            ' Premature end of file?'])


  #Reshape data
  pData = reshape(ActRead,[gridSize.x, gridSize.y, gridSize.z, theLattice.numDimensions])

  fclose(fidr)
  #waitbar(1,h)
  #close(h)
  #fprintf('\b\b\b100##\n')

  cmap=parula(64)

  #Test: print all z-planes
  figure
  nRows=2
  nCols=ceil(gridSize.z/nRows)
  for kk=1:gridSize.z
    subplot(nRows,nCols,kk)
    imagesc(pData(:,:,kk))
    title(gca,['Plane z=' num2str(kk)])
  
  # #...or alternatively
  # figure
  # montage(permute(pData,[1 2 4 3]),'DisplayRange',[])
  # colormap(cmap) #Watch out! Montage does not scale for colormap automatically

  opt.fontSize=11
  opt.outputfilesPrefix = 'OCTtest_Triton_0001'
  opt.destinationFolder='../Figures/'

  #Save the figure
  mySaveFig(gcf,[opt.destinationFolder opt.outputfilesPrefix])
  close gcf

# ##Display volume
# #https://www.mathworks.com/help/matlab/visualize/techniques-for-visualizing-scalar-volume-data.html
# 
# figure
# colormap(cmap)
# hiso = patch(isosurface(pData,5),
#    'FaceColor',[1,.75,.65],
#    'EdgeColor','none')
# #The isonormals function to renders the isosurface using vertex
# #normals obtained from the data, improving the quality of th
# #isosurface. The isosurface uses a single color to represent its
# #isovalue.
# isonormals(pData,hiso)
# #Use isocaps to calculate the data for another patch that is
# #displayed at the same isovalue (5) as the isosurface. Use the
# #data to show details of the interior. You can see this as the
# #sliced-away top of the head. The lower isocap is not visible
# #in the final view.
# hcap = patch(isocaps(pData,5),
#    'FaceColor','interp',
#    'EdgeColor','none')
# #Define the view and set the aspect ratio (view, axis, daspect).
# view(35,30) 
# axis tight 
# daspect([1,1,.4])
# #Add lighting and recalculate the surface normals based
# #on the gradient of the volume data, which produces smoother
# #lighting (camlight, lighting, isonormals). Increase the
# #AmbientStrength property of the isocap to brighten the coloring
# #without affecting the isosurface. Set the SpecularColorReflectance
# #of the isosurface to make the color of the specular reflected
# #light closer to the color of the isosurface; then set the
# #SpecularExponent to reduce the size of the specular spot.
# lightangle(45,30)
# lighting gouraud
# hcap.AmbientStrength = 0.6
# hiso.SpecularColorReflectance = 0
# hiso.SpecularExponent = 50

	return pData
# end of function loadOCT_AmiraMesh


## AUXILIARY FUNCTIONS

# def FindAndJump(buffer, searchString)
# # Find a string in the given buffer and return a pointer
# # to the contents directly behind the searchString.
# # If not found, return the buffer. A subsequent sscanf()
# # will fail then, but at least we return a decent pointer.
#     FoundLoc = strstr(buffer, searchString)
#     if (FoundLoc)   
#         res = FoundLoc + strlen(searchString)
#     else
#         res = buffer
#	return res
# end of function FindAndJump
#     

# def getFieldName(lineString)
# #Extract the field name
# idx=find(lineString==' ')
# if (isempty(idx))
#     fieldName=''
# else
#     fieldName=lineString(1:idx(1)-1)
#   return fieldName
# end of function getFieldName

def findField(fidr,fieldName)
  #Finds the line containing the field specified
  k=[]
  lineString=''
  while (ischar(lineString) and isempty(k))
        #Note: ischar(lineString) tests for end-of-file as indicated in
        #Matlab's help for the fgetl function and the help page on
        #"Testing for EOF with fgetl and fgets"
    lineString = fgetl(fidr)
    k=strfind(lineString,fieldName)
  return lineString
# end of function findField


def findDefinition(fidr,fieldName)
  #Finds the line containing the field specified
  k=[]
  lineString=''
  while (ischar(lineString) and isempty(k))
        #Note: ischar(lineString) tests for end-of-file as indicated in
        #Matlab's help for the fgetl function and the help page on
        #"Testing for EOF with fgetl and fgets"
    lineString = fgetl(fidr)
    if (~isempty(strfind(lineString,'define ')))
        k=strfind(lineString,fieldName)
  return lineString
# end of function findDefinition


def findStruct(fidr,fieldName)
  #Finds the line containing the specified struct
  #Once found, it seeks for the closing brace '}' in subsequente lines
  #until the end of the struct is found
  k=[]
  lineString=''
  while (ischar(lineString) and isempty(k))
        #Note: ischar(lineString) tests for end-of-file as indicated in
        #Matlab's help for the fgetl function and the help page on
        #"Testing for EOF with fgetl and fgets"
    lineString = fgetl(fidr)
    k=strfind(lineString,[fieldName ' {'])


  if ~isempty(k) #found
    #Now keep reading until the closing brace is found. Note that
    #it may be in the current line.
    k=strfind(lineString,'}')
    while (ischar(lineString) and isempty(k))
        lineString = [lineString fgetl(fidr)] #append the new line
        k=strfind(lineString,'}')
  
  return lineString  
# end of function findStruct
   

def parseStructParameters(lineString)
  #Parses the struct of parameters
  theParameters = struct('content',[],'boundingBox',[],'coordType',[])

  idx=[find(lineString=='{') find(lineString==',') find(lineString=='}')]
  #If any comma token splitter falls within quotes, then ignore
  idx2 = find(lineString=='"')
  while ~isempty(idx2)
    idxMin = idx2(1)
    idxMax = idx2(2)
    idx3=find(idx>idxMin and idx<idxMax)
    idx(idx3)=[]
    idx2(1:2) = []
  end
  lineString = lineString(idx(1)+1:end) #discard the first part (struct name)
  idx = idx(2:end)-idx(1) #adjust remaining indexes
   
  while ~isempty(idx)
    #parse next struct field
    tmpLine = lineString(1:idx(1)-1)
    #ignore preceding spaces
    while isspace(tmpLine(1))
	  tmpLine(1)=[] 

    idx2=find(tmpLine==' ')
    structFieldName = tmpLine(1:idx2(1)-1)
    structFieldData = tmpLine(idx2(1)+1:end)
    switch (lower(structFieldName))
        case 'content'
            theParameters.content = structFieldData
            theParameters.content(theParameters.content=='"')=[]
        case 'boundingbox'
            A= sscanf(structFieldData, '#g #g #g #g #g #g')
            theParameters.boundingBox = A
        case 'coordtype'
            theParameters.coordType = structFieldData
            theParameters.coordType(theParameters.coordType=='"')=[]
        otherwise
            error(['Unexpected field name "' structFieldName 
                    '" for struct Parameters.'])
    
    lineString = lineString(idx(1)+1:end) #discard the current field
    idx = idx(2:end)-idx(1) #adjust remaining indexes


  return theParameters
# end of function parseStructParameters







def parseStructLattice(lineString)
  #Parses the struct Lattice

  idx=[find(lineString=='{') find(lineString=='[') find(lineString==']') find(lineString=='}')]
  lineString = lineString(idx(1)+1:end) #discard the first part (struct name)
  idx = idx(2:end)-idx(1) #adjust remaining indexes
   
  while ~isempty(idx)
    #parse next struct field
    tmpLine = lineString(1:idx(1)-1)
    #ignore preceding spaces
    while isspace(tmpLine(1))
	  tmpLine(1)=[]

    idx2=[find(tmpLine=='[') find(tmpLine==' ')]
    theLattice.format = tmpLine(1:idx2(1)-1)
	theLattice.numDimensions = 1 #Scalar fields
    if tmpLine(idx2(1))=='['
        theLattice.numDimensions = tmpLine(idx2(1)+1:idx2(1)-1) #Vector fields
    
    lineString = lineString(idx(1)+1:end) #discard the current field
    idx = idx(2:end)-idx(1) #adjust remaining indexes


  return theLattice
# end of function parseStructLattice


