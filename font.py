'''
Created on Jan 17, 2020

@author: emader
'''

import struct
import math
#
# A bunch of these should probably be in a utility module
#
from datetime import datetime, timedelta, tzinfo, timezone

ldtBase = datetime(1904, 1, 1, tzinfo=timezone.utc)

def formatLongDateTime(ldt):
    dateTime = ldtBase + timedelta(seconds=ldt)
    return dateTime.strftime("%A, %B %_d %Y %I:%M:%S %p %Z")

def formatHex16(value):
    return "0x{:04X}".format(value)

def formatHex32(value):
    return "0x{:08X}".format(value)

def formatDecimal(value):
    return "{:d}".format(value)

def formatFixed(fixed):
    return "{:.3f}".format(floatFromFixed(fixed))

def swapLongDateTime(highWord, lowWord):
    return (highWord << 32) | lowWord

def floatFromFixed(fixed):
    quotient = fixed / 65536.0
    integerPart = math.floor(quotient)
    fractionPart = quotient - integerPart
    
    return integerPart + fractionPart

def roundAndDivide(value, dividend):
    return int((value + dividend - 1) / dividend)

class File(object):
    
    def __init__(self, filePath):
        self.fonts = []
        self.fontFile = open(filePath, "rb")
        
        if filePath[-4:] == ".ttc":
            _ = Collection(self.fontFile, self.fonts)
        else:
            self.fonts.append(Font(self.fontFile))
        
class Collection(object):
    FONT_COLLECTION_HEADER_FORMAT = ">4sHHI"
    
    FONT_COLLECTION_HEADER_LENGTH = struct.calcsize(FONT_COLLECTION_HEADER_FORMAT)
    
    def __init__(self, fontFile, fontList):
        collectionHeaderData = fontFile.read(self.FONT_COLLECTION_HEADER_LENGTH)
        self.ttcTag, self.majorVersion, self.minorVersion, self.numFonts = struct.unpack(self.FONT_COLLECTION_HEADER_FORMAT, collectionHeaderData)
        
        offsetListFormat = ">{:d}I".format(self.numFonts)
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
            self.tables.append(Table.factory(fontFile))
            
            
class Table(object):
    '''
    classdocs
    '''
    FONT_DIRECTORY_ENTRY_FORMAT  = ">4sIII"
    FONT_DIRECTORY_ENTRY_LENGTH  = struct.calcsize(FONT_DIRECTORY_ENTRY_FORMAT)

    rawBytes = None
    
    BYTES_PER_WORD = struct.calcsize(">H")
    WORDS_PER_LINE = 16
    BYTES_PER_LINE = BYTES_PER_WORD * WORDS_PER_LINE
    
    @staticmethod
    def factory(fontFile):
        directoryEntryData = fontFile.read(Table.FONT_DIRECTORY_ENTRY_LENGTH)
        tagBytes, checksum, offset, length = struct.unpack(Table.FONT_DIRECTORY_ENTRY_FORMAT, directoryEntryData)
        
        if tagBytes == b'head':
            return HeadTable(fontFile, tagBytes, checksum, offset, length)
        else:
            return Table(fontFile, tagBytes, checksum, offset, length)
        
    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        self.fontFile = fontFile
        self.tag = tagBytes.decode("ascii")
        self.checksum = checksum
        self.offset = offset
        self.length = length

    def rawData(self):
        if self.rawBytes == None:
            self.fontFile.seek(self.offset)
            self.rawBytes = self.fontFile.read(self.length)
            return self.rawBytes

    def dump(self):
        tableData = self.rawData()
        wordsToDump = roundAndDivide(self.length, self.BYTES_PER_WORD)
        linesToDump = roundAndDivide(wordsToDump, self.WORDS_PER_LINE)
        rawWordsFormat = ">{:d}H".format(wordsToDump)
        rawWords = struct.unpack(rawWordsFormat, tableData)
        
        lineOffset = 0
        for line in range(linesToDump):
            print("      {:s}".format(formatHex32(lineOffset)), end=":")
            
            wordsPerLine = min(self.WORDS_PER_LINE, wordsToDump - (lineOffset >> 1))
            for word in range(wordsPerLine):
                print(" {:s}".format(formatHex16(rawWords[(lineOffset >> 1) + word])), end="")
            
            lineOffset += self.BYTES_PER_LINE
            print()
        print()
     
    def format(self):
        print("      Don't know how to format a '{:s}' table.".format(self.tag))
        print()
            
# typedef struct {
#     Fixed version;              // 00
#     Fixed fontRevision;         // 04
#     UInt32 checksumAdjustment;  // 08
#     UInt32 magicNumber;         // 12
#     UInt16 flags;               // 16
#     UInt16 unitsPerEm;          // 18
# //  LongDateTime creationDate;  // 20
#     UInt32 creationDate0;       // Need to split as two UInt32s because it's not on an 8 byte boundary (really?)
#     UInt32 creationDate1;
# //  LongDateTime modifiedDate;  // 28
#     UInt32 modifiedDate0;
#     UInt32 modifiedDate1;
#     FWord xMin;                 // 36
#     FWord yMin;                 // 38
#     FWord xMax;                 // 40
#     FWord yMax;                 // 42
#     UInt16 macStyle;            // 44
#     UInt16 lowestRecPPEM;       // 46
#     SInt16 fontDirectionHint;   // 48
#     SInt16 indexToLocFormat;    // 50
#     SInt16 glyphDataFormat;     // 52
#                                 // 54
#     
# } FFLRawHeadTable;

def formatLine(label, value):
    print("      {:<25s}{:>40s}".format(label + ":", value))
            
class HeadTable(Table):
    HEAD_TABLE_FORMAT = ">iiIIHHIIIIhhhhHHhhh"
    HEAD_TABLE_LENGTH = struct.calcsize(HEAD_TABLE_FORMAT)
    
    def format(self):
        rawTable = self.rawData()
        version, revision, adjust, magic, flags, upm, cd0, cd1, md0, md1, xMin, yMin, xMax, yMax, style, lowPPEM, dirHint, ilocFormat, gdFormat = struct.unpack(self.HEAD_TABLE_FORMAT, rawTable)
        creationDate = swapLongDateTime(cd0, cd1)
        modDate = swapLongDateTime(md0, md1)
        formatLine("Version", formatFixed(version))
        formatLine("Font Revision", formatFixed(revision))
        formatLine("Checksum Adjustment", formatHex32(adjust))
        formatLine("Magic Number", formatHex32(magic))
        formatLine("Flags", formatHex16(flags))
        formatLine("Units Per EM", formatDecimal(upm))
        formatLine("Creation Date", formatLongDateTime(creationDate))
        formatLine("Modification Date", formatLongDateTime(modDate))
        formatLine("xMin", formatDecimal(xMin))
        formatLine("yMin", formatDecimal(yMin))
        formatLine("xMax", formatDecimal(xMax))
        formatLine("yMax", formatDecimal(yMax))
        formatLine("Mac Style", formatHex16(style))
        formatLine("Lowest Rec PPEM", formatDecimal(lowPPEM))
        formatLine("Font Direction Hint", formatDecimal(dirHint))
        formatLine("Index to Loc Format", formatDecimal(ilocFormat))
        formatLine("Glyh Data Format", formatDecimal(gdFormat))
        print()
    