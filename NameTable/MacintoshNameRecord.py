'''
Created on Feb 03, 2020

@author: emader
'''

from PlatformAndEncoding import PLATFORM_ID_MACINTOSH, MacintoshPlatform, getPLatformName
from NameTable import NameRecord


class MacintoshNameRecord(NameRecord.NameRecord):
    LANGUAGE_ID_ENGLISH = 0
    LANGUAGE_ID_FRENCH = 1
    LANGUAGE_ID_GERMAN = 2
    LANGUAGE_ID_ITALIAN = 3
    LANGUAGE_ID_DUCTH = 4
    LANGUAGE_ID_SWEDISH = 5
    LANGUAGE_ID_SPANISH = 6
    LANGUAGE_ID_DANISH = 7
    LANGUAGE_ID_PORTUGUESE = 8
    LANGUAGE_ID_NORWEGIAN = 9
    LANGUAGE_ID_HEBREW = 10
    LANGUAGE_ID_JAPANESE = 11
    LANGUAGE_ID_ARABIC = 12
    LANGUAGE_ID_FINNISH = 13
    LANGUAGE_ID_GREEK = 14
    LANGUAGE_ID_ICELANDIC = 15
    LANGUAGE_ID_MALTESE = 16
    LANGUAGE_ID_TURKISH = 17
    LANGUAGE_ID_CROATIAN = 18
    LANGUAGE_ID_CHINESE_TRADITIONAL = 19
    LANGUAGE_ID_URDU = 20
    LANGUAGE_ID_HINDI = 21
    LANGUAGE_ID_THAI = 22
    LANGUAGE_ID_KOREAN = 23
    LANGUAGE_ID_LITHUANIAN = 24
    LANGUAGE_ID_POLISH = 25
    LANGUAGE_ID_HUNGARIAN = 26
    LANGUAGE_ID_ESTONIAN = 27
    LANGUAGE_ID_LATVIAN = 28
    LANGUAGE_ID_SAMI = 29
    LANGUAGE_ID_FAROESE = 30
    LANGUAGE_ID_FARSI = 31
    LANGUAGE_ID_RUSSIAN = 32
    LANGUAGE_ID_CHINESE_SIMPLIFIED = 33
    LANGUAGE_ID_FLEMISH = 34
    LANGUAGE_ID_IRISH_GAELIC = 35
    LANGUAGE_ID_ALBANIAN = 36
    LANGUAGE_ID_ROMANIAN = 37
    LANGUAGE_ID_CZECH = 38
    LANGUAGE_ID_SLOVAK = 39
    LANGUAGE_ID_SLOVENIAN = 40
    LANGUAGE_ID_YIDDISH = 41
    LANGUAGE_ID_SERBIAN = 42
    LANGUAGE_ID_MACEDONIAN = 43
    LANGUAGE_ID_BULGARIAN = 44
    LANGUAGE_ID_UKRANIAN = 45
    LANGUAGE_ID_BYELORUSSIAN = 46
    LANGUAGE_ID_CATALAN = 130
    # and a bunch more...

    def __init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes):
        NameRecord.NameRecord.__init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes)

        #
        # Many of these don't seem to have Python codecs...
        #
        self.stringEncodings = {
            MacintoshPlatform.ENCODING_ID_JAPANESE: "shift_jis", # MacJapanese is actually a superset of SHIFT-JIS
            # MacintoshPlatform.ENCODING_ID_CHINESE_TRADITIONAL: "Chinese (Traditional)",
            MacintoshPlatform.ENCODING_ID_KOREAN: "euc_kr", # MacKoran is actually a superset of EUC-KR
            # MacintoshPlatform.ENCODING_ID_ARABIC: "Arabic",
            # MacintoshPlatform.ENCODING_ID_HEBREW: "Hebrew",
            MacintoshPlatform.ENCODING_ID_GREEK: "mac_greek",
            MacintoshPlatform.ENCODING_ID_RUSSIAN: "mac_cyrillic",
            MacintoshPlatform.ENCODING_ID_RSYMBOL: "koi8_r", # not sure about this...
            # MacintoshPlatform.ENCODING_ID_DEVANAGARI: "Devanagari",
            # MacintoshPlatform.ENCODING_ID_GURMUKHI: "Gurmukhi",
            # MacintoshPlatform.ENCODING_ID_GUJARATI: "Gujarati",
            # MacintoshPlatform.ENCODING_ID_ORIYA: "Oriya",
            # MacintoshPlatform.ENCODING_ID_BENGALI: "Bengali",
            # MacintoshPlatform.ENCODING_ID_TAMIL: "Tamil",
            # MacintoshPlatform.ENCODING_ID_TELEGU: "Telegu",
            # MacintoshPlatform.ENCODING_ID_KANNADA: "Kannada",
            # MacintoshPlatform.ENCODING_ID_MALAYALAM: "Malayalam",
            # MacintoshPlatform.ENCODING_ID_SINHALESE: "Sinhalese",
            # MacintoshPlatform.ENCODING_ID_BURMESE: "Burmese",
            # MacintoshPlatform.ENCODING_ID_KHMER: "Khmer",
            # MacintoshPlatform.ENCODING_ID_THAI: "Thai",
            # MacintoshPlatform.ENCODING_ID_LAO: "Lao",
            # MacintoshPlatform.ENCODING_ID_GEORGIAN: "Georgian",
            # MacintoshPlatform.ENCODING_ID_ARMENIAN: "Armenian",
            # MacintoshPlatform.ENCODING_ID_CHINESE_SIMPLIFIED: "Chinese (Simplified)",
            # MacintoshPlatform.ENCODING_ID_TIBETAN: "Tibetan",
            # MacintoshPlatform.ENCODING_ID_MONGOLIAN: "Mongolian",
            # MacintoshPlatform.ENCODING_ID_GEEZ: "Geez",
            MacintoshPlatform.ENCODING_ID_SLAVIC: "mac_latin2",
            # MacintoshPlatform.ENCODING_ID_VIETNAMESE: "Vietnamese",
            # MacintoshPlatform.ENCODING_ID_SINDHI: "Sindhi"
        }

        self.languageNames = {
            self.LANGUAGE_ID_ENGLISH : "English",
            self.LANGUAGE_ID_FRENCH : "French",
            self.LANGUAGE_ID_GERMAN : "German",
            self.LANGUAGE_ID_ITALIAN : "Italian",
            self.LANGUAGE_ID_DUCTH : "Dutch",
            self.LANGUAGE_ID_SWEDISH : "Swedish",
            self.LANGUAGE_ID_SPANISH : "Spanish",
            self.LANGUAGE_ID_DANISH : "Danish",
            self.LANGUAGE_ID_PORTUGUESE : "Portuguese",
            self.LANGUAGE_ID_NORWEGIAN : "Norwegian",
            self.LANGUAGE_ID_HEBREW : "Hebrew",
            self.LANGUAGE_ID_JAPANESE : "Japanese",
            self.LANGUAGE_ID_ARABIC : "Arabic",
            self.LANGUAGE_ID_FINNISH : "Finish",
            self.LANGUAGE_ID_GREEK : "Greek",
            self.LANGUAGE_ID_ICELANDIC : "Icelandic",
            self.LANGUAGE_ID_MALTESE : "Maltese",
            self.LANGUAGE_ID_TURKISH : "Turkish",
            self.LANGUAGE_ID_CROATIAN : "Croation",
            self.LANGUAGE_ID_CHINESE_TRADITIONAL : "Chinese (Traditional)",
            self.LANGUAGE_ID_URDU : "Urdu",
            self.LANGUAGE_ID_HINDI : "Hindi",
            self.LANGUAGE_ID_THAI : "Thai",
            self.LANGUAGE_ID_KOREAN : "Korean",
            self.LANGUAGE_ID_LITHUANIAN : "Lithuanian",
            self.LANGUAGE_ID_POLISH : "Polish",
            self.LANGUAGE_ID_HUNGARIAN : "Hungarian",
            self.LANGUAGE_ID_ESTONIAN : "Estonian",
            self.LANGUAGE_ID_LATVIAN : "Latvian",
            self.LANGUAGE_ID_SAMI : "Sami",
            self.LANGUAGE_ID_FAROESE : "Faroese",
            self.LANGUAGE_ID_FARSI : "Farsi",
            self.LANGUAGE_ID_RUSSIAN : "Russian",
            self.LANGUAGE_ID_CHINESE_SIMPLIFIED : "Chinese (Simplified)",
            self.LANGUAGE_ID_FLEMISH : "Flemish",
            self.LANGUAGE_ID_IRISH_GAELIC : "Irish Gaelic",
            self.LANGUAGE_ID_ALBANIAN : "Albanian",
            self.LANGUAGE_ID_ROMANIAN : "Romanian",
            self.LANGUAGE_ID_CZECH : "Czech",
            self.LANGUAGE_ID_SLOVAK : "Slovak",
            self.LANGUAGE_ID_SLOVENIAN : "Slovenian",
            self.LANGUAGE_ID_YIDDISH : "Yiddish",
            self.LANGUAGE_ID_SERBIAN : "Serbian",
            self.LANGUAGE_ID_MACEDONIAN : "Macedonian",
            self.LANGUAGE_ID_BULGARIAN : "Bulgarian",
            self.LANGUAGE_ID_UKRANIAN : "Ukkranian",
            self.LANGUAGE_ID_BYELORUSSIAN : "Byelorussian",
            self.LANGUAGE_ID_CATALAN : "Catalan"
        }

        self.languageEncodings = {
            self.LANGUAGE_ID_ENGLISH: "mac_roman",
            self.LANGUAGE_ID_FRENCH: "mac_roman",
            self.LANGUAGE_ID_GERMAN: "mac_roman",
            self.LANGUAGE_ID_ITALIAN: "mac_roman",
            self.LANGUAGE_ID_DUCTH: "mac_roman",
            self.LANGUAGE_ID_SWEDISH: "mac_roman",
            self.LANGUAGE_ID_SPANISH: "mac_roman",
            self.LANGUAGE_ID_DANISH: "mac_roman",
            self.LANGUAGE_ID_PORTUGUESE: "mac_roman",
            self.LANGUAGE_ID_NORWEGIAN: "mac_roman",
            # self.LANGUAGE_ID_HEBREW: "Hebrew",
            # self.LANGUAGE_ID_JAPANESE: "Japanese",
            # self.LANGUAGE_ID_ARABIC: "Arabic",
            self.LANGUAGE_ID_FINNISH: "mac_roman",
            self.LANGUAGE_ID_GREEK: "mac_greek",
            self.LANGUAGE_ID_ICELANDIC: "mac_iceland",
            self.LANGUAGE_ID_MALTESE: "mac_roman",
            self.LANGUAGE_ID_TURKISH: "mac_turkish",
            # self.LANGUAGE_ID_CROATIAN: "Croation",
            # self.LANGUAGE_ID_CHINESE_TRADITIONAL: "Chinese (Traditional)",
            # self.LANGUAGE_ID_URDU: "Urdu",
            # self.LANGUAGE_ID_HINDI: "Hindi",
            # self.LANGUAGE_ID_THAI: "Thai",
            # self.LANGUAGE_ID_KOREAN: "Korean",
            self.LANGUAGE_ID_LITHUANIAN: "mac_latin2",
            self.LANGUAGE_ID_POLISH: "mac_latin2",
            self.LANGUAGE_ID_HUNGARIAN: "mac_latin2",
            self.LANGUAGE_ID_ESTONIAN: "mac_latin2",
            self.LANGUAGE_ID_LATVIAN: "mac_latin2",
            self.LANGUAGE_ID_SAMI: "mac_roman",
            self.LANGUAGE_ID_FAROESE: "mac_roman",
            # self.LANGUAGE_ID_FARSI: "Farsi",
            self.LANGUAGE_ID_RUSSIAN: "mac_cyrillic",
            self.LANGUAGE_ID_CHINESE_SIMPLIFIED: "Chinese (Simplified)",
            self.LANGUAGE_ID_FLEMISH: "mac_roman",
            self.LANGUAGE_ID_IRISH_GAELIC: "mac_roman Gaelic",
            self.LANGUAGE_ID_ALBANIAN: "mac_latin2",
            # self.LANGUAGE_ID_ROMANIAN: "Romanian",
            self.LANGUAGE_ID_CZECH: "mac_latin2",
            self.LANGUAGE_ID_SLOVAK: "mac_latin2",
            self.LANGUAGE_ID_SLOVENIAN: "mac_latin2",
            self.LANGUAGE_ID_YIDDISH: "mac_roman",
            self.LANGUAGE_ID_SERBIAN: "mac_cyrillic",
            self.LANGUAGE_ID_MACEDONIAN: "mac_cyrillic",
            self.LANGUAGE_ID_BULGARIAN: "mac_cyrillic",
            self.LANGUAGE_ID_UKRANIAN: "mac_cyrillic",
            self.LANGUAGE_ID_BYELORUSSIAN: "mac_cyrillic",
            self.LANGUAGE_ID_CATALAN: "mac_roman"
        }

    def platformName(self):
        return getPLatformName(PLATFORM_ID_MACINTOSH)

    def encodingName(self):
        return MacintoshPlatform.getEncodingName(self.encodingID)

    def getStringEncoding(self):
        if self.encodingID == MacintoshPlatform.ENCODING_ID_ROMAN:
            encoding = self.languageEncodings.get(self.languageID)
        else:
            encoding = self.stringEncodings.get(self.encodingID)

        return encoding