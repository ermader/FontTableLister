'''
Created on Feb 03, 2020

@author: emader
'''

import struct

from PlatformAndEncoding import PLATFORM_ID_UNICODE, PLATFORM_ID_MACINTOSH, PLATFORM_ID_WINDOWS

from NameTable import UnicodeNameRecord, MacintoshNameRecord, NameRecord, WindowsNameRecord

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