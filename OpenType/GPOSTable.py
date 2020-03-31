'''
Created on Mar 31, 2020

@author: emader
'''

import struct

import FontTable
from OpenType import ScriptList


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

    def format(self):
        print(f"      Version: {self.majorVersion}.{self.minorVersion}")

        self.scriptList.format()
