'''
Created on Feb 13, 2020

@author: emader
'''

import struct
import utility

import FontTable
from StandardGlyphNames import standardGlyphNames

# typedef struct {
#     Fixed version;
#     Fixed italicAngle;
#     FWord underlinePosition;
#     FWord underlineThickness;
#     UInt32 isFixedPitch;
#     UInt32 minMemType42;
#     UInt32 maxMemType42;
#     UInt32 minMemType1;
#     UInt32 maxMemType1;
# } FFLRawPostHeader;
#
# typedef struct {
#     UInt16 numGlyphs;
#     UInt16 glyphNameIndex[1]; // numGlyphs long
#     UInt8  names[1];          // numGlyph - 258 strings...
# } FFLRawPostStringTable;

class Table(FontTable.Table):
    POST_TABLE_HEADER_FORMAT = ">iihhIIIII"
    POST_TABLE_HEADER_LENGTH = struct.calcsize(POST_TABLE_HEADER_FORMAT)

    POST_STRING_TABLE_FORMAT = ">H"  # only numGlyphs...
    POST_STRING_TABLE_FORMAT_LENGTH = struct.calcsize(POST_STRING_TABLE_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        fixedVersion, fixedIitalicAngle, self.underlinePosition, self.underlineThickness, fixedPitch, \
        self.minMemType42, self.maxMemType42, self.minMemType1, self.maxMemType1 = \
            struct.unpack(self.POST_TABLE_HEADER_FORMAT, rawTable[:self.POST_TABLE_HEADER_LENGTH])

        self.version = utility.floatFromFixed(fixedVersion)
        self.italicAngle = utility.floatFromFixed(fixedIitalicAngle)
        self.isFixedPitch = fixedPitch != 0
        self.numGlyphs = None
        self.nameIndexTable = None
        self.names = None

        if self.version == 2.0:
            stringTableStart = self.POST_TABLE_HEADER_LENGTH
            stringTableEnd = stringTableStart + self.POST_STRING_TABLE_FORMAT_LENGTH
            self.numGlyphs, = struct.unpack(self.POST_STRING_TABLE_FORMAT, rawTable[stringTableStart:stringTableEnd])

            nameIndexTableFormat = f">{self.numGlyphs:d}H"
            nameIndexTableStart = stringTableEnd
            nameIndexTableLength = struct.calcsize(nameIndexTableFormat)
            nameIndexTableEnd = nameIndexTableStart + nameIndexTableLength

            self.nameIndexTable = struct.unpack(nameIndexTableFormat, rawTable[nameIndexTableStart:nameIndexTableEnd])

            self.names = []
            stringBytes = rawTable[nameIndexTableEnd:]
            byteIndex = 0
            while byteIndex < len(stringBytes):
                strLen = stringBytes[byteIndex]

                if strLen == 0:
                    break

                strStart = byteIndex + 1
                strEnd = strStart + strLen
                self.names.append(stringBytes[strStart:strEnd].decode("latin_1"))

                byteIndex = strEnd



    def getGlyphName(self, glyphID):
        standardGlyphCount = len(standardGlyphNames)

        if glyphID < standardGlyphCount:
            return standardGlyphNames[glyphID]

        return self.names[glyphID - standardGlyphCount]

    def format(self):
        FontTable.formatLine("Version", utility.formatFloat3(self.version))
        FontTable.formatLine("Italic Angle", utility.formatFloat3(self.italicAngle))
        FontTable.formatLine("Underline Position", utility.formatDecimal(self.underlinePosition))
        FontTable.formatLine("Underline Thickness", utility.formatDecimal(self.underlineThickness))
        FontTable.formatLine("isFixedPitch", f"{self.isFixedPitch}")
        FontTable.formatLine("Min Memory Type42", utility.formatDecimal(self.minMemType42))
        FontTable.formatLine("Max Memory Type42", utility.formatDecimal(self.maxMemType42))
        FontTable.formatLine("Min Memory Type1", utility.formatDecimal(self.minMemType1))
        FontTable.formatLine("Max Memory Type1", utility.formatDecimal(self.maxMemType1))

        if self.version == 2.0:
           for glyphID in range(0, self.numGlyphs):
                nameIndex = self.nameIndexTable[glyphID]
                print(f"      {glyphID:>6d} {nameIndex:>6d}    {self.getGlyphName(nameIndex)}")

        print()
