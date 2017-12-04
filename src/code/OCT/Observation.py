'''
Created on 24/11/2017

@author: Aleida
'''

class Observation(object):
    '''
    classdocs
    '''


    def __init__(self, idO = None, acquisitionDate = None, theRawObservation = None):
        '''
        Constructor
        '''
        self.id = idO
        self.acquisitionDate = acquisitionDate
        self.theRawObservation = theRawObservation
        
        