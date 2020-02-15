'''
Created on Feb 13, 2020

@author: emader
'''

import struct
import utility

import FontTable

# typedef struct {
#     Fixed version;
#     Fixed italicAngle;
#     FWord underlinePosition;
#     FWord underlineThickness;
#     UInt32 isFixedPitch;
#     UInt32 minMemType42;
#     UInt32 maxMemType42;
#     UInt32 minMemType1;
#     UInt32 maxMemType1;
# } FFLRawPostHeader;
#
# typedef struct {
#     UInt16 numGlyphs;
#     UInt16 glyphNameIndex[1]; // numGlyphs long
#     UInt8  names[1];          // numGlyph - 258 strings...
# } FFLRawPostStringTable;

class Table(FontTable.Table):
    POST_TABLE_HEADER_FORMAT = ">iihhIIIII"
    POST_TABLE_HEADER_LENGTH = struct.calcsize(POST_TABLE_HEADER_FORMAT)

    def format(self):
        rawTable = self.rawData()

        version, italicAngle, underlinePosition, underlineThickness, isFixedPitch, \
        minMemType42, maxMemType42, minMemType1, maxMemType1 = struct.unpack(self.POST_TABLE_HEADER_FORMAT, rawTable[:self.POST_TABLE_HEADER_LENGTH])

        FontTable.formatLine("Version", utility.formatFixed(version))
        FontTable.formatLine("Italic Angle", utility.formatFixed(italicAngle))
        FontTable.formatLine("Underline Position", utility.formatDecimal(underlinePosition))
        FontTable.formatLine("Underline Thickness", utility.formatDecimal(underlineThickness))
        FontTable.formatLine("isFixedPitch", f"{isFixedPitch != 0}")
        FontTable.formatLine("Min Memory Type42", utility.formatDecimal(minMemType42))
        FontTable.formatLine("Max Memory Type43", utility.formatDecimal(maxMemType42))
        FontTable.formatLine("Min Memory Type1", utility.formatDecimal(minMemType1))
        FontTable.formatLine("Max Memory Type1", utility.formatDecimal(maxMemType1))

        print()
