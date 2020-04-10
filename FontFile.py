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

    requiredTables = ['cmap', 'head', 'hhea', 'hmtx', 'maxp', 'name', 'OS/2', 'post']

    def __init__(self, fontFile, fontOffset=0):
        fontFile.seek(fontOffset)
        directoryHeaderData = fontFile.read(self.FONT_DIRECTORY_HEADER_LENGTH)
        self.scalerType, self.numTables, self.searchRange, self.entrySelector, self.rangeShift = struct.unpack(
            self.FONT_DIRECTORY_HEADER_FORMAT, directoryHeaderData)

        self.tables = {}
        rawDirectoryEntries = fontFile.read(self.FONT_DIRECTORY_ENTRY_LENGTH * self.numTables)

        entryStart = 0
        entryEnd = entryStart + self.FONT_DIRECTORY_ENTRY_LENGTH

        for _ in range(self.numTables):
            tagBytes, checksum, offset, length = struct.unpack(self.FONT_DIRECTORY_ENTRY_FORMAT, rawDirectoryEntries[entryStart:entryEnd])

            table = TableFactory.tableFactory(fontFile, tagBytes, checksum, offset, length)
            self.tables[table.tag] = table

            entryStart = entryEnd
            entryEnd += self.FONT_DIRECTORY_ENTRY_LENGTH

    def getTable(self, tableTag):
        return self.tables[tableTag] if tableTag in self.tables else None

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

    def hasRequiredTables(self):
        for requiredTable in self.requiredTables:
            if requiredTable not in self.tables:
                return False

        return True

    def missingRequiredTables(self):
        missingTables = []

        for requiredTable in self.requiredTables:
            if requiredTable not in self.tables:
                missingTables.append(requiredTable)

        return missingTables

    def hasUnicodeMapping(self):
        cmapTable = self.getTable('cmap')
        return cmapTable.hasUnicodeMapping()

    def hasTrueTypeOutlines(self):
        return 'glyf' in self.tables and 'loca' in self.tables

    def hasCFFOutlines(self):
        return 'CFF ' in self.tables or 'CFF2' in self.tables

    def getGlyphName(self, glyphID):
        postTable = self.getTable('post')
        if postTable.version == 2.0:
            return postTable.getGlyphName(glyphID)
        else:
            charCode = self.getCharCode(glyphID)
            if charCode is not None:
                return f"uni{charCode:04X}"

            return f"gid{glyphID:05d}"

    def getGlyphID(self, charCode):
        cmapTable = self.getTable('cmap')
        return cmapTable.getGlyphID(charCode)

    def getCharCode(self, glyphID):
        cmapTable = self.getTable('cmap')
        return cmapTable.getCharCode(glyphID)