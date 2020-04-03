'''
Created on Apr 2, 2020

@author: emader
'''

import struct
import utility

import PostTable

class Table:
    CLASS_DEF_TABLE_FORMAT_FORMAT = ">H"
    CLASS_DEF_TABLE_FORMAT_LENGTH = struct.calcsize(CLASS_DEF_TABLE_FORMAT_FORMAT)

    CLASS_DEF_TABLE_HEADER_1_FORMAT = ">HHH"
    CLASS_DEF_TABLE_HEADER_1_LENGTH = struct.calcsize(CLASS_DEF_TABLE_HEADER_1_FORMAT)

    CLASS_DEF_TABLE_HEADER_2_FORMAT = ">HH"
    CLASS_DEF_TABLE_HEADER_2_LENGTH = struct.calcsize(CLASS_DEF_TABLE_HEADER_2_FORMAT)

    CLASS_RANGE_RECORD_FORMAT = ">HHH"
    CLASS_RANGE_RECORD_LENGTH = struct.calcsize(CLASS_RANGE_RECORD_FORMAT)

    def __init__(self, rawTable, classDefTableOffset):
        self.classTable = {}

        classTableHeaderStart = classDefTableOffset
        classTableHeaderEnd = classTableHeaderStart + self.CLASS_DEF_TABLE_FORMAT_LENGTH
        (tableFormat,) = struct.unpack(self.CLASS_DEF_TABLE_FORMAT_FORMAT, rawTable[classTableHeaderStart:classTableHeaderEnd])

        if tableFormat == 1:
            classTableHeaderEnd = classTableHeaderStart + self.CLASS_DEF_TABLE_HEADER_1_LENGTH
            (_, startGlyphID, glyphCount) = struct.unpack(self.CLASS_DEF_TABLE_HEADER_1_FORMAT, rawTable[classTableHeaderStart:classTableHeaderEnd])
            classValueArrayFormat = f">{glyphCount}H"
            classValueArrayLength = struct.calcsize(classValueArrayFormat)
            classValueArrayStart = self.CLASS_DEF_TABLE_HEADER_1_LENGTH
            classValueArrayEnd = classValueArrayStart + classValueArrayLength

            classValueArray = struct.unpack(classValueArrayFormat, rawTable[classValueArrayStart:classValueArrayEnd])

            for glyph in range(glyphCount):
                self.classTable[startGlyphID+glyph] = classValueArray[glyph]
        elif tableFormat == 2:
            classTableHeaderEnd = classTableHeaderStart + self.CLASS_DEF_TABLE_HEADER_2_LENGTH
            (_, classRangeCount) = struct.unpack(self.CLASS_DEF_TABLE_HEADER_2_FORMAT, rawTable[classTableHeaderStart:classTableHeaderEnd])

            classRangeRecordStart = classTableHeaderEnd
            classRangeRecordEnd = classRangeRecordStart + self.CLASS_RANGE_RECORD_LENGTH
            for _ in range(classRangeCount):
                (startGlyphID, endGlyphID, glyphClass) = struct.unpack(self.CLASS_RANGE_RECORD_FORMAT, rawTable[classRangeRecordStart:classRangeRecordEnd])

                for glyphID in range(startGlyphID, endGlyphID+1):
                    self.classTable[glyphID] = glyphClass

                classRangeRecordStart = classRangeRecordEnd
                classRangeRecordEnd += self.CLASS_RANGE_RECORD_LENGTH

    def format(self, classNames):
        for (glyphID, glyphClass) in self.classTable.items():
            glyphName = f"glyph{glyphID:05d}"
            className = classNames[glyphClass] if glyphClass in classNames else f"Class {glyphClass}"
            print(f"      {glyphName}: {className}")