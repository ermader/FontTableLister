'''
Created on Mar 29, 2020

@author: emader
'''

import struct
import utility

class ScriptList:
    SCRIPT_LIST_TABLE_FORMAT = ">H"
    SCRIPT_LIST_TABLE_LENGTH = struct.calcsize(SCRIPT_LIST_TABLE_FORMAT)

    SCRIPT_RECORD_FORMAT = ">4sH"
    SCRIPT_RECORD_LENGTH = struct.calcsize(SCRIPT_RECORD_FORMAT)

    def __init__(self, rawTable, scriptListOffset):
        scriptListEnd = scriptListOffset + self.SCRIPT_LIST_TABLE_LENGTH
        (scriptCount,) = struct.unpack(self.SCRIPT_LIST_TABLE_FORMAT, rawTable[scriptListOffset:scriptListEnd])

        self.scriptRecords = []
        scriptRecordStart = scriptListEnd
        scriptRecordEnd = scriptRecordStart + self.SCRIPT_RECORD_LENGTH
        for _ in range(scriptCount):
            (scriptTagBytes, scriptOffset) = struct.unpack(self.SCRIPT_RECORD_FORMAT, rawTable[scriptRecordStart:scriptRecordEnd])
            self.scriptRecords.append(scriptTagBytes.decode("ascii"))
            scriptRecordStart = scriptRecordEnd
            scriptRecordEnd += self.SCRIPT_RECORD_LENGTH
