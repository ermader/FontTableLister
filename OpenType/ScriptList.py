'''
Created on Mar 29, 2020

@author: emader
'''

import struct
import utility

def formatLine(label, value):
    print(f"          {label + ':':<25s}{value:>10s}")

class LangSysTable:
    LANG_SYS_TABLE_FORMAT = ">HHH"
    LANG_SYS_TABLE_LENGTH = struct.calcsize(LANG_SYS_TABLE_FORMAT)

    def __init__(self, rawTable, langSysTag, langSysOffset):
        self.langSysTag = langSysTag

        langSysStart = langSysOffset
        langSysEnd = langSysStart + self.LANG_SYS_TABLE_LENGTH
        (self.lookupOrder, self.requiredFeatureIndex, featureIndexCount) = \
            struct.unpack(self.LANG_SYS_TABLE_FORMAT, rawTable[langSysStart:langSysEnd])

        featureIndicesTableFormat = f">{featureIndexCount:d}H"
        featureIndicesTableLength = struct.calcsize(featureIndicesTableFormat)
        featureIndicesTableStart = langSysEnd
        featureIndicesTableEnd = featureIndicesTableStart + featureIndicesTableLength
        self.featureIndicesTable = struct.unpack(featureIndicesTableFormat, rawTable[featureIndicesTableStart:featureIndicesTableEnd])

    def format(self):
        print(f"        language: '{self.langSysTag}':")
        formatLine("Lookup Order", utility.formatHex16(self.lookupOrder))
        formatLine("Required Feature Index", utility.formatDecimal(self.requiredFeatureIndex))
        print("          Feature Indices:")
        for featureIndex in self.featureIndicesTable:
            print(f"            Feature{featureIndex:02d}")

class ScriptTable:
    SCRIPT_TABLE_FORMAT = ">HH"
    SCRIPT_TABLE_LENGTH = struct.calcsize(SCRIPT_TABLE_FORMAT)

    LANG_SYS_RECORD_FORMAT = ">4sH"
    LANG_SYS_RECORD_LENGTH = struct.calcsize(LANG_SYS_RECORD_FORMAT)

    def __init__(self, rawTable, scriptTag, scriptTableOffset):
        scriptTableStart = scriptTableOffset
        scriptTableEnd = scriptTableStart + self.SCRIPT_TABLE_LENGTH

        self.langSysTables = []
        self.scriptTag = scriptTag
        (defaultLangSysOffset, langSysCount) = struct.unpack(self.SCRIPT_TABLE_FORMAT, rawTable[scriptTableStart:scriptTableEnd])

        self.defaultLangSysTable = LangSysTable(rawTable, 'dflt', scriptTableOffset+defaultLangSysOffset)

        langSysRecordStart = scriptTableEnd
        langSysRecordEnd = langSysRecordStart + self.LANG_SYS_RECORD_LENGTH
        for _ in range(langSysCount):
            (langSysTagBytes, langSysOffset) = struct.unpack(self.LANG_SYS_RECORD_FORMAT, rawTable[langSysRecordStart:langSysRecordEnd])
            langSysTag = langSysTagBytes.decode("ascii")
            self.langSysTables.append(LangSysTable(rawTable, langSysTag, scriptTableOffset+langSysOffset))
            langSysRecordStart = langSysRecordEnd
            langSysRecordEnd += self.LANG_SYS_RECORD_LENGTH

    def format(self):
        print(f"      script: '{self.scriptTag}':")
        self.defaultLangSysTable.format()
        for langSysTable in self.langSysTables:
            langSysTable.format()

class ScriptListTable:
    SCRIPT_LIST_TABLE_FORMAT = ">H"
    SCRIPT_LIST_TABLE_LENGTH = struct.calcsize(SCRIPT_LIST_TABLE_FORMAT)

    SCRIPT_RECORD_FORMAT = ">4sH"
    SCRIPT_RECORD_LENGTH = struct.calcsize(SCRIPT_RECORD_FORMAT)

    def __init__(self, rawTable, scriptListOffset):
        scriptListEnd = scriptListOffset + self.SCRIPT_LIST_TABLE_LENGTH
        (scriptCount,) = struct.unpack(self.SCRIPT_LIST_TABLE_FORMAT, rawTable[scriptListOffset:scriptListEnd])

        self.scriptTables = []
        scriptRecordStart = scriptListEnd
        scriptRecordEnd = scriptRecordStart + self.SCRIPT_RECORD_LENGTH
        for _ in range(scriptCount):
            (scriptTagBytes, scriptOffset) = struct.unpack(self.SCRIPT_RECORD_FORMAT, rawTable[scriptRecordStart:scriptRecordEnd])
            scriptTag = scriptTagBytes.decode("ascii")
            self.scriptTables.append(ScriptTable(rawTable, scriptTag, scriptListOffset+scriptOffset))
            scriptRecordStart = scriptRecordEnd
            scriptRecordEnd += self.SCRIPT_RECORD_LENGTH

    def format(self):
        for scriptTable in self.scriptTables:
            scriptTable.format()
            print()