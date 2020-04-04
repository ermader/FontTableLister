'''
Created on Jan 26, 2020

@author: emader
'''

import FontTable
import HeadTable
import HheaTable
from NameTable import NameTable
import MaxpTable
import VheaTable
import OS2Table
import PostTable
from OpenType import GSUBTable
from OpenType import GPOSTable
from OpenType import GDEFTable


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
    elif tagBytes == b'GDEF':
        return GDEFTable.Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'GSUB':
        return GSUBTable.Table(fontFile, tagBytes, checksum, offset, length)
    elif tagBytes == b'GPOS':
        return GPOSTable.Table(fontFile, tagBytes, checksum, offset, length)
    else:
        return FontTable.Table(fontFile, tagBytes, checksum, offset, length)
