'''
Created on Feb 03, 2020

@author: emader
'''

import struct

import utility
import FontTable

# typedef struct {
#     UInt16 platformID;
#     UInt16 encodingID;
#     UInt16 languageID;
#     UInt16 nameID;
#     UInt16 length;
#     UInt16 offset;
# } FFLRawNameRecord;

class NameRecord:
    NAME_ID_COMYRIGHT_NOTICE = 0
    NAME_ID_FONT_FAMILY = 1
    NAME_ID_FONT_SUBFAMILY = 2
    NAME_ID_UNIQUE_FONT_IDENTIFIER = 3
    NAME_ID_FULL_NAME = 4
    NAME_ID_VERSION_STRING = 5
    NAME_ID_POSTSCRIPT_NAME = 6
    NAME_ID_TRADEMARK = 7
    NAME_ID_MANUFACTURER = 8
    NAME_ID_DESIGNER = 9
    NAME_ID_DESCRIPTION = 10
    NAME_ID_VENDOR_URL = 11
    NAME_ID_DESIGNER_URL = 12
    NAME_ID_LICENSE_DESCRIPTION = 13
    NAME_ID_LICENSE_URL = 14
    # nameID 15 reserved
    NAME_ID_TYPOGRAPHIC_FAMILY = 16
    NAME_ID_TYPOGRAPHIC_SUBFAMILY = 17
    NAME_ID_COMPATIBLE_FULL_NAME = 18
    NAME_ID_SAMPLE_TEXT = 19

    def __init__(self, platformID, encodingID, languageID, nameID, length, offset, stringBytes):
        self.platformID = platformID
        self.encodingID = encodingID
        self.languageID = languageID
        self.nameID = nameID
        self.length = length
        self.offset = offset
        self.stringBytes = stringBytes

        self.nameIDNames = {
            self.NAME_ID_COMYRIGHT_NOTICE : "Copyright",
            self.NAME_ID_FONT_FAMILY : "Family",
            self.NAME_ID_FONT_SUBFAMILY : "Subfamily",
            self. NAME_ID_UNIQUE_FONT_IDENTIFIER : "Unique Name",
            self.NAME_ID_FULL_NAME : "Full Name",
            self.NAME_ID_VERSION_STRING : "Version",
            self.NAME_ID_POSTSCRIPT_NAME : "Postscript Name",
            self.NAME_ID_TRADEMARK : "Trademark",
            self.NAME_ID_MANUFACTURER : "Manufacturer",
            self.NAME_ID_DESIGNER : "Designer",
            self.NAME_ID_DESCRIPTION : "Description",
            self.NAME_ID_VENDOR_URL : "Vendor URL",
            self.NAME_ID_DESIGNER_URL : "Designer URL",
            self.NAME_ID_LICENSE_DESCRIPTION : "License",
            self.NAME_ID_LICENSE_URL : "License URL",
            self.NAME_ID_TYPOGRAPHIC_FAMILY : "Typographic Family",
            self.NAME_ID_TYPOGRAPHIC_SUBFAMILY : "Typographic Subfamily",
            self.NAME_ID_COMPATIBLE_FULL_NAME : "Menu Name",
            self.NAME_ID_SAMPLE_TEXT : "Sample Text"
        }

        self.encodingNames = {}
        self.languageNames = {}


    def platformName(self):
        return f"Platform {self.platformID:d}"

    def encodingName(self):
        name = self.encodingNames.get(self.encodingID)

        if name is not None:
            return name

        return f"Encoding {self.encodingID:d}"

    def languageName(self):
        name = self.languageNames.get(self.languageID)

        if name is not None:
            return name

        return f"Language {self.languageID:d}"

    def nameIDName(self):
        idName = self.nameIDNames.get(self.nameID)

        if idName is not None:
            return idName

        return f"Name {self.nameID:d}"

    def getStringEncoding(self):
        return None

    def getString(self):
        encoding = self.getStringEncoding()

        if encoding is not None:
            startByte = self.offset
            endByte = startByte + self.length

            return self.stringBytes[startByte:endByte].decode(encoding)

        return "(can't decode this string)"