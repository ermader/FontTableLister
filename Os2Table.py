'''
Created on Feb 13, 2020

@author: emader
'''

import struct
import utility

import FontTable

# typedef struct {
#     // Version 0
#     UInt16 version;             // offset 0
#     SInt16 xAvgCharWidth;
#     UInt16 usWeightClass;
#     UInt16 usWidthClass;
#     UInt16 fsType;
#     SInt16 ySubscriptXSize;     // offset 10
#     SInt16 ySubscriptYSize;
#     SInt16 ySubscriptXOffset;
#     SInt16 ySubscriptYOffset;
#     SInt16 ySuperscriptXSize;
#     SInt16 ySuperscriptYSize;   // offset 20
#     SInt16 ySuperscriptXOffset;
#     SInt16 ySuperscriptYOffset;
#     SInt16 yStrikeoutSize;
#     SInt16 yStrikeoutPosition;
#     SInt16 sFamilyClass;        // offset 30
#
#     UInt8  panoseFamilyType;
#     UInt8  panoseSerifStyle;
#     UInt8  panoseWeight;
#     UInt8  panoseProportion;
#     UInt8  panoseContrast;
#     UInt8  PanoseStrokeVariation;
#     UInt8  panoseArmStyle;
#     UInt8  panoseLetterForm;
#     UInt8  panoseMidline;
#     UInt8  panoseXHeight;       // offset 40
#
# //    Need to split these up because they're not on long word boundaries
#     UInt16 ulUnicodeRange1Low;
#     UInt16 ulUnicodeRange1High;
#     UInt16 ulUnicodeRange2Low;
#     UInt16 ulUnicodeRange2High;
#     UInt16 ulUnicodeRange3Low;  // offset 50
#     UInt16 ulUnicodeRange3High;
#     UInt16 ulUnicodeRange4Low;
#     UInt16 ulUnicodeRange4High;
#     UInt16 achVendIDLow;        // four char tag
#     UInt16 achVendIDHigh;       // offset 60
#
#     UInt16 fsSelection;
#     UInt16 usFirstCharIndex;
#     UInt16 usLastCharIndex;
#     SInt16 sTypoAscender;
#     SInt16 sTypoDescender;      // offset 70
#     SInt16 sTypoLineGap;
#     SInt16 usWinAscent;
#     SInt16 usWinDescent;        // offset 76
#
#     // Version 1 additions
#     // Not on a long word boundary
#     UInt16 ulCodePageRange1Low;
#     UInt16 ulCodePageRange1High;
#     UInt16 ulCodePageRange2Low;
#     UInt16 ulCodePageRange2High;
#
#     // Version 2 additions
#     SInt16 sxHeight;
#     SInt16 sCapHeight;
#     UInt16 usDefaultChar;
#     UInt16 usBreakChar;
#     UInt16 usMaxContext;
#
#     // Version 5 additions
#     UInt16 usLowerOpticalPointSize;
#     UInt16 usUpperOpticalPointSize;
# } FFLRawOs2Table;

class Os2Table(FontTable.Table):

    OS2_TABLE_FORMAT_0_0 = ">HhHHHHHHHHHHHHHH"
    OS2_TABLE_FORMAT_0_1 = ">BBBBBBBBBB"  # Panose info
    OS2_TABLE_FORMAT_0_2 = ">HHHHHHHHHHHHHhhhhh"  # Unicode ranges, rest of format 0 part
    OS2_TABLE_FORMAT_1 = ">HHHH"  # Format 1 additions
    OS2_TABLE_FORMAT_2 = ">HHHHH"  # Format 2 additions
    OS2_TABLE_FORMAT_5 = ">HH"  # Format 5 additions

    OS2_TABLE_FORMAT_0_0_LENGTH = struct.calcsize(OS2_TABLE_FORMAT_0_0)
    OS2_TABLE_FORMAT_0_1_LENGTH = struct.calcsize(OS2_TABLE_FORMAT_0_1)
    OS2_TABLE_FORMAT_0_2_LENGTH = struct.calcsize(OS2_TABLE_FORMAT_0_2)
    OS2_TABLE_FORMAT_1_LENGTH = struct.calcsize(OS2_TABLE_FORMAT_1)
    OS2_TABLE_FORMAT_2_LENGTH = struct.calcsize(OS2_TABLE_FORMAT_2)
    OS2_TABLE_FORMAT_5_LENGTH = struct.calcsize(OS2_TABLE_FORMAT_5)

    def format(self):
        print()
