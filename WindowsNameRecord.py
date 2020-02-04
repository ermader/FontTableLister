'''
Created on Feb 03, 2020

@author: emader
'''

import NameRecord

class WindowsNameRecord(NameRecord.NameRecord):
    def __init(self, platformID, encodingID, languageID, nameID, length, offset):
        NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset)

    def platformName(self):
        return "Windows"