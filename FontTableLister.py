'''
Created on Jan 16, 2020

@author: emader
'''

import struct
import sys

fontDirectoryHeaderFormat = ">IHHHH"
fontDirectoryEntryFormat  = ">4sIII"

fontDirectoryHeaderLength = struct.calcsize(fontDirectoryHeaderFormat)
fontDirectoryEntryLength  = struct.calcsize(fontDirectoryEntryFormat)

for fontFileName in sys.argv[1:] :
    fontFile = open(fontFileName, "rb")
    
    fontName = fontFileName.split("/")[-1:][0] # not sure why I need the [0]...
    
    directoryHeaderData = fontFile.read(fontDirectoryHeaderLength)
    scalerType, numTables, searchRange, entrySelector, rangeShift = struct.unpack(fontDirectoryHeaderFormat, directoryHeaderData)
    
    print(fontName + " contains " + str(numTables) + " tables.")
    
    for entry in range(numTables) :
        directoryEntryData = fontFile.read(fontDirectoryEntryLength)
        tag, checksum, offset, length = struct.unpack(fontDirectoryEntryFormat, directoryEntryData)
        print(str(tag) + " " + str(length))
    
    print()
    