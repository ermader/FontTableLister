'''
Created on Jan 26, 2020

@author: emader
'''
import struct
import utility


import FontTable

# typedef struct {
#     Fixed version;
#     UInt16 numGlyphs;
#     UInt16 maxPoints;
#     UInt16 maxContours;
#     UInt16 maxComponentPoints;
#     UInt16 maxComponentContours;
#     UInt16 maxZones;
#     UInt16 maxTwilightPoints;
#     UInt16 maxStorage;
#     UInt16 maxFunctionDefs;
#     UInt16 maxInstructionDefs;
#     UInt16 maxStackElements;
#     UInt16 maxSizeOfInstructions;
#     UInt16 maxComponentElements;
#     UInt16 maxComponentDepth;
# } FFLRawMaxpTable;

class Table(FontTable.Table):
    MAXP_TABLE_FORMAT = ">i14H"
    MAXP_TABLE_LENGTH = struct.calcsize(MAXP_TABLE_FORMAT)

    def format(self):
        rawTable = self.rawData()
        (version, numGlyphs, maxPoints, maxContours, maxComponentPoints, maxComponentContours, maxZones, maxTwilightPoints, maxStorage, maxFunctionDefs, maxInstructionDefs, maxStackElements, maxSizeOfInstructions, maxComponentElements, maxComponentDepth) = struct.unpack(self.MAXP_TABLE_FORMAT, rawTable)

        FontTable.formatLine("Version", utility.formatFixed(version))
        FontTable.formatLine("Number of Glyphs", utility.formatDecimal(numGlyphs))
        FontTable.formatLine("Max Points", utility.formatDecimal(maxPoints))
        FontTable.formatLine("Max Contours", utility.formatDecimal(maxContours))
        FontTable.formatLine("Max Component Points", utility.formatDecimal(maxComponentPoints))
        FontTable.formatLine("Max Component Contours", utility.formatDecimal(maxComponentContours))
        FontTable.formatLine("Max Zones", utility.formatDecimal(maxZones))
        FontTable.formatLine("Max Twilight Points", utility.formatDecimal(maxTwilightPoints))
        FontTable.formatLine("Max Storage", utility.formatDecimal(maxStorage))
        FontTable.formatLine("Max Function Definitions", utility.formatDecimal(maxFunctionDefs))
        FontTable.formatLine("Max Instruction Defs", utility.formatDecimal(maxInstructionDefs))
        FontTable.formatLine("Max Stack Elements", utility.formatDecimal(maxStackElements))
        FontTable.formatLine("Max Size of Instructions", utility.formatDecimal(maxSizeOfInstructions))
        FontTable.formatLine("Max Component Elements", utility.formatDecimal(maxComponentElements))
        FontTable.formatLine("Max Component Depth", utility.formatDecimal(maxComponentDepth))