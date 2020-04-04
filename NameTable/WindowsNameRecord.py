'''
Created on Feb 03, 2020

@author: emader
'''

from PlatformAndEncoding import WindowsPlatform
from NameTable import NameRecord


class WindowsNameRecord(NameRecord.NameRecord):
    # There are a *lot* more of these
    # These are just the ones I have encountered, or expect to encounter
    LANGUAGE_ID_ARABIC_ALGERIA = 0x1401
    LANGUAGE_ID_ARABIC_BAHRAIN = 0x3C01
    LANGUAGE_ID_ARABIC_EGYPT = 0x0C01
    LANGUAGE_ID_ARABIC_IRAQ = 0x0801
    LANGUAGE_ID_ARABIC_JORDAN = 0x2C01
    LANGUAGE_ID_ARABIC_KUWAIT = 0x3401
    LANGUAGE_ID_ARABIC_LEBANON = 0x3001
    LANGUAGE_ID_ARABIC_LIBYA = 0x1001
    LANGUAGE_ID_ARABIC_MOROCCO = 0x1801
    LANGUAGE_ID_ARABIC_OMAN = 0x2001
    LANGUAGE_ID_ARABIC_QATAR = 0x4001
    LANGUAGE_ID_ARABIC_SAUDIA_ARABIA = 0x0401
    LANGUAGE_ID_ARABIC_SYRIA = 0x2801
    LANGUAGE_ID_ARABIC_TUNISIA = 0x1C01
    LANGUAGE_ID_ARABIC_UAE = 0x3801
    LANGUAGE_ID_ARABIC_YEMEN = 0x2401
    LANGUAGE_ID_BASQUE = 0x042D
    LANGUAGE_ID_CATALAN = 0x0403
    LANGUAGE_ID_CHINESE_HONG_KONG = 0x0C04
    LANGUAGE_ID_CHINESE_MACAO = 0x1404
    LANGUAGE_ID_CHINESE_PRC = 0x0804
    LANGUAGE_ID_CHINESE_SINGAPORE = 0x1004
    LANGUAGE_ID_CHINESE_TAIWAN = 0x0404
    LANGUAGE_ID_CROATIAN_CORATIA = 0x041A
    LANGUAGE_ID_CROATIAN_LATIN = 0x101A
    LANGUAGE_ID_CZECH = 0x0405
    LANGUAGE_ID_DANISH_DENMARK = 0x0406
    LANGUAGE_ID_DUTCH_BELGUIM = 0x0813
    LANGUAGE_ID_DUTCH_NETHERLANDS = 0x0413
    LANGUAGE_ID_ENGLISH_UK = 0x0809
    LANGUAGE_ID_ENGLISH_US = 0x0409
    LANGUAGE_ID_FINNISH = 0x040B
    LANGUAGE_ID_FRENCH_CANADA = 0x0C0C
    LANGUAGE_ID_FRENCH_FRANCE = 0x040C
    LANGUAGE_ID_GERMAN_GERMANY = 0x0407
    LANGUAGE_ID_GREEK = 0x0408
    LANGUAGE_ID_HEBREW = 0x040D
    LANGUAGE_ID_HUNGARIAN = 0x040E
    LANGUAGE_ID_ICELANDIC = 0x040F
    LANGUAGE_ID_ITALIAN_ITALY = 0x0410
    LANGUAGE_ID_JAPANESE = 0x0411
    LANGUAGE_ID_KOREAN = 0x0412
    LANGUAGE_ID_NORWEGIAN_BOKMAL = 0x0414
    LANGUAGE_ID_NORWEGIAN_NYNORSK = 0x0814
    LANGUAGE_ID_POLISH = 0x0415
    LANGUAGE_ID_PORTUGUESE_BRAZIL = 0x0416
    LANGUAGE_ID_PORTUGUESE_PORTUGAL = 0x0816
    LANGUAGE_ID_ROMANIAN = 0x0418
    LANGUAGE_ID_RUSSIAN = 0x0419
    LANGUAGE_ID_SLOVAK = 0x041B
    LANGUAGE_ID_SLOVENIAN = 0x0424
    LANGUAGE_ID_SPANISH_MEXICO = 0x080A
    LANGUAGE_ID_SPANISH_PANAMA = 0x180A
    LANGUAGE_ID_SPANISH_TRADITIONAL_SORT = 0x040A
    LANGUAGE_ID_SPANISH_MODERN_SORT = 0x0C0A
    LANGUAGE_ID_SWEDISH_SWEDEN = 0x041D
    LANGUAGE_ID_THAI = 0x041E
    LANGUAGE_ID_TURKISH = 0x041F
    LANGUAGE_ID_VIETNAMESE = 0x042A

    def __init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes):
        NameRecord.NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes)

        self.encodingNames = {
            WindowsPlatform.ENCODING_ID_SYMBOL : "Symbol",
            WindowsPlatform.ENCODING_ID_UNICODE_BMP : "Unicode BMP",
            WindowsPlatform.ENCODING_ID_SHIFT_JIS : "Shift JIS",
            WindowsPlatform.ENCODING_ID_PRC : "PRC",
            WindowsPlatform.ENCODING_ID_BIG_5 : "Big 5",
            WindowsPlatform.ENCODING_ID_WANSUNG : "Wansung",
            WindowsPlatform.ENCODING_ID_JOHAB : "Johab",
            WindowsPlatform.ENCODING_ID_UNICODE_UCS4 : "Unicode UCS4"
        }

        self.stringEncodings = {
            WindowsPlatform.ENCODING_ID_SYMBOL: "utf_16_be", # really?
            WindowsPlatform.ENCODING_ID_UNICODE_BMP: "utf_16_be",
            WindowsPlatform.ENCODING_ID_SHIFT_JIS: "Shift_jis",
            WindowsPlatform.ENCODING_ID_PRC: "gb2312",
            WindowsPlatform.ENCODING_ID_BIG_5: "big5",
            WindowsPlatform.ENCODING_ID_WANSUNG: "cp949",
            WindowsPlatform.ENCODING_ID_JOHAB: "johab",
            WindowsPlatform.ENCODING_ID_UNICODE_UCS4: "utf_32_be"
        }

        self.languageNames = {
            self.LANGUAGE_ID_ARABIC_ALGERIA : "Arabic (Algeria)",
            self.LANGUAGE_ID_ARABIC_BAHRAIN : "Arabic (Bahrain)",
            self.LANGUAGE_ID_ARABIC_EGYPT : "Arabic (Egypt)",
            self.LANGUAGE_ID_ARABIC_IRAQ : "Arabic (Iraq)",
            self.LANGUAGE_ID_ARABIC_JORDAN : "Arabic (Jordan)",
            self.LANGUAGE_ID_ARABIC_KUWAIT : "Arabic (Kuwait)",
            self.LANGUAGE_ID_ARABIC_LEBANON : "Arabic (Lebanon)",
            self.LANGUAGE_ID_ARABIC_LIBYA : "Arabic (Libya)",
            self.LANGUAGE_ID_ARABIC_MOROCCO : "Arabic (Morocco)",
            self.LANGUAGE_ID_ARABIC_OMAN : "Arabic (Oman)",
            self.LANGUAGE_ID_ARABIC_QATAR : "Arabic (Qatar)",
            self.LANGUAGE_ID_ARABIC_SAUDIA_ARABIA : "Arabic (Saudi Arabia)",
            self.LANGUAGE_ID_ARABIC_SYRIA : "Arabic (Syria)",
            self.LANGUAGE_ID_ARABIC_TUNISIA : "Arabic (Tunisia)",
            self.LANGUAGE_ID_ARABIC_UAE : "Arabic (UAE)",
            self.LANGUAGE_ID_ARABIC_YEMEN : "Arabic (Yemen)",
            self.LANGUAGE_ID_BASQUE : "Basque",
            self.LANGUAGE_ID_CATALAN : "Catalan",
            self.LANGUAGE_ID_CHINESE_HONG_KONG : "Chinese (Hong Kong)",
            self.LANGUAGE_ID_CHINESE_MACAO : "Chinese (Macao)",
            self.LANGUAGE_ID_CHINESE_PRC : "Chinese (PRC)",
            self.LANGUAGE_ID_CHINESE_TAIWAN : "Chinese (Taiwan)",
            self.LANGUAGE_ID_CROATIAN_CORATIA : "Croatian",
            self.LANGUAGE_ID_CROATIAN_LATIN : "Croatian (Latin)",
            self.LANGUAGE_ID_CZECH : "Czech",
            self.LANGUAGE_ID_DANISH_DENMARK : "Danish",
            self.LANGUAGE_ID_DUTCH_BELGUIM : "Dutch (Belguim)",
            self.LANGUAGE_ID_DUTCH_NETHERLANDS : "Dutch",
            self.LANGUAGE_ID_ENGLISH_UK : "English (UK)",
            self.LANGUAGE_ID_ENGLISH_US : "English (US)",
            self.LANGUAGE_ID_FINNISH : "Finnish",
            self.LANGUAGE_ID_FRENCH_CANADA : "French (Canada}",
            self.LANGUAGE_ID_FRENCH_FRANCE : "French",
            self.LANGUAGE_ID_GERMAN_GERMANY : "German",
            self.LANGUAGE_ID_GREEK : "Greek",
            self.LANGUAGE_ID_HEBREW : "Hebrew",
            self.LANGUAGE_ID_HUNGARIAN : "Hungarian",
            self.LANGUAGE_ID_ICELANDIC : "Icelandic",
            self.LANGUAGE_ID_ITALIAN_ITALY : "Italian",
            self.LANGUAGE_ID_JAPANESE : "Japanese",
            self.LANGUAGE_ID_KOREAN : "Korean",
            self.LANGUAGE_ID_NORWEGIAN_BOKMAL : "Norwegian (Bokmal)",
            self.LANGUAGE_ID_NORWEGIAN_NYNORSK : "Norwegian (Nynorsk)",
            self.LANGUAGE_ID_POLISH : "Polish",
            self.LANGUAGE_ID_PORTUGUESE_BRAZIL : "Portuguese (Brazil)",
            self.LANGUAGE_ID_PORTUGUESE_PORTUGAL : "Portuguese (Portugal)",
            self.LANGUAGE_ID_ROMANIAN : "Romanian",
            self.LANGUAGE_ID_RUSSIAN : "Russian",
            self.LANGUAGE_ID_SLOVAK : "Slovak",
            self.LANGUAGE_ID_SLOVENIAN : "Slovenian",
            self.LANGUAGE_ID_SPANISH_MEXICO : "Spanish (Mexico)",
            self.LANGUAGE_ID_SPANISH_PANAMA : "Spanish (Panama)",
            self.LANGUAGE_ID_SPANISH_TRADITIONAL_SORT : "Spanish (Traditional)",
            self.LANGUAGE_ID_SPANISH_MODERN_SORT : "Spanish (Modern)",
            self.LANGUAGE_ID_SWEDISH_SWEDEN : "Swedish",
            self.LANGUAGE_ID_THAI : "Thai",
            self.LANGUAGE_ID_TURKISH : "Turkish",
            self.LANGUAGE_ID_VIETNAMESE : "Vietnamese"
        }

    def platformName(self):
        return "Windows"

    def getStringEncoding(self):
        return self.stringEncodings.get(self.encodingID)
