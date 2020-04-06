'''
Created on Mar 31, 2020

@author: emader
'''

import struct

import FontTable
from OpenType import ScriptList
from OpenType import FeatureList
from OpenType import LookupList

lookupTypes = {
    0: "(zero)",
    1: "Single Adjustment",
    2: "Pair Adjustment",
    3: "Cursive Attachment",
    4: "MarkToBase Attachment",
    5: "MarkToLigature Attachment",
    6: "MarkToMark Attachment",
    7: "Context Positioning",
    8: "Chaining Context Positioning",
    9: "Extension Positioning"
}

class Table(FontTable.Table):
    GPOS_TABLE_HEADER_FORMAT = ">HHHHH"
    GPOS_TABLE_HEADER_LENGTH = struct.calcsize(GPOS_TABLE_HEADER_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        # For now, we'll ignore version 1.1...
        (self.majorVersion, self.minorVersion, scriptListOffset, featureListOffset, lookupListOffset) = \
            struct.unpack(self.GPOS_TABLE_HEADER_FORMAT, rawTable[:self.GPOS_TABLE_HEADER_LENGTH])

        self.scriptList = ScriptList.ScriptListTable(rawTable, scriptListOffset)
        self.featureList = FeatureList.FeatureListTable(rawTable, featureListOffset)
        self.lookupList = LookupList.LookupListTable(rawTable, lookupListOffset)

    def format(self, parentFont):
        print(f"      Version: {self.majorVersion}.{self.minorVersion}")

        self.scriptList.format()
        self.featureList.format()
        self.lookupList.format(lookupTypes)
