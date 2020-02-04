'''
Created on Feb 03, 2020

@author: emader
'''

import NameRecord

class WindowsNameRecord(NameRecord.NameRecord):
    ENCODING_ID_SYMBOL = 0
    ENCODING_ID_UNICODE_BMP = 1
    ENCODING_ID_SHIFT_JIS = 2
    ENCODING_ID_PRC = 3
    ENCODING_ID_BIG_5 = 4
    ENCODING_ID_WANSUNG = 5
    ENCODING_ID_JOHAB = 6
    # 7 - 9 reserved
    ENCODING_ID_UNICODE_UCS4 = 10

    def __init__(self, platformID, encodingID, languageID, nameID, length, offset):
        NameRecord.NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset)

        self.encodingNames = {
            self.ENCODING_ID_SYMBOL : "Symbol",
            self.ENCODING_ID_UNICODE_BMP : "Unicode BMP",
            self.ENCODING_ID_SHIFT_JIS : "Shift JIS",
            self.ENCODING_ID_PRC : "PRC",
            self.ENCODING_ID_BIG_5 : "Big 5",
            self.ENCODING_ID_WANSUNG : "Wansung",
            self.ENCODING_ID_JOHAB : "Johab",
            self.ENCODING_ID_UNICODE_UCS4 : "Unicode UCS4"
        }

    def platformName(self):
        return "Windows"

    def encodingName(self):
        name = self.encodingNames.get(self.encodingID)

        if name is not None:
            return name

        return NameRecord.encodingName(self)
