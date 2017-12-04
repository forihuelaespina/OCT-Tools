'''
Created on 22/11/2017

@author: Aleida
'''

class StudyDesign(object):
    '''
    classdocs
    '''


    def __init__(self, theVariables = [None], theTreatments = [None], theGroups = [None] ):
        '''
        Constructor
        '''
        self.theVariables = theVariables
        self.theTreatments = theTreatments
        self.theGroups = theGroups
        
    