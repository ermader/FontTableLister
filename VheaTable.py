'''
Created on Feb 13, 2020

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
#     UFWord advanceHeightMax;
#     FWord minTopSideBearing;
#     FWord minBottomSideBearing;
#     FWord yMaxExtent;
#     SInt16 caretSlopeRise;
#     SInt16 caretSlopeRun;
#     FWord caretOffset;
#     SInt16 reserved[4];
#     SInt16 metricDataFormat;
#     UInt16 numOfLongVertMetrics;
# } FFLRawVHeadTable;

class Table(FontTable.Table):
    VHEA_TABLE_FORMAT = ">ihhhHhhhhhh4hhh"
    VHEA_Table_LENGTH = struct.calcsize(VHEA_TABLE_FORMAT)

    def format(self, parentFont):
        rawTable = self.rawData()
        version, ascent, descent, lineGap, advanceHeightMax, minTopSideBearing, minBottomSideBearing, yMaxExtent,\
        caretSlopeRise, caretSlopeRun, caretOffset, r0, r1, r2, r3, metricDataFormat, numOfLongVertMetrics = struct.unpack(self.VHEA_TABLE_FORMAT, rawTable)

        FontTable.formatLine("Version", utility.formatFixed(version))
        FontTable.formatLine("Ascent", utility.formatDecimal(ascent))
        FontTable.formatLine("Descent", utility.formatDecimal(descent))
        FontTable.formatLine("Line Gap", utility.formatDecimal(lineGap))
        FontTable.formatLine("Advance Height Max", utility.formatDecimal(advanceHeightMax))
        FontTable.formatLine("Min Top Side Bearing", utility.formatDecimal(minTopSideBearing))
        FontTable.formatLine("Min Bottom Side Bearing", utility.formatDecimal(minBottomSideBearing))
        FontTable.formatLine("yx Max Extent", utility.formatDecimal(yMaxExtent))
        FontTable.formatLine("Caret Slope Rise", utility.formatDecimal(caretSlopeRise))
        FontTable.formatLine("Caret Slope Run", utility.formatDecimal(caretSlopeRun))
        FontTable.formatLine("Caret Offset", utility.formatDecimal(caretOffset))
        FontTable.formatLine("Metric Data Format", utility.formatDecimal(metricDataFormat))
        FontTable.formatLine("Number of Long Vertical Metrics", utility.formatDecimal(numOfLongVertMetrics))


