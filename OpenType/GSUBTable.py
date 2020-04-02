'''
Created on Mar 29, 2020

@author: emader
'''

import struct

import FontTable
from OpenType import ScriptList
from OpenType import FeatureList
from OpenType import LookupList

lookupTypes = {
    0: "(zero)",
    1: "Single",
    2: "Multiple",
    3: "Alternate",
    4: "Ligature",
    5: "Context",
    6: "Chaining Context",
    7: "Extension Substitution",
    8: "Reverse Chaining Context Single"
}

class Table(FontTable.Table):
    GSUB_TABLE_HEADER_FORMAT = ">HHHHH"
    GSUB_TABLE_HEADER_LENGTH = struct.calcsize(GSUB_TABLE_HEADER_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        # For now, we'll ignore version 1.1...
        (self.majorVersion, self.minorVersion, scriptListOffset, featureListOffset, lookupListOffset) = \
            struct.unpack(self.GSUB_TABLE_HEADER_FORMAT, rawTable[:self.GSUB_TABLE_HEADER_LENGTH])

        self.scriptList = ScriptList.ScriptListTable(rawTable, scriptListOffset)
        self.featureList = FeatureList.FeatureListTable(rawTable, featureListOffset)
        self.lookupList = LookupList.LookupListTable(rawTable, lookupListOffset)

    def format(self):
        print(f"      Version: {self.majorVersion}.{self.minorVersion}")

        self.scriptList.format()
        self.featureList.format()
        self.lookupList.format(lookupTypes)