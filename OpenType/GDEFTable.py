'''
Created on Apr 2, 2020

@author: emader
'''

import struct

import FontTable

from OpenType import ClassDefinitionTable

classNames = {
    1: "Base Glyph",
    2: "Ligature Glyph",
    3: "Mark Glyph",
    4: "Component Glyph"
}

class Table(FontTable.Table):
    GDEF_TABLE_HEADER_FORMAT = ">HHHHHH"
    GDEF_TABLE_HEADER_LENGTH = struct.calcsize(GDEF_TABLE_HEADER_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

        # For now, we'll only handle format 1.0
        (self.majorVersion, self.minorVersion, glyphClassDefOffset, attachListOffset, ligCaretListOffset, markAttachClassDefOffset) =\
            struct.unpack(self.GDEF_TABLE_HEADER_FORMAT, rawTable[:self.GDEF_TABLE_HEADER_LENGTH])

        self.classDefinitionTable = ClassDefinitionTable.Table(rawTable, glyphClassDefOffset) if glyphClassDefOffset != 0 else None

    def format(self, parentFont):
        self.classDefinitionTable.format(classNames, parentFont)
        print()