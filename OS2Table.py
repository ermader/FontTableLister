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

class OS2Table(FontTable.Table):

    OS2_TABLE_FORMAT_0_0 = ">HhHHHHHHHHHHHHHH"
    OS2_TABLE_FORMAT_0_1 = ">BBBBBBBBBB"  # Panose info
    OS2_TABLE_FORMAT_0_2 = ">HHHHHHHH4sHHHhhhhh"  # Unicode ranges, rest of format 0 part
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
        rawTable = self.rawData()

        formatStart = 0
        formatEnd = self.OS2_TABLE_FORMAT_0_0_LENGTH
        version, xAvgCharWidth, usWeightClass, usWidthClass, fsType, ySubscriptXSize, ySubscriptYSize, ySubscriptXOffset, ySubscriptYOffset, \
        ySuperscriptXSize, ySuperscriptYSize, ySuperscriptXOffset, ySuperscriptYOffset, yStrikeoutSize, yStrikeoutPosition, sFamilyclass \
            = struct.unpack(self.OS2_TABLE_FORMAT_0_0, rawTable[formatStart:formatEnd])

        FontTable.formatLine("Version", utility.formatDecimal(version))
        FontTable.formatLine("Avg Char Width", utility.formatDecimal(xAvgCharWidth))
        FontTable.formatLine("Weight Class", utility.formatDecimal(usWeightClass))
        FontTable.formatLine("Width Class", utility.formatDecimal(usWidthClass))
        FontTable.formatLine("Type Flags", utility.formatHex16(fsType))
        FontTable.formatLine("Subscript X Size", utility.formatDecimal(ySubscriptXSize))
        FontTable.formatLine("Subscript Y Size", utility.formatDecimal(ySubscriptYSize))
        FontTable.formatLine("Subscript X Offset", utility.formatDecimal(ySubscriptXOffset))
        FontTable.formatLine("Subscript Y Offset", utility.formatDecimal(ySubscriptYOffset))
        FontTable.formatLine("Superscript X Size", utility.formatDecimal(ySuperscriptXSize))
        FontTable.formatLine("Superscript Y Size", utility.formatDecimal(ySuperscriptYSize))
        FontTable.formatLine("Superscript X Offset", utility.formatDecimal(ySuperscriptXOffset))
        FontTable.formatLine("Superscript Y Offset", utility.formatDecimal(ySuperscriptYOffset))
        FontTable.formatLine("Strikeout Size", utility.formatDecimal(yStrikeoutSize))
        FontTable.formatLine("Strikeout Position", utility.formatDecimal(yStrikeoutPosition))
        FontTable.formatLine("Family Class", utility.formatHex16(sFamilyclass))

        formatStart = formatEnd
        formatEnd += self.OS2_TABLE_FORMAT_0_1_LENGTH
        panoseFamilyType, panoseSerifType, panoseWeight, panoseProportion, panoseContrast, panoseStrokeVariation, \
        panoseArmStype, panoseLetterForm, panoseMidLine, panoseXHeight = struct.unpack(self.OS2_TABLE_FORMAT_0_1, rawTable[formatStart:formatEnd])

        FontTable.formatLine("Panose Family Type", utility.formatHex8(panoseFamilyType))
        FontTable.formatLine("Panose Serif Type", utility.formatHex8(panoseSerifType))
        FontTable.formatLine("Panose Weight", utility.formatHex8(panoseWeight))
        FontTable.formatLine("Panose Proportion", utility.formatHex8(panoseProportion))
        FontTable.formatLine("Panose Contrast", utility.formatHex8(panoseContrast))
        FontTable.formatLine("Panose Stroke Variation", utility.formatHex8(panoseStrokeVariation))
        FontTable.formatLine("Panose Arm Style", utility.formatHex8(panoseArmStype))
        FontTable.formatLine("Panose Letter Form", utility.formatHex8(panoseLetterForm))
        FontTable.formatLine("Panose Mid Line", utility.formatHex8(panoseMidLine))
        FontTable.formatLine("Panose X Height", utility.formatHex8(panoseXHeight))

        formatStart = formatEnd
        formatEnd += self.OS2_TABLE_FORMAT_0_2_LENGTH

        ucRange1High, ucRange1Low, ucRange2High, ucRange2Low, ucRange3High, ucRange3Low, ucRange4High, ucRange4Low, \
        achVendID, fsSelection, usFirstCharIndex, usLastCharIndex, \
        sTypoAscender, sTypoDescender,sTypoLineGap, usWinAscent, usWinDescent = struct.unpack(self.OS2_TABLE_FORMAT_0_2, rawTable[formatStart:formatEnd])

        vendorID = achVendID.decode("ascii")

        FontTable.formatLine("Unicode Range 1", utility.formatHex32(utility.swapLongInt(ucRange1High, ucRange1Low)))
        FontTable.formatLine("Unicode Range 2", utility.formatHex32(utility.swapLongInt(ucRange2High, ucRange2Low)))
        FontTable.formatLine("Unicode Range 3", utility.formatHex32(utility.swapLongInt(ucRange3High, ucRange3Low)))
        FontTable.formatLine("Unicode Range 4", utility.formatHex32(utility.swapLongInt(ucRange4High, ucRange4Low)))
        FontTable.formatLine("Font Vendor ID", f"'{vendorID}'")
        FontTable.formatLine("Font Selection Flags", utility.formatHex16(fsSelection))
        FontTable.formatLine("First Char Index", utility.formatHex16(usFirstCharIndex))
        FontTable.formatLine("Last Char Index", utility.formatHex16(usLastCharIndex))
        FontTable.formatLine("Typographic Ascender", utility.formatDecimal(sTypoAscender))
        FontTable.formatLine("Typographic Descender", utility.formatDecimal(sTypoDescender))
        FontTable.formatLine("Typographic Line Gap", utility.formatDecimal(sTypoLineGap))
        FontTable.formatLine("Windows Ascent", utility.formatDecimal(usWinAscent))
        FontTable.formatLine("Windows Descent", utility.formatDecimal(usWinDescent))

        if version >= 1:
            formatStart = formatEnd
            formatEnd += self.OS2_TABLE_FORMAT_1_LENGTH

            ucpRange1High, ucpRange1Low, ucpRange2High, ucpRange2Low = struct.unpack(self.OS2_TABLE_FORMAT_1, rawTable[formatStart:formatEnd])

            FontTable.formatLine("Code Page Range 1", utility.formatHex32(utility.swapLongInt(ucpRange1High, ucpRange1Low)))
            FontTable.formatLine("Code Page Range 2", utility.formatHex32(utility.swapLongInt(ucpRange2High, ucpRange2Low)))

        if version >= 2:
            formatStart = formatEnd
            formatEnd += self.OS2_TABLE_FORMAT_2_LENGTH

            sxHeight, sCapHeight, usDefaultChar, usBreakChar, usMaxContext = struct.unpack(self.OS2_TABLE_FORMAT_2, rawTable[formatStart:formatEnd])

            FontTable.formatLine("x Height", utility.formatDecimal(sxHeight))
            FontTable.formatLine("Cap Height", utility.formatDecimal(sCapHeight))
            FontTable.formatLine("Default Char", utility.formatHex16(usDefaultChar))
            FontTable.formatLine("Break Char", utility.formatHex16(usBreakChar))
            FontTable.formatLine("Max Context", utility.formatDecimal(usMaxContext))
            
        print()
