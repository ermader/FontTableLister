'''
Created on Jan 26, 2020

@author: emader
'''

import struct
import utility

import FontTable

# typedef struct {
#     Fixed version;
#     FWord ascent;
#     FWord descent;
#     FWord lineGap;
#     UFWord advanceWidthMax;
#     FWord minLeftSideBearing;
#     FWord minRightSideBearing;
#     FWord xMaxExtent;
#     SInt16 caretSlopeRise;
#     SInt16 caretSlopeRun;
#     FWord caretOffset;
#     SInt16 reserved[4];
#     SInt16 metricDataFormat;
#     UInt16 numOfLongMetrics;
# } FFLRawHHeadTable;

class Table(FontTable.Table):
    HHEA_TABLE_FORMAT = ">ihhhHhhhhhh4hhH"
    HHEA_TABLE_LENGTH = struct.calcsize(HHEA_TABLE_FORMAT)

    def format(self):
        rawTable = self.rawData()
        version, ascent, descent, lineGap, awMax, lsbMin, rsbMin, xMaxExtent, caretSlopeRise, caretSlopeRun, caretOffset, r0, r1, r2, r2, metricDataFormat, numLongMetrics = struct.unpack(self.HHEA_TABLE_FORMAT, rawTable)

        FontTable.formatLine("Version", utility.formatFixed(version))
        FontTable.formatLine("Ascent", utility.formatDecimal(ascent))
        FontTable.formatLine("Descent", utility.formatDecimal(descent))
        FontTable.formatLine("Line Gap", utility.formatDecimal(lineGap))
        FontTable.formatLine("Advance Width Max", utility.formatDecimal(awMax))
        FontTable.formatLine("Min Left Side Bearing", utility.formatDecimal(lsbMin))
        FontTable.formatLine("Min Right Side Bearing", utility.formatDecimal(rsbMin))
        FontTable.formatLine("x Max Extent", utility.formatDecimal(xMaxExtent))
        FontTable.formatLine("Caret Slope Rise", utility.formatDecimal(caretSlopeRise))
        FontTable.formatLine("Caret Slope Run", utility.formatDecimal(caretSlopeRun))
        FontTable.formatLine("Caret Offset", utility.formatDecimal(caretOffset))
        FontTable.formatLine("Metric Data Format", utility.formatDecimal(metricDataFormat))
        FontTable.formatLine("Number of Long Metrics", utility.formatDecimal(numLongMetrics))