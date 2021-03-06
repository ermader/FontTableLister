'''
Created on Apr 4, 2020

@author: emader
'''

import struct
import utility

from PlatformAndEncoding import PLATFORM_ID_UNICODE, PLATFORM_ID_MACINTOSH, PLATFORM_ID_WINDOWS,\
     UnicodePlatform, MacintoshPlatform, WindowsPlatform, getPLatformName, getEncodingName

import FontTable

class EncodingRecord:
    ENCODING_SUBTABLE_FORMAT = ">H" # only the format
    ENCODING_SUBTABLE_LENGTH = struct.calcsize(ENCODING_SUBTABLE_FORMAT)

    formatNames = {
        0: "Byte encoding table (0)",
        2: "High-byte mapping through table (2)",
        4: "Segment mapping to delta values (4)",
        6: "Trimmed table mapping (6)",
        8: "Mixed 16-bit and 32-bit coverage (8)",
        10: "Trimmed mapping (10)",
        12: "Segmented coverage (12)",
        13: "Many-to-one range mappings (13)",
        14: "Unicode variation sequences (14)"
    }

    def getFormatName(self):
        if self.subtableFormat in self.formatNames:
            return self.formatNames[self.subtableFormat]

        return f"Format {self.subtableFormat}"

    def readSubtableFormat0(self, rawTable, subtableStart):
        ENCODING_SUBTABLE_0_FORMAT = ">HHH"
        ENCODING_SUBTABLE_0_LENGTH = struct.calcsize(ENCODING_SUBTABLE_0_FORMAT)
        subtableEnd = subtableStart + ENCODING_SUBTABLE_0_LENGTH

        (_, subtableLength, subtableLanguage) = struct.unpack(ENCODING_SUBTABLE_0_FORMAT, rawTable[subtableStart:subtableEnd])

        glyphIDArrayStart = subtableEnd
        glyhCount = 256 # this table maps all single byte character codes
        glyphIDArrayFormat = f">{glyhCount}B"
        glyphIDArrayEnd = glyphIDArrayStart + struct.calcsize(glyphIDArrayFormat)

        charCodes = [charCode for charCode in range(256)]
        glyphCodes = struct.unpack(glyphIDArrayFormat, rawTable[glyphIDArrayStart:glyphIDArrayEnd])

        return (charCodes, glyphCodes)

    def readSubtableFormat4(self, rawTable, subtableStart):
        ENCODING_SUBTABLE_4_FORMAT = ">HHHHHHH"
        ENCODING_SUBTABLE_4_LENGTH = struct.calcsize(ENCODING_SUBTABLE_4_FORMAT)
        subtableEnd = subtableStart + ENCODING_SUBTABLE_4_LENGTH

        (_, subtableLength, subtableLanguage, segCountX2, searchRange, entrySelector, rangeShift) = \
                        struct.unpack(ENCODING_SUBTABLE_4_FORMAT, rawTable[subtableStart:subtableEnd])

        charCodes = []
        glyphCodes = []

        segCount = segCountX2 // 2
        segmentArrayUnsignedFormat = f">{segCount}H"
        segmentArraySignedFormat = f">{segCount}h"
        segmentArrayLength = struct.calcsize(segmentArrayUnsignedFormat)
        segmentArrayStart = subtableEnd
        segmentArrayEnd = segmentArrayStart + segmentArrayLength

        endCodes = struct.unpack(segmentArrayUnsignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

        segmentArrayStart = segmentArrayEnd + struct.calcsize(">H")  # reservedPad
        segmentArrayEnd = segmentArrayStart + segmentArrayLength
        startCodes = struct.unpack(segmentArrayUnsignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

        segmentArrayStart = segmentArrayEnd
        segmentArrayEnd = segmentArrayStart + segmentArrayLength
        idDeltas = struct.unpack(segmentArraySignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

        segmentArrayStart = segmentArrayEnd
        segmentArrayEnd = segmentArrayStart + segmentArrayLength
        idRangeOffsets = struct.unpack(segmentArrayUnsignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

        glyphIndexArrayStart = segmentArrayEnd
        glyphIndexArrayEnd = subtableStart + subtableLength
        glyphIndexArrayCount = (
                                           glyphIndexArrayEnd - glyphIndexArrayStart) // 2  # should really use the size of an "H"...
        glyphIndexArrayFormat = f">{glyphIndexArrayCount}H"
        glyphIndexArray = struct.unpack(glyphIndexArrayFormat, rawTable[glyphIndexArrayStart:glyphIndexArrayEnd])

        for segment in range(segCount - 1):  # we skip the last segment, which is for glyph 0xFFFF
            startCode = startCodes[segment]
            endCode = endCodes[segment]
            idDelta = idDeltas[segment]
            idRangeOffset = idRangeOffsets[segment]

            # idRangeOffset[i], if not zero, is the byte offset from idRangeOffset[i] to the
            # corresponding entry into glyphIndexArray. The spec. gives this expression to
            # retrieve that entry:
            # glyphIndex = *( &idRangeOffset[i] + idRangeOffset[i] / 2 + (charCode - startCode[i]) )
            # So: idRangeOffset // 2 is the number of words from idRangeOffset[i] to the entry
            # in glyphIndexArray, so the index is idRangeOffset // 2 - segCount + i
            glyphIndexArrayIndex = idRangeOffset // 2 - segCount + segment

            charCodeRange = range(startCode, endCode + 1)
            charCodes.extend(charCodeRange)

            if idRangeOffset == 0:
                glyphCodes.extend([(charCode + idDelta) & 0xFFFF for charCode in charCodeRange])
            else:
                for charCode in charCodeRange:
                    index = glyphIndexArrayIndex + charCode - startCode
                    glyphID = (glyphIndexArray[index] + idDelta) & 0xFFFF if glyphIndexArray[index] != 0 else 0
                    glyphCodes.append(glyphID)

        return (charCodes, glyphCodes)

    def readSubtableFormat6(self, rawTable, subtableStart):
        ENCODING_SUBTABLE_6_FORMAT = ">HHHHH"
        ENCODING_SUBTABLE_6_LENGTH = struct.calcsize(ENCODING_SUBTABLE_6_FORMAT)
        subtableEnd = subtableStart + ENCODING_SUBTABLE_6_LENGTH

        (_, subtableLength, subtableLanguage, firstCode, entryCount) = struct.unpack(ENCODING_SUBTABLE_6_FORMAT, rawTable[subtableStart:subtableEnd])

        glyphIDArrayFormat = f">{entryCount}H"
        glyphIDArrayLength = struct.calcsize(glyphIDArrayFormat)
        glyphIDArrayStart = subtableEnd
        glyphIDArrayEnd = glyphIDArrayStart + glyphIDArrayLength

        charCodes = [charCode for charCode in range(firstCode, firstCode+entryCount)]
        glyphCodes = struct.unpack(glyphIDArrayFormat, rawTable[glyphIDArrayStart:glyphIDArrayEnd])

        return (charCodes, glyphCodes)

    def readSubtableFormat12(self, rawTable, subtableStart):
        ENCODING_SUBTABLE_12_FORMAT = ">HHIII"
        ENCODING_SUBTABLE_12_LENGTH = struct.calcsize(ENCODING_SUBTABLE_12_FORMAT);

        MAP_GROUP_RECORD_FORMAT = ">III"
        MAP_GROUP_RECORD_LENGTH = struct.calcsize(MAP_GROUP_RECORD_FORMAT)

        charCodes = []
        glyphCodes = []
        subtableEnd = subtableStart + ENCODING_SUBTABLE_12_LENGTH

        (_, _, subtableLength, subtableLanguage, numGroups) = struct.unpack(ENCODING_SUBTABLE_12_FORMAT, rawTable[subtableStart:subtableEnd])

        mapGroupStart = subtableEnd
        mapGroupEnd = mapGroupStart + MAP_GROUP_RECORD_LENGTH
        for _ in range(numGroups):
            (startCharCode, endCharCode, startGlyphID) = struct.unpack(MAP_GROUP_RECORD_FORMAT, rawTable[mapGroupStart:mapGroupEnd])

            charCodeRange = range(startCharCode, endCharCode + 1)
            charCodes.extend(charCodeRange)
            gids = [startGlyphID + char - startCharCode for char in charCodeRange]
            glyphCodes.extend([startGlyphID + char - startCharCode for char in charCodeRange])
            mapGroupStart = mapGroupEnd
            mapGroupEnd += MAP_GROUP_RECORD_LENGTH

        return (charCodes, glyphCodes)

    def __init__(self, rawTable, platformID, encodingID, offset32, offsetToSubtableMap):
        self.platformID = platformID
        self.encodingID = encodingID
        self.offset32 = offset32

        encodingSubtableStart = offset32
        encodingSubtableEnd = encodingSubtableStart + self.ENCODING_SUBTABLE_LENGTH

        (self.subtableFormat, ) = struct.unpack(self.ENCODING_SUBTABLE_FORMAT,  rawTable[encodingSubtableStart:encodingSubtableEnd])
        if self.offset32 not in offsetToSubtableMap:
            charCodes = []
            glyphCodes = []

            if self.subtableFormat == 0:
                (charCodes, glyphCodes) = self.readSubtableFormat0(rawTable, encodingSubtableStart)
            elif self.subtableFormat == 4: # want symbolic constants for these?
                (charCodes, glyphCodes) = self.readSubtableFormat4(rawTable, encodingSubtableStart)
            elif self.subtableFormat == 6:
                (charCodes, glyphCodes) = self.readSubtableFormat6(rawTable, encodingSubtableStart)
            elif self.subtableFormat == 12:
                (charCodes, glyphCodes) = self.readSubtableFormat12(rawTable, encodingSubtableStart)

            z = list(zip(charCodes, glyphCodes))
            offsetToSubtableMap[offset32] = ({c: g for (c, g) in z}, {g: c for (c, g) in z})



class Table(FontTable.Table):
    preferredMappings = [
        (PLATFORM_ID_UNICODE, UnicodePlatform.ENCODING_ID_UNICODE_FULL),
        (PLATFORM_ID_WINDOWS, WindowsPlatform.ENCODING_ID_UNICODE_UCS4),
        (PLATFORM_ID_UNICODE, UnicodePlatform.ENCODING_ID_UNICODE_2_0_FULL),
        (PLATFORM_ID_UNICODE, -1),  # Any encoding will do...
        (PLATFORM_ID_WINDOWS, WindowsPlatform.ENCODING_ID_UNICODE_BMP)
    ]
    preferredMappingCount = len(preferredMappings)
    bestMapping = preferredMappingCount
    bestEncodingRecord = None

    CMAP_HEADER_FORMAT = ">HH"
    CMAP_HEADER_LENGTH = struct.calcsize(CMAP_HEADER_FORMAT)

    ENCODING_RECORD_FORMAT = ">HHI"
    ENCODING_RECORD_LENGTH = struct.calcsize(ENCODING_RECORD_FORMAT)

    def rankMapping(self, encodingRecord):
        platformID = encodingRecord.platformID
        encodingID = encodingRecord.encodingID

        for mapping in range(self.preferredMappingCount):
            (preferredPlatformID, preferredEncodingID) = self.preferredMappings[mapping]
            if preferredPlatformID == platformID and (preferredEncodingID == encodingID or preferredEncodingID == -1):
                if mapping < self.bestMapping:
                    self.bestMapping = mapping
                    self.bestEncodingRecord = encodingRecord

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        self.encodingRecords = []
        self.offsetToSubtableMap = {}

        (version, numTables) = struct.unpack(self.CMAP_HEADER_FORMAT, rawTable[:self.CMAP_HEADER_LENGTH])

        encodingRecordStart = self.CMAP_HEADER_LENGTH
        encodingRecordEnd = encodingRecordStart + self.ENCODING_RECORD_LENGTH

        for _ in range(numTables):
            (platformID, encodingID, offset32) = struct.unpack(self.ENCODING_RECORD_FORMAT, rawTable[encodingRecordStart:encodingRecordEnd])

            encodingRecord = EncodingRecord(rawTable, platformID, encodingID, offset32, self.offsetToSubtableMap)
            self.encodingRecords.append(encodingRecord)

            self.rankMapping(encodingRecord)

            encodingRecordStart = encodingRecordEnd
            encodingRecordEnd += self.ENCODING_RECORD_LENGTH

        if self.bestEncodingRecord is not None:
            (self.charToGlyphMap, self.glyphToCharMap) = self.offsetToSubtableMap[self.bestEncodingRecord.offset32]

    def hasUnicodeMapping(self):
        return self.bestEncodingRecord is not None

    def getCharCode(self, glyphID):
        if glyphID in self.glyphToCharMap:
            return self.glyphToCharMap[glyphID]

        return None

    def getGlyphID(self, charCode):
        if charCode in self.charToGlyphMap:
            return self.charToGlyphMap[charCode]

        return None

    def format(self, parentFont):
        for encodingRecord in self.encodingRecords:
            platformID = encodingRecord.platformID
            encodingID = encodingRecord.encodingID
            offset32 = encodingRecord.offset32
            formatName = encodingRecord.getFormatName()

            print(f"      {getPLatformName(platformID):10} {getEncodingName(platformID, encodingID):15} {utility.formatHex32(offset32):12} {formatName}")