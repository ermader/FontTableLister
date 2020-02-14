'''
Created on Jan 26, 2020

@author: emader
'''
import struct

import FontTable
import HeadTable
import HheaTable
import NameTable
import MaxpTable
import VheaTable
import OS2Table

FONT_DIRECTORY_ENTRY_FORMAT = ">4sIII"
FONT_DIRECTORY_ENTRY_LENGTH = struct.calcsize(FONT_DIRECTORY_ENTRY_FORMAT)

def tableFactory(fontFile):
    directoryEntryData = fontFile.read(FONT_DIRECTORY_ENTRY_LENGTH)
    tagBytes, checksum, offset, length = struct.unpack(FONT_DIRECTORY_ENTRY_FORMAT, directoryEntryData)

    if tagBytes == b'head':
        return HeadTable.Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'hhea':
        return HheaTable.Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'name':
        return NameTable.NameTable(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'maxp':
        return MaxpTable.Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'OS/2':
        return OS2Table.OS2Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'vhea':
        return VheaTable.Table(fontFile, tagBytes, checksum, offset, length)
    else:
        return FontTable.Table(fontFile, tagBytes, checksum, offset, length)
