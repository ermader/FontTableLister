'''
Created on Apr 4, 2020

@author: emader
'''

import struct
import utility

import FontTable

class Table:
    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        FontTable.Table.__init__(self, fontFile, tagBytes, checksum, offset, length)

        rawTable = self.rawData()

