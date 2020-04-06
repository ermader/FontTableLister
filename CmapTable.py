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

                    segCount = segCountX2 // 2
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

                    glyphIndexArrayStart = segmentArrayEnd
                    glyphIndexArrayEnd = encodingSubtableStart + subtableLength
                    glyphIndexArrayCount = (glyphIndexArrayEnd - glyphIndexArrayStart) // 2 # should really use the size of an "H"...
                    glyphIndexArrayFormat = f">{glyphIndexArrayCount}H"
                    glyphIndexArray = struct.unpack(glyphIndexArrayFormat, rawTable[glyphIndexArrayStart:glyphIndexArrayEnd])

                    for segment in range(segCount - 1): # we skip the last segment, which is for glyph 0xFFFF
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
                            glyphIDs.extend([(charCode + idDelta) & 0xFFFF for charCode in charCodeRange])
                        else:
                            for charCode in charCodeRange:
                                index = charCode - startCode + glyphIndexArrayIndex
                                glyphID = (glyphIndexArray[index] + idDelta) & 0xFFFF if glyphIndexArray[index] != 0 else 0
                                glyphIDs.append(glyphID)

                    z = list(zip(charCodes, glyphIDs))
                    self.charToGlyphMap = {c: g for (c, g) in z}
                    self.glyphToCharMap = {g: c for (c, g) in z}

                    break

            encodingRecordStart = encodingRecordEnd
            encodingRecordEnd += self.ENCODING_RECORD_LENGTH

