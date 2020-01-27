'''
Created on Jan 26, 2020

@author: emader
'''

import struct

import utility
import FontTable

# typedef struct {
#     Fixed version;              // 00
#     Fixed fontRevision;         // 04
#     UInt32 checksumAdjustment;  // 08
#     UInt32 magicNumber;         // 12
#     UInt16 flags;               // 16
#     UInt16 unitsPerEm;          // 18
# //  LongDateTime creationDate;  // 20
#     UInt32 creationDate0;       // Need to split as two UInt32s because it's not on an 8 byte boundary (really?)
#     UInt32 creationDate1;
# //  LongDateTime modifiedDate;  // 28
#     UInt32 modifiedDate0;
#     UInt32 modifiedDate1;
#     FWord xMin;                 // 36
#     FWord yMin;                 // 38
#     FWord xMax;                 // 40
#     FWord yMax;                 // 42
#     UInt16 macStyle;            // 44
#     UInt16 lowestRecPPEM;       // 46
#     SInt16 fontDirectionHint;   // 48
#     SInt16 indexToLocFormat;    // 50
#     SInt16 glyphDataFormat;     // 52
#                                 // 54
#
# } FFLRawHeadTable;

class Table(FontTable.Table):
    HEAD_TABLE_FORMAT = ">iiIIHHIIIIhhhhHHhhh"
    HEAD_TABLE_LENGTH = struct.calcsize(HEAD_TABLE_FORMAT)

    def format(self):
        rawTable = self.rawData()
        version, revision, adjust, magic, flags, upm, cd0, cd1, md0, md1, xMin, yMin, xMax, yMax, style, lowPPEM, dirHint, ilocFormat, gdFormat = struct.unpack(
            self.HEAD_TABLE_FORMAT, rawTable)

        creationDate = utility.swapLongDateTime(cd0, cd1)
        modDate = utility.swapLongDateTime(md0, md1)
        FontTable.formatLine("Version", utility.formatFixed(version))
        FontTable.formatLine("Font Revision", utility.formatFixed(revision))
        FontTable.formatLine("Checksum Adjustment", utility.formatHex32(adjust))
        FontTable.formatLine("Magic Number", utility.formatHex32(magic))
        FontTable.formatLine("Flags", utility.formatHex16(flags))
        FontTable.formatLine("Units Per EM", utility.formatDecimal(upm))
        FontTable.formatLine("Creation Date", utility.formatLongDateTime(creationDate))
        FontTable.formatLine("Modification Date", utility.formatLongDateTime(modDate))
        FontTable.formatLine("xMin", utility.formatDecimal(xMin))
        FontTable.formatLine("yMin", utility.formatDecimal(yMin))
        FontTable.formatLine("xMax", utility.formatDecimal(xMax))
        FontTable.formatLine("yMax", utility.formatDecimal(yMax))
        FontTable.formatLine("Mac Style", utility.formatHex16(style))
        FontTable.formatLine("Lowest Rec PPEM", utility.formatDecimal(lowPPEM))
        FontTable.formatLine("Font Direction Hint", utility.formatDecimal(dirHint))
        FontTable.formatLine("Index to Loc Format", utility.formatDecimal(ilocFormat))
        FontTable.formatLine("Glyph Data Format", utility.formatDecimal(gdFormat))
        print()
