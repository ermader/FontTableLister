'''
Created on Apr 1, 2020

@author: emader
'''

import struct
import utility

class FeatureTable:
    FEATURE_TABLE_FORMAT = ">HH"
    FEATURE_TABLE_LENGTH = struct.calcsize(FEATURE_TABLE_FORMAT)

    def __init__(self, rawTable, featureTag, featureTableOffset):
        self.featureTag = featureTag
        featureTableStart = featureTableOffset
        featureTableEnd = featureTableStart + self.FEATURE_TABLE_LENGTH
        (self.featureParams, lookupIndexCount) = struct.unpack(self.FEATURE_TABLE_FORMAT, rawTable[featureTableStart:featureTableEnd])

        lookupIndicesFormat = f">{lookupIndexCount}H"
        lookupIndicesLength = struct.calcsize(lookupIndicesFormat)
        lookupIndicesStart = featureTableEnd
        lookupIndicesEnd = lookupIndicesStart + lookupIndicesLength
        self.lookupIndices = struct.unpack(lookupIndicesFormat, rawTable[lookupIndicesStart:lookupIndicesEnd])

    def format(self, featureIndex):
        print(f"      Feature{featureIndex:02d}: '{self.featureTag}'")
        for lookupIndex in self.lookupIndices:
            print(f"        Lookup{lookupIndex:02d}")

        print()

class FeatureListTable:
    FEATURE_LIST_TABLE_FORMAT = ">H"
    FEATURE_LIST_TABLE_LENGTH = struct.calcsize(FEATURE_LIST_TABLE_FORMAT)

    FEATURE_RECORD_FORMAT = ">4sH"
    FEATURE_RECORD_LENGTH = struct.calcsize(FEATURE_RECORD_FORMAT)

    def __init__(self, rawTable, featureListOffset):
        featureListEnd = featureListOffset + self.FEATURE_LIST_TABLE_LENGTH
        (featureCount,) = struct.unpack(self.FEATURE_LIST_TABLE_FORMAT, rawTable[featureListOffset:featureListEnd])

        self.featureTables = []
        featureRecordStart = featureListEnd
        featureRecordEnd = featureRecordStart + self.FEATURE_RECORD_LENGTH
        for _ in range(featureCount):
            (featureTagBytes, featureOffset) = struct.unpack(self.FEATURE_RECORD_FORMAT, rawTable[featureRecordStart:featureRecordEnd])
            featureTag = featureTagBytes.decode("ascii")
            self.featureTables.append(FeatureTable(rawTable, featureTag, featureListOffset+featureOffset))
            featureRecordStart = featureRecordEnd
            featureRecordEnd += self.FEATURE_RECORD_LENGTH

    def format(self):
        featureIndex = 0
        for featureTable in self.featureTables:
            featureTable.format(featureIndex)
            featureIndex += 1