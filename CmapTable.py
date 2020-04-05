'''
Created on Apr 4, 2020

@author: emader
'''

import struct
import utility

from PlatformAndEncoding import PLATFORM_ID_UNICODE, PLATFORM_ID_MACINTOSH, PLATFORM_ID_WINDOWS, UnicodePlatform, MacintoshPlatform, WindowsPlatform

import FontTable

class Table(FontTable.Table):
    CMAP_HEADER_FORMAT = ">HH"
    CMAP_HEADER_LENGTH = struct.calcsize(CMAP_HEADER_FORMAT)

    ENCODING_RECORD_FORMAT = ">HHI"
    ENCODING_RECORD_LENGTH = struct.calcsize(ENCODING_RECORD_FORMAT)

    ENCODING_SUBTABLE_FORMAT = ">HHH"
    ENCODING_SUBTABLE_LENGTH = struct.calcsize(ENCODING_SUBTABLE_FORMAT)

    ENCODING_SUBTABLE_4_FORMAT = ">HHHHHHH"
    ENCODING_SUBTABLE_4_LENGTH = struct.calcsize(ENCODING_SUBTABLE_4_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        self.charToGlyphMap = {}
        self.glyphToCharMap = {}

        (version, numTables) = struct.unpack(self.CMAP_HEADER_FORMAT, rawTable[:self.CMAP_HEADER_LENGTH])

        encodingRecordStart = self.CMAP_HEADER_LENGTH
        encodingRecordEnd = encodingRecordStart + self.ENCODING_RECORD_LENGTH
        for _ in range(numTables):
            (platformID, encodingID, offset32) = struct.unpack(self.ENCODING_RECORD_FORMAT, rawTable[encodingRecordStart:encodingRecordEnd])

            if platformID == PLATFORM_ID_UNICODE or (platformID == PLATFORM_ID_WINDOWS and encodingID == WindowsPlatform.ENCODING_ID_UNICODE_BMP):
                encodingSubtableStart = offset32
                encodingSubtableEnd = encodingSubtableStart + self.ENCODING_SUBTABLE_LENGTH

                (subtableFormat, subtableLength, subtableLanguage) = struct.unpack(self.ENCODING_SUBTABLE_FORMAT, rawTable[encodingSubtableStart:encodingSubtableEnd])

                if subtableFormat == 4:
                    charCodes = []
                    glyphIDs = []
                    encodingSubtableEnd = encodingSubtableStart + self.ENCODING_SUBTABLE_4_LENGTH

                    (_, _, _, segCountX2, searchRange, entrySelector, rangeShift) = \
                        struct.unpack(self.ENCODING_SUBTABLE_4_FORMAT, rawTable[encodingSubtableStart:encodingSubtableEnd])

                    segCount = int(segCountX2 / 2)
                    segmentArrayUnsignedFormat = f">{segCount}H"
                    segmentArraySignedFormat = f">{segCount}h"
                    segmentArrayLength = struct.calcsize(segmentArrayUnsignedFormat)
                    segmentArrayStart = encodingSubtableEnd
                    segmentArrayEnd = segmentArrayStart + segmentArrayLength

                    endCodes = struct.unpack(segmentArrayUnsignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

                    segmentArrayStart = segmentArrayEnd + struct.calcsize(">H") # reservedPad
                    segmentArrayEnd = segmentArrayStart + segmentArrayLength
                    startCodes = struct.unpack(segmentArrayUnsignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

                    segmentArrayStart = segmentArrayEnd
                    segmentArrayEnd = segmentArrayStart + segmentArrayLength
                    idDeltas = struct.unpack(segmentArraySignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

                    segmentArrayStart = segmentArrayEnd
                    segmentArrayEnd = segmentArrayStart + segmentArrayLength
                    idRangeOffsets = struct.unpack(segmentArrayUnsignedFormat, rawTable[segmentArrayStart:segmentArrayEnd])

                    glyphIDArrayStart = segmentArrayEnd
                    glyphIDArrayEnd = encodingSubtableStart + subtableLength
                    glyphIDArrayCount = int((glyphIDArrayEnd - glyphIDArrayStart) / 2) # should really use the size of an "H"...
                    glyphIDArrayFormat = f">{glyphIDArrayCount}H"
                    glyphIDArray = struct.unpack(glyphIDArrayFormat, rawTable[glyphIDArrayStart:glyphIDArrayEnd])

                    for segment in range(segCount -1):
                        startCode = startCodes[segment]
                        endCode = endCodes[segment]
                        idDelta = idDeltas[segment]
                        idRangeOffset = idRangeOffsets[segment]

                        # this is because of the indexing magic built into format 4...
                        magic = idRangeOffset // 2 - startCode + segment - segCount

                        charCodeRange = range(startCode, endCode + 1)
                        charCodes.extend(charCodeRange)

                        if idRangeOffset == 0:
                            glyphIDs.extend([(charCode + idDelta) & 0xFFFF for charCode in charCodeRange])
                        else:
                            for charCode in charCodeRange:
                                index = charCode + magic
                                glyphID = (glyphIDArray[index] + idDelta) & 0xFFFF if glyphIDArray[index] != 0 else 0
                                glyphIDs.append(glyphID)

                    z = list(zip(charCodes, glyphIDs))
                    self.charToGlyphMap = {c: g for (c, g) in z}
                    self.glyphToCharMap = {g: c for (c, g) in z}

                    break

            encodingRecordStart = encodingRecordEnd
            encodingRecordEnd += self.ENCODING_RECORD_LENGTH

