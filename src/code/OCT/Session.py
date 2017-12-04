'''
Created on 22/11/2017

@author: Aleida
'''
from sphinx.versioning import add_uids

class Session(object):
    '''
    classdocs
    '''


    def __init__(self, idS = None, theUnit = None, theTreatment = None, theObservations = [None], theDate = None):
        '''
        Constructor
        '''
        self.id = idS
        self.theUnit =theUnit
        self.theTreatment = theTreatment
        self.theObservations = theObservations
        self.theDate = theDate
        
        