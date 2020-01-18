'''
Created on Jan 17, 2020

@author: emader
'''

import struct

class File(object):
    
    def __init__(self, filePath):
        self.fonts = []
        self.fontFile = open(filePath, "rb")
        
        if filePath[-4:] == ".ttc":
            collection = Collection(self.fontFile, self.fonts)
        else:
            self.fonts.append(Font(self.fontFile))
        
class Collection(object):
    FONT_COLLECTION_HEADER_FORMAT = ">4sHHI"
    
    FONT_COLLECTION_HEADER_LENGTH = struct.calcsize(FONT_COLLECTION_HEADER_FORMAT)
    
    def __init__(self, fontFile, fontList):
        collectionHeaderData = fontFile.read(self.FONT_COLLECTION_HEADER_LENGTH)
        self.ttcTag, self.majorVersion, self.minorVersion, self.numFonts = struct.unpack(self.FONT_COLLECTION_HEADER_FORMAT, collectionHeaderData)
        
        offsetListFormat = ">%dI" % (self.numFonts)
        offsetListLength = struct.calcsize(offsetListFormat)
        offsetListData = fontFile.read(offsetListLength)
        offsetList = struct.unpack(offsetListFormat, offsetListData)
        
        for offset in offsetList:
            fontList.append(Font(fontFile, offset))
            
class Font(object):
    '''
    classdocs
    '''
    FONT_DIRECTORY_HEADER_FORMAT = ">IHHHH"

    FONT_DIRECTORY_HEADER_LENGTH = struct.calcsize(FONT_DIRECTORY_HEADER_FORMAT)


    def __init__(self, fontFile, fontOffset=0):
        fontFile.seek(fontOffset)
        directoryHeaderData = fontFile.read(self.FONT_DIRECTORY_HEADER_LENGTH)
        self.scalerType, self.numTables, self.searchRange, self.entrySelector, self.rangeShift = struct.unpack(self.FONT_DIRECTORY_HEADER_FORMAT, directoryHeaderData)

        self.tables = []
        for _ in range(self.numTables) :
            self.tables.append(Table(fontFile))
            
            
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
        return self.tag.decode("ascii")

