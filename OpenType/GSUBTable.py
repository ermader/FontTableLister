'''
Created on Mar 29, 2020

@author: emader
'''

import struct

import FontTable
from OpenType import ScriptList


class Table(FontTable.Table):
    GSUB_TABLE_HEADER_FORMAT = ">HHHHH"
    GSUB_TABLE_HEADER_LENGTH = struct.calcsize(GSUB_TABLE_HEADER_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        # For now, we'll ignore version 1.1...
        (self.majorVersion, self.minorVersion, scriptListOffset, featureListOffset, lookupListOffset) = \
            struct.unpack(self.GSUB_TABLE_HEADER_FORMAT, rawTable[:self.GSUB_TABLE_HEADER_LENGTH])

        self.scriptList = ScriptList.ScriptList(rawTable, scriptListOffset)
