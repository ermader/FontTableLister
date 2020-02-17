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
import PostTable

def tableFactory(fontFile, tagBytes, checksum, offset, length):
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
    elif tagBytes == b'post':
        return PostTable.Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'vhea':
        return VheaTable.Table(fontFile, tagBytes, checksum, offset, length)
    else:
        return FontTable.Table(fontFile, tagBytes, checksum, offset, length)
