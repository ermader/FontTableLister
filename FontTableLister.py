'''
Created on Jan 16, 2020

@author: emader
'''

import struct
import sys

def stringFromTag(tag):
    # There's *got* to be a better way to do this...
    return "%c%c%c%c" % (tag[0], tag[1], tag[2], tag[3])

fontDirectoryHeaderFormat = ">IHHHH"
fontDirectoryEntryFormat  = ">4sIII"

fontDirectoryHeaderLength = struct.calcsize(fontDirectoryHeaderFormat)
fontDirectoryEntryLength  = struct.calcsize(fontDirectoryEntryFormat)

for fontFileName in sys.argv[1:] :
    fontFile = open(fontFileName, "rb")
    
    fontName = fontFileName.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string
    
    directoryHeaderData = fontFile.read(fontDirectoryHeaderLength)
    scalerType, numTables, searchRange, entrySelector, rangeShift = struct.unpack(fontDirectoryHeaderFormat, directoryHeaderData)
    
    print(fontName + " contains " + str(numTables) + " tables.")
    
    for entry in range(numTables) :
        directoryEntryData = fontFile.read(fontDirectoryEntryLength)
        tag, checksum, offset, length = struct.unpack(fontDirectoryEntryFormat, directoryEntryData)
        
        print("'" + stringFromTag(tag) + "'" + " " + str(length))
    
    print()
    