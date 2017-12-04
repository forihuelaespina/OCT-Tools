'''
Created on 21/11/2017

@author: Aleida
'''

class Document (object):
    '''
    classdocs
    '''


    def __init__(self, doc = None, theStudy = None, lastModified = None, creationDate = None, theSettings = None):
        '''
        Constructor
        '''
        self.theStudy = theStudy
        self.lastModified = lastModified
        self.creationDate = creationDate
        self.theSettings = theSettings
        print('Documento creado')
        
    def getStudy(self):
        return self.theStudy
    
    def setStudy(self, s):
        self.theStudy = s
        
    def getModificationDate(self):
        return self.lastModified
    
    def setModificationDate(self, d):
        self.lastModified = d
        
    def getCreationDate(self):
        return self.creationDate
    
    def setCreationDate(self, d):
        self.creationDate = d

    def getSettings(self):
        return self.theSettings
    
    def setSettings(self, sl):
        self.theSettings = sl