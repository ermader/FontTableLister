'''
Created on Feb 03, 2020

@author: emader
'''

import struct

import utility
import FontTable
import NameRecord

class UnicodeNameRecord(NameRecord.NameRecord):
    ENCODING_ID_UNICODE_1_0 = 0
    ENCODING_ID_UNICODE_1_1 = 1
    ENCODING_ID_ISO_10646 = 2
    ENCODING_ID_UNICODE_2_0_BMP_ONLY = 3
    ENCODING_ID_UNICODE_2_0_FULL = 4
    ENCODING_ID_UNICODE_VARIATION_SEQUENCES = 5
    ENCODING_ID_UNICODE_FULL = 6

    def __init(self, platformID, encodingID, languageID, nameID, length, offset):
        NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset)

        self.encodingNames = {
            self.ENCODING_ID_UNICODE_1_0 : "Unicode 1.0",
            self.ENCODING_ID_UNICODE_1_1 : "Unicode 1.1",
            self.ENCODING_ID_ISO_10646 : "ISO 10646",
            self.ENCODING_ID_UNICODE_2_0_BMP_ONLY : "Unicode BMP",
            self.ENCODING_ID_UNICODE_2_0_FULL : "Unicode",
            self.ENCODING_ID_UNICODE_VARIATION_SEQUENCES : "Unicode Variation Sequences",
            self.ENCODING_ID_UNICODE_FULL : "Unicode UCS4"
        }

    def platformName(self):
        return "Unicode"

    def encodingName(self):
        name = self.encodingNames.get(self.encodingID)

        if name is not None:
            return name

        return NameRecord.encodingName(self)

