'''
Created on Feb 03, 2020

@author: emader
'''

from PlatformAndEncoding import UnicodePlatform

from NameTable import NameRecord


class UnicodeNameRecord(NameRecord.NameRecord):
    def __init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes):
        NameRecord.NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes)

        self.encodingNames = {
            UnicodePlatform.ENCODING_ID_UNICODE_1_0 : "Unicode 1.0",
            UnicodePlatform.ENCODING_ID_UNICODE_1_1 : "Unicode 1.1",
            UnicodePlatform.ENCODING_ID_ISO_10646 : "ISO 10646",
            UnicodePlatform.ENCODING_ID_UNICODE_2_0_BMP_ONLY : "Unicode BMP",
            UnicodePlatform.ENCODING_ID_UNICODE_2_0_FULL : "Unicode",
            UnicodePlatform.ENCODING_ID_UNICODE_VARIATION_SEQUENCES : "Unicode Variation Sequences",
            UnicodePlatform.ENCODING_ID_UNICODE_FULL : "Unicode UCS4"
        }

        self.stringEncodings = {
            # not sure about most of these... UTF16BE is a superset of most of them...
            UnicodePlatform.ENCODING_ID_UNICODE_1_0: "utf_16_be",
            UnicodePlatform.ENCODING_ID_UNICODE_1_1: "utf_16_be",
            UnicodePlatform.ENCODING_ID_ISO_10646: "utf_16_be",
            UnicodePlatform.ENCODING_ID_UNICODE_2_0_BMP_ONLY: "utf_16_be",
            UnicodePlatform.ENCODING_ID_UNICODE_2_0_FULL: "utf_16_be",
            UnicodePlatform.ENCODING_ID_UNICODE_VARIATION_SEQUENCES: "utf_16_be",
            UnicodePlatform.ENCODING_ID_UNICODE_FULL: "utf_32-be"
        }

    def platformName(self):
        return "Unicode"

    def getStringEncoding(self):
        return self.stringEncodings.get(self.encodingID)