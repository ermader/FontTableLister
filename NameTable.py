'''
Created on Feb 03, 2020

@author: emader
'''

import struct

import utility
import FontTable
import NameRecordFactory

# typedef struct {
#     UInt16 format;
#     UInt16 count;
#     UInt16 stringOffset;
#     // followed by name records
# } FFLRawNameTableHeader;

class NameTable(FontTable.Table):
    NAME_TABLE_HEADER_FORMAT = ">HHH"
    NAME_TABLE_HEADER_LENGTH = struct.calcsize(NAME_TABLE_HEADER_FORMAT)

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)
        self.nameRecords = None

    def getNameRecords(self):
        if self.nameRecords == None:
            rawBytes = self.rawData()
            self.format, self.count, self.stringOffset = struct.unpack(self.NAME_TABLE_HEADER_FORMAT, rawBytes[:self.NAME_TABLE_HEADER_LENGTH])

            self.nameRecords = []
            nameRecordOffset = self.NAME_TABLE_HEADER_LENGTH

            for _ in range(self.count):
                rawNameRecord = rawBytes[nameRecordOffset : nameRecordOffset + NameRecordFactory.NAME_RECORD_LENGTH]
                self.nameRecords.append(NameRecordFactory.nameRecordFactory(rawNameRecord))
                nameRecordOffset += NameRecordFactory.NAME_RECORD_LENGTH


        return self.nameRecords

    def format(self):
        self.getNameRecords()

        for nameRecord in self.nameRecords:
            print(f"{nameRecord.platformName()} {nameRecord.encodingName()} {nameRecord.languageName()} {nameRecord.nameIDName()}")
