'''
Created on 22/11/2017

@author: Aleida
'''
from jinja2 import idtracking

class Treatment(object):
    '''
    classdocs
    '''


    def __init__(self, idT = None, name = None, factorLevels = None):
        '''
        Constructor
        '''
        self.id = idT
        self.name = name
        self.factorLevels = factorLevels
        
    