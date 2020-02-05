'''
Created on Feb 03, 2020

@author: emader
'''

import struct

import NameRecord
import UnicodeNameRecord
import MacintoshNameRecord
import WindowsNameRecord

PLATFORM_ID_UNICODE = 0
PLATFORM_ID_MACINTOSH = 1
# platform ID 2 is deprecated
PLATFORM_ID_WINDOWS = 3
PLATFORM_ID_CUSTOM = 4

NAME_RECORD_FORMAT = ">HHHHHH"
NAME_RECORD_LENGTH = struct.calcsize(NAME_RECORD_FORMAT)

def nameRecordFactory(rawNameRecord, stringBytes):
    platformID, encodingID, languageID, nameID, length, offset = struct.unpack(
        NAME_RECORD_FORMAT, rawNameRecord)

    if platformID == PLATFORM_ID_UNICODE:
        return UnicodeNameRecord.UnicodeNameRecord(platformID, encodingID, languageID, nameID, length, offset, stringBytes)
    elif platformID == PLATFORM_ID_MACINTOSH:
        return MacintoshNameRecord.MacintoshNameRecord(platformID, encodingID, languageID, nameID, length, offset, stringBytes)
    elif platformID == PLATFORM_ID_WINDOWS:
        return WindowsNameRecord.WindowsNameRecord(platformID, encodingID, languageID, nameID, length, offset, stringBytes)
    else:
        return NameRecord.NameRecord(platformID, encodingID, languageID, nameID, length, offset, stringBytes)