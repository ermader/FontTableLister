'''
Created on Apr 4, 2020

@author: emader
'''

PLATFORM_ID_UNICODE = 0
PLATFORM_ID_MACINTOSH = 1
# platform ID 2 is deprecated
PLATFORM_ID_WINDOWS = 3
PLATFORM_ID_CUSTOM = 4

platformNames = {
    PLATFORM_ID_UNICODE: "Unicode",
    PLATFORM_ID_MACINTOSH: "Macintosh",
    PLATFORM_ID_WINDOWS: "Windows",
    PLATFORM_ID_CUSTOM: "Custom"
}

def getPLatformName(platformID):
    platformName = platformNames.get(platformID)
    
    return platformName if platformName is not None else f"PLatform {platformID}"

def getEncodingName(platformID, encodingID):
    if platformID == PLATFORM_ID_UNICODE:
        encodingName = UnicodePlatform.getEncodingName(encodingID)
    elif platformID == PLATFORM_ID_MACINTOSH:
        encodingName = MacintoshPlatform.getEncodingName(encodingID)
    elif platformID == PLATFORM_ID_WINDOWS:
        encodingName = WindowsPlatform.getEncodingName(encodingID)
    else:
        encodingName = f"Encoding {encodingID}"

    return encodingName

class UnicodePlatform:
    ENCODING_ID_UNICODE_1_0 = 0
    ENCODING_ID_UNICODE_1_1 = 1
    ENCODING_ID_ISO_10646 = 2
    ENCODING_ID_UNICODE_2_0_BMP_ONLY = 3
    ENCODING_ID_UNICODE_2_0_FULL = 4
    ENCODING_ID_UNICODE_VARIATION_SEQUENCES = 5
    ENCODING_ID_UNICODE_FULL = 6

    encodingNames = {
        ENCODING_ID_UNICODE_1_0: "Unicode 1.0",
        ENCODING_ID_UNICODE_1_1: "Unicode 1.1",
        ENCODING_ID_ISO_10646: "ISO 10646",
        ENCODING_ID_UNICODE_2_0_BMP_ONLY: "Unicode BMP",
        ENCODING_ID_UNICODE_2_0_FULL: "Unicode",
        ENCODING_ID_UNICODE_VARIATION_SEQUENCES: "Unicode Variation Sequences",
        ENCODING_ID_UNICODE_FULL: "Unicode UCS4"
    }

    @classmethod
    def getEncodingName(cls, encodingID):
        encodingName = cls.encodingNames.get(encodingID)

        return encodingName if encodingName is not None else f"Encoding {encodingID}"

class MacintoshPlatform:
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

    encodingNames = {
        ENCODING_ID_ROMAN: "Roman",
        ENCODING_ID_JAPANESE: "Japanese",
        ENCODING_ID_CHINESE_TRADITIONAL: "Chinese (Traditional)",
        ENCODING_ID_KOREAN: "Korean",
        ENCODING_ID_ARABIC: "Arabic",
        ENCODING_ID_HEBREW: "Hebrew",
        ENCODING_ID_GREEK: "Greek",
        ENCODING_ID_RUSSIAN: "Russian",
        ENCODING_ID_RSYMBOL: "RSymbol",
        ENCODING_ID_DEVANAGARI: "Devanagari",
        ENCODING_ID_GURMUKHI: "Gurmukhi",
        ENCODING_ID_GUJARATI: "Gujarati",
        ENCODING_ID_ORIYA: "Oriya",
        ENCODING_ID_BENGALI: "Bengali",
        ENCODING_ID_TAMIL: "Tamil",
        ENCODING_ID_TELEGU: "Telegu",
        ENCODING_ID_KANNADA: "Kannada",
        ENCODING_ID_MALAYALAM: "Malayalam",
        ENCODING_ID_SINHALESE: "Sinhalese",
        ENCODING_ID_BURMESE: "Burmese",
        ENCODING_ID_KHMER: "Khmer",
        ENCODING_ID_THAI: "Thai",
        ENCODING_ID_LAO: "Lao",
        ENCODING_ID_GEORGIAN: "Georgian",
        ENCODING_ID_ARMENIAN: "Armenian",
        ENCODING_ID_CHINESE_SIMPLIFIED: "Chinese (Simplified)",
        ENCODING_ID_TIBETAN: "Tibetan",
        ENCODING_ID_MONGOLIAN: "Mongolian",
        ENCODING_ID_GEEZ: "Geez",
        ENCODING_ID_SLAVIC: "Slavic",
        ENCODING_ID_VIETNAMESE: "Vietnamese",
        ENCODING_ID_SINDHI: "Sindhi"
    }

    @classmethod
    def getEncodingName(cls, encodingID):
        encodingName = cls.encodingNames.get(encodingID)

        return encodingName if encodingName is not None else f"Encoding {encodingID}"

class WindowsPlatform:
    ENCODING_ID_SYMBOL = 0
    ENCODING_ID_UNICODE_BMP = 1
    ENCODING_ID_SHIFT_JIS = 2
    ENCODING_ID_PRC = 3
    ENCODING_ID_BIG_5 = 4
    ENCODING_ID_WANSUNG = 5
    ENCODING_ID_JOHAB = 6
    # 7 - 9 reserved
    ENCODING_ID_UNICODE_UCS4 = 10

    encodingNames = {
        ENCODING_ID_SYMBOL: "Symbol",
        ENCODING_ID_UNICODE_BMP: "Unicode BMP",
        ENCODING_ID_SHIFT_JIS: "Shift JIS",
        ENCODING_ID_PRC: "PRC",
        ENCODING_ID_BIG_5: "Big 5",
        ENCODING_ID_WANSUNG: "Wansung",
        ENCODING_ID_JOHAB: "Johab",
        ENCODING_ID_UNICODE_UCS4: "Unicode UCS4"
    }

    @classmethod
    def getEncodingName(cls, encodingID):
        encodingName = cls.encodingNames.get(encodingID)
        
        return encodingName if encodingName is not None else f"Encoding {encodingID}"
