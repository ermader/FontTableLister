'''
Created on Jan 16, 2020

@author: emader
'''

import sys
import argparse

import font

parser = argparse.ArgumentParser()

parser.add_argument("file", type=argparse.FileType("rb"))
parser.add_argument("-i", "--index", type=int, default=0)
parser.add_argument("-d", "--dump", action="append")
parser.add_argument("-f", "--format", action="append")
parser.add_argument("-l", "--list", action="store_true")

arguments = parser.parse_args(sys.argv[1:])

fileObject = arguments.file
fileName = fileObject.name.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string

print("{:s}:".format(fileName))
fontFile = font.File(fileObject)

fontIndex = min(len(fontFile.fonts) - 1, arguments.index)
fontObject = fontFile.fonts[fontIndex]

if arguments.list:
    print("  Font {:d} contains {:d} tables:".format(fontIndex, len(fontObject.tables)))
    
    for table in fontObject.tables:
        print("    '{:s}' {:10,d}".format(table.tag, table.length))
    
    print()

for tableTag in arguments.dump:
    print("  Hex dump of '{:s}' table:".format(tableTag))
    table = fontObject.getTable(tableTag)
    table.dump()
    print()
    
for tableTag in arguments.format:
    print("  Formatted '{:s}' table:".format(tableTag))
    table = fontObject.getTable(tableTag)
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
    