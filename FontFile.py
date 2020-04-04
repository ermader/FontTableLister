'''
Created on Jan 26, 2020

@author: emader
'''
import struct

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


from NameTable import NameRecordFactory
from NameTable.NameRecord import NameRecord
from NameTable.MacintoshNameRecord import MacintoshNameRecord
from NameTable.WindowsNameRecord import WindowsNameRecord

class Font(object):
    '''
    classdocs
    '''
    FONT_DIRECTORY_HEADER_FORMAT = ">IHHHH"
    FONT_DIRECTORY_HEADER_LENGTH = struct.calcsize(FONT_DIRECTORY_HEADER_FORMAT)

    FONT_DIRECTORY_ENTRY_FORMAT = ">4sIII"
    FONT_DIRECTORY_ENTRY_LENGTH = struct.calcsize(FONT_DIRECTORY_ENTRY_FORMAT)

    def __init__(self, fontFile, fontOffset=0):
        fontFile.seek(fontOffset)
        directoryHeaderData = fontFile.read(self.FONT_DIRECTORY_HEADER_LENGTH)
        self.scalerType, self.numTables, self.searchRange, self.entrySelector, self.rangeShift = struct.unpack(
            self.FONT_DIRECTORY_HEADER_FORMAT, directoryHeaderData)

        self.tables = []
        rawDirectoryEntries = fontFile.read(self.FONT_DIRECTORY_ENTRY_LENGTH * self.numTables)

        entryStart = 0
        entryEnd = entryStart + self.FONT_DIRECTORY_ENTRY_LENGTH

        for _ in range(self.numTables):
            tagBytes, checksum, offset, length = struct.unpack(self.FONT_DIRECTORY_ENTRY_FORMAT, rawDirectoryEntries[entryStart:entryEnd])

            self.tables.append(TableFactory.tableFactory(fontFile, tagBytes, checksum, offset, length))

            entryStart = entryEnd
            entryEnd += self.FONT_DIRECTORY_ENTRY_LENGTH

    def getTable(self, tableTag):
        for table in self.tables:
            if table.tag == tableTag:
                return table

        return None

    def queryName(self, nameID):
        queries = [
            (NameRecordFactory.PLATFORM_ID_MACINTOSH, MacintoshNameRecord.LANGUAGE_ID_ENGLISH),
            (NameRecordFactory.PLATFORM_ID_WINDOWS, WindowsNameRecord.LANGUAGE_ID_ENGLISH_US),
            (NameRecordFactory.PLATFORM_ID_UNICODE, 0)
        ]

        nameTable = self.getTable('name')
        for (platformID, languageID) in queries:
            psName = nameTable.findName(platformID, nameID, languageID)
            if psName is not None:
                return psName

        return None

    def getPostscriptName(self):
        return self.queryName(NameRecord.NAME_ID_POSTSCRIPT_NAME)
