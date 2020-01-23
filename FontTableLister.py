'''
Created on Jan 16, 2020

@author: emader
'''

import sys
import os
import argparse

import font

parser = argparse.ArgumentParser(prog="FontTableLister")

parser.add_argument("file", type=argparse.FileType("rb"), help="the font file to examine")
parser.add_argument("-i", "--index", type=int, default=0, metavar="font_index", help="the subfont to examine. (default = %(default)s)")
parser.add_argument("-d", "--dump", action="append", metavar="table", help="hex dump the table")
parser.add_argument("-f", "--format", action="append", metavar="table", help="show the formatted table")
parser.add_argument("-l", "--list", action="store_true", help="list all the tables in the font")

arguments = parser.parse_args(sys.argv[1:])

fileObject = arguments.file
fileName = fileObject.name.split(os.sep)[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string

print("{:s}:".format(fileName))
fontFile = font.File(fileObject)

fontIndex = min(len(fontFile.fonts) - 1, arguments.index)
fontObject = fontFile.fonts[fontIndex]

if arguments.list:
    print("  Font {:d} contains {:d} tables:".format(fontIndex, len(fontObject.tables)))
    
    for table in fontObject.tables:
        print("    '{:s}' 0x{:08X} 0x{:08X} {:10,d}".format(table.tag, table.checksum, table.offset, table.length))
    
    print()

if arguments.dump:
    for tableTag in arguments.dump:
        print("  Hex dump of '{:s}' table:".format(tableTag))
        table = fontObject.getTable(tableTag)
        if table:
            table.dump()
            
        print()

if arguments.format:    
    for tableTag in arguments.format:
        print("  Formatted '{:s}' table:".format(tableTag))
        table = fontObject.getTable(tableTag)
        if table:
            table.format()
            
        print()
    
# for fontFileName in sys.argv[1:] :
#     fontFile = font.File(fontFileName)
#     
#     fontName = fontFileName.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string
#     
#     print("{:s} contains {:d} fonts.".format(fontName, len(fontFile.fonts)))
#     
#     fontNumber = 1
#     for fontObject in fontFile.fonts:
#         print("    Font {:d} contains {:d} tables.".format(fontNumber, len(fontObject.tables)))
#         for table in fontObject.tables :
#             print("    '{:s}' {:10,d}".format(table.tag, table.length))
#             if table.tag == 'head':
#                 table.format()
#             elif table.tag == 'hhea':
#                 table.dump()
#             elif table.tag == 'cmap':
#                 table.format()
#         
#         print()
#         fontNumber += 1
#     print()
    