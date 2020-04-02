'''
Created on Apr 1, 2020

@author: emader
'''

import struct
import utility

class LookupTable:
    LOOKUP_TABLE_FORMAT = ">HHH"
    LOOKUP_TABLE_LENGTH = struct.calcsize(LOOKUP_TABLE_FORMAT)

    def __init__(self, rawTable, lookupTableOffset):
        lookupTableStart = lookupTableOffset
        lookupTableEnd = lookupTableStart + self.LOOKUP_TABLE_LENGTH
        (self.lookupType, self.lookupFlags, self.subTableCount) = \
            struct.unpack(self.LOOKUP_TABLE_FORMAT, rawTable[lookupTableStart:lookupTableEnd])

    def format(self, lookupTypes, lookupIndex):
        lookupTypeName = lookupTypes[self.lookupType] if self.lookupType in lookupTypes else f"LookupType{self.lookupType}"

        print(f"      Lookup{lookupIndex:02d}: {lookupTypeName}")
        print(f"        lookupFlags: {utility.formatHex16(self.lookupFlags)}")
        print(f"        subTableCount: {self.subTableCount:d}")
        print()

class LookupListTable:
    LOOKUP_LIST_TABLE_FORMAT = ">H"
    LOOKUP_LIST_TABLE_LENGTH = struct.calcsize(LOOKUP_LIST_TABLE_FORMAT)

    def __init__(self, rawTable, lookupListOffset):
        lookupListEnd = lookupListOffset + self.LOOKUP_LIST_TABLE_LENGTH
        (lookupCount,) = struct.unpack(self.LOOKUP_LIST_TABLE_FORMAT, rawTable[lookupListOffset:lookupListEnd])

        lookupOffsetsListFormat = f">{lookupCount:d}H"
        lookupOffsetsListLength = struct.calcsize(lookupOffsetsListFormat)
        lookupOffsetsListStart = lookupListEnd
        lookupOffsetsListEnd = lookupOffsetsListStart + lookupOffsetsListLength
        lookupOffsetsList = struct.unpack(lookupOffsetsListFormat, rawTable[lookupOffsetsListStart:lookupOffsetsListEnd])

        self.lookupTables = []
        for offset in lookupOffsetsList:
            self.lookupTables.append(LookupTable(rawTable, lookupListOffset+offset))

    def format(self, lookupTypes):
        lookupIndex = 0
        for lookupTable in self.lookupTables:
            lookupTable.format(lookupTypes, lookupIndex)
            lookupIndex += 1