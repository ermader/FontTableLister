'''
Created on Feb 03, 2020

@author: emader
'''

import NameRecord

class MacintoshNameRecord(NameRecord.NameRecord):
    ENCODING_ID_ROMAN = 0
    ENCODING_ID_JAPANESE = 1
    ENCODING_ID_CHINESE_TRADITIONAL = 2
    ENCODING_ID_KOREAN = 3
    ENCODING_ID_ARABIC = 4
    ENCODING_ID_HEBREW = 5
    ENCODING_ID_GREEK = 6
    ENCODING_ID_RUSSIAN = 7
    ENCODING_ID_RSYMBOL = 8
    ENCODING_ID_DEVANAGARI = 9
    ENCODING_ID_GURMUKHI = 10
    ENCODING_ID_GUJARATI = 11
    ENCODING_ID_ORIYA = 12
    ENCODING_ID_BENGALI = 13
    ENCODING_ID_TAMIL = 14
    ENCODING_ID_TELEGU = 15
    ENCODING_ID_KANNADA = 16
    ENCODING_ID_MALAYALAM = 17
    ENCODING_ID_SINHALESE = 18
    ENCODING_ID_BURMESE = 19
    ENCODING_ID_KHMER = 20
    ENCODING_ID_THAI = 21
    ENCODING_ID_LAO = 22
    ENCODING_ID_GEORGIAN = 23
    ENCODING_ID_ARMENIAN = 24
    ENCODING_ID_CHINESE_SIMPLIFIED = 25
    ENCODING_ID_TIBETAN = 26
    ENCODING_ID_MONGOLIAN = 27
    ENCODING_ID_GEEZ = 28
    ENCODING_ID_SLAVIC = 29
    ENCODING_ID_VIETNAMESE = 30
    ENCODING_ID_SINDHI = 31

    def __init__(self, platformID, encodingID, languageID, nameID, length, offset):
        NameRecord.NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset)

        self.encodingNames = {
            self.ENCODING_ID_ROMAN : "Roman",
            self.ENCODING_ID_JAPANESE : "Japanese",
            self.ENCODING_ID_CHINESE_TRADITIONAL : "Chinese (Traditional)",
            self.ENCODING_ID_KOREAN : "Korean",
            self.ENCODING_ID_ARABIC : "Arabic",
            self.ENCODING_ID_HEBREW : "Hebrew",
            self.ENCODING_ID_GREEK : "Greek",
            self.ENCODING_ID_RUSSIAN : "Russian",
            self.ENCODING_ID_RSYMBOL : "RSymbol",
            self.ENCODING_ID_DEVANAGARI : "Devanagari",
            self.ENCODING_ID_GURMUKHI : "Gurmukhi",
            self.ENCODING_ID_GUJARATI : "Gujarati",
            self.ENCODING_ID_ORIYA : "Oriya",
            self.ENCODING_ID_BENGALI : "Bengali",
            self.ENCODING_ID_TAMIL : "Tamil",
            self.ENCODING_ID_TELEGU : "Telegu",
            self.ENCODING_ID_KANNADA : "Kannada",
            self.ENCODING_ID_MALAYALAM : "Malayalam",
            self.ENCODING_ID_SINHALESE : "Sinhalese",
            self.ENCODING_ID_BURMESE : "Burmese",
            self.ENCODING_ID_KHMER : "Khmer",
            self.ENCODING_ID_THAI : "Thai",
            self.ENCODING_ID_LAO : "Lao",
            self.ENCODING_ID_GEORGIAN : "Georgian",
            self.ENCODING_ID_ARMENIAN : "Armenian",
            self.ENCODING_ID_CHINESE_SIMPLIFIED : "Chinese (Simplified)",
            self.ENCODING_ID_TIBETAN : "Tibetan",
            self.ENCODING_ID_MONGOLIAN : "Mongolian",
            self.ENCODING_ID_GEEZ : "Geez",
            self.ENCODING_ID_SLAVIC : "Slavic",
            self.ENCODING_ID_VIETNAMESE : "Vietnamese",
            self.ENCODING_ID_SINDHI : "Sindhi"
        }


    def platformName(self):
        return "Macintosh"

    def encodingName(self):
        name = self.encodingNames.get(self.encodingID)

        if name is not None:
            return name

        return NameRecord.encodingName(self)
