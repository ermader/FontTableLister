'''
Created on Feb 03, 2020

@author: emader
'''

import struct

import FontTable
from NameTable import NameRecordFactory


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
            self.nameTableFormat, self.count, self.stringOffset = struct.unpack(self.NAME_TABLE_HEADER_FORMAT, rawBytes[:self.NAME_TABLE_HEADER_LENGTH])

            self.stringBytes = rawBytes[self.stringOffset:]

            self.nameRecords = []
            nameRecordStart = self.NAME_TABLE_HEADER_LENGTH
            nameRecordEnd = nameRecordStart + NameRecordFactory.NAME_RECORD_LENGTH

            for _ in range(self.count):
                rawNameRecord = rawBytes[nameRecordStart:nameRecordEnd]
                self.nameRecords.append(NameRecordFactory.nameRecordFactory(rawNameRecord, self.stringBytes))
                nameRecordStart = nameRecordEnd
                nameRecordEnd += NameRecordFactory.NAME_RECORD_LENGTH


        return self.nameRecords

    def findName(self, platformID, nameID, languageID):
        self.getNameRecords()
        for nameRecord in self.nameRecords:
            if nameRecord.platformID == platformID and nameRecord.nameID == nameID and nameRecord.languageID == languageID:
                return nameRecord.getString()

        return None

    def format(self, parentFont):
        self.getNameRecords()

        for nameRecord in self.nameRecords:
            str = nameRecord.getString().replace("\r", "\\r").replace("\n", "\\n")
            print(f"      {nameRecord.platformName():10} {nameRecord.encodingName():20} {nameRecord.languageName():20} {nameRecord.nameIDName():25} {str}")
