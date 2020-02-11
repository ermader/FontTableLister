'''
Created on Jan 26, 2020

@author: emader
'''
import struct

import utility
import TableFactory


class File(object):

    def __init__(self, file):
        self.fonts = []
        self.fontFile = file
        filePath = file.name

        if filePath.endswith(".ttc"):
            _ = Collection(self.fontFile, self.fonts)
        else:
            self.fonts.append(Font(self.fontFile))

    def getPostscriptNames(self):
        names = []

        for fontObject in self.fonts:
            names.append(fontObject.getPostscriptName())

        return names

    def fontWithPostscriptName(self, psname):
        for fontObject in self.fonts:
            if fontObject.getPostscriptName() == psname:
                return fontObject

        return None

class Collection(object):
    FONT_COLLECTION_HEADER_FORMAT = ">4sHHI"

    FONT_COLLECTION_HEADER_LENGTH = struct.calcsize(FONT_COLLECTION_HEADER_FORMAT)

    def __init__(self, fontFile, fontList):
        collectionHeaderData = fontFile.read(self.FONT_COLLECTION_HEADER_LENGTH)
        self.ttcTag, self.majorVersion, self.minorVersion, self.numFonts = struct.unpack(
            self.FONT_COLLECTION_HEADER_FORMAT, collectionHeaderData)

        offsetListFormat = f">{self.numFonts:d}I"
        offsetListLength = struct.calcsize(offsetListFormat)
        offsetListData = fontFile.read(offsetListLength)
        offsetList = struct.unpack(offsetListFormat, offsetListData)

        for offset in offsetList:
            fontList.append(Font(fontFile, offset))


import NameRecordFactory
from NameRecord import NameRecord
from MacintoshNameRecord import MacintoshNameRecord

class Font(object):
    '''
    classdocs
    '''
    FONT_DIRECTORY_HEADER_FORMAT = ">IHHHH"

    FONT_DIRECTORY_HEADER_LENGTH = struct.calcsize(FONT_DIRECTORY_HEADER_FORMAT)

    def __init__(self, fontFile, fontOffset=0):
        fontFile.seek(fontOffset)
        directoryHeaderData = fontFile.read(self.FONT_DIRECTORY_HEADER_LENGTH)
        self.scalerType, self.numTables, self.searchRange, self.entrySelector, self.rangeShift = struct.unpack(
            self.FONT_DIRECTORY_HEADER_FORMAT, directoryHeaderData)

        self.tables = []
        for _ in range(self.numTables):
            self.tables.append(TableFactory.tableFactory(fontFile))

    def getTable(self, tableTag):
        for table in self.tables:
            if table.tag == tableTag:
                return table

        return None

    def getPostscriptName(self):
        nameTable = self.getTable('name')
        return nameTable.findName(NameRecordFactory.PLATFORM_ID_MACINTOSH, NameRecord.NAME_ID_POSTSCRIPT_NAME, MacintoshNameRecord.LANGUAGE_ID_ENGLISH) # Hey! Need multiple queries...
