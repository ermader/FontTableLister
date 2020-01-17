'''
Created on Jan 17, 2020

@author: emader
'''

import struct

class Font(object):
    '''
    classdocs
    '''
    FONT_DIRECTORY_HEADER_FORMAT = ">IHHHH"

    FONT_DIRECTORY_HEADER_LENGTH = struct.calcsize(FONT_DIRECTORY_HEADER_FORMAT)


    def __init__(self, filePath):
        self.fontFile = open(filePath, "rb")
        #fileName = filePath.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string
        directoryHeaderData = self.fontFile.read(self.FONT_DIRECTORY_HEADER_LENGTH)
        self.scalerType, self.numTables, self.searchRange, self.entrySelector, self.rangeShift = struct.unpack(self.FONT_DIRECTORY_HEADER_FORMAT, directoryHeaderData)

        self.tables = []
        for _ in range(self.numTables) :
            self.tables.append(Table(self.fontFile))
            
            
class Table(object):
    '''
    classdocs
    '''
    FONT_DIRECTORY_ENTRY_FORMAT  = ">4sIII"
    FONT_DIRECTORY_ENTRY_LENGTH  = struct.calcsize(FONT_DIRECTORY_ENTRY_FORMAT)

    def __init__(self, fontFile):
        self.fontFile = fontFile
        
        directoryEntryData = fontFile.read(self.FONT_DIRECTORY_ENTRY_LENGTH)
        self.tag, self.checksum, self.offset, self.length = struct.unpack(self.FONT_DIRECTORY_ENTRY_FORMAT, directoryEntryData)

    def tag_string(self):
        # There's *got* to be a better way to do this...
        return "%c%c%c%c" % (self.tag[0], self.tag[1], self.tag[2], self.tag[3])

