'''
Created on 21/11/2017

@author: Aleida
'''

class Study(object):
    '''
    classdocs
    '''


    def __init__(self, s = None, theCohort = None, theDesign = None, theObservations = [None] ):
        '''
        Constructor
        '''
        self.theCohort = theCohort
        self.theDesign = theDesign
        self.theObservations = theObservations
        
    def getCohort(self):
        return self.theCohort
    
    def setCohort(self, c):
        self.theCohort = c
        
    def getStudyDesign(self):
        return self.theDesign
    
    def setStudyDesign(self, sd):
        self.theDesign = sd
        
    def addObservation(self, o):
        self.theObservations.append(o)
        
    def removeObservation(self, ind):
        self.theObservations.remove(ind)
                    
    def getObservation(self, ind):
        return self.theObservations(ind)