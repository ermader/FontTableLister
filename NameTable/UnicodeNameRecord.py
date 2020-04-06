'''
Created on Feb 03, 2020

@author: emader
'''

from PlatformAndEncoding import PLATFORM_ID_UNICODE, UnicodePlatform, getPLatformName

from NameTable import NameRecord


class UnicodeNameRecord(NameRecord.NameRecord):
    def __init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes):
        NameRecord.NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes)

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

        self.languageNames = {}

    def platformName(self):
        return getPLatformName(PLATFORM_ID_UNICODE)

    def encodingName(self):
        return UnicodePlatform.getEncodingName(self.encodingID)

    def getStringEncoding(self):
        return self.stringEncodings.get(self.encodingID)