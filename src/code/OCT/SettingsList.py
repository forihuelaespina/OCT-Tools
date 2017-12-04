'''
Created on 21/11/2017

@author: Aleida
'''

class SettingsList(object):
    '''
    classdocs
    '''


    def __init__(self, sl = None, currentSettings = [None], defaultSettings = [1]):
        self.currentSettings = currentSettings
        self.defaultSettings = defaultSettings
        
    def removeSetting(self, name):
        self.currentSettings.remove(name)
        
    def setSetting (self, name, value):
        self.currentSettings(name) = value
        
    def resetSettings(self, soft):
        self.currentSettings = self.defaultSettings