'''
Created on 22/11/2017

@author: Aleida
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, theExperimentalUnits = [None]):
        '''
        Constructor
        '''
        self.theExperimentalUnits = theExperimentalUnits
        
    def addExperimentalUnit(self, eu):
        self.theExperimentalUnits.append(eu)
        
    def removeExperimentalUnit(self, idEu):
        self.theExperimentalUnits.remove(idEu)
        
    def getExperimentalUnit(self, idEu):
        return self.theExperimentalUnits(idEu)
    
    def clear(self):
        self.theExperimentalUnits = [None]
        
    def getCohortSize(self):
        return len(self.theExperimentalUnits) 