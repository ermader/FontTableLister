'''
Created on Jan 16, 2020

@author: emader
'''

import sys
import os
import argparse

import FontFile

parser = argparse.ArgumentParser(prog="FontTableLister")

parser.add_argument("file", type=argparse.FileType("rb"), help="the font file to examine")
parser.add_argument("-c", "--contents", action="store_true", help="List all fonts in the file")
parser.add_argument("-i", "--index", type=int, default=0, metavar="font_index", help="the subfont to examine. (default = %(default)s)")
parser.add_argument("-p", "--psname", metavar="postscript_name", help="postscript name of the font to examine")
parser.add_argument("-d", "--dump", action="append", metavar="table", help="hex dump the table")
parser.add_argument("-f", "--format", action="append", metavar="table", help="show the formatted table")
parser.add_argument("-l", "--list", action="store_true", help="list all the tables in the font")

arguments = parser.parse_args(sys.argv[1:])

fileObject = arguments.file
fileName = fileObject.name.split(os.sep)[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string

fontFile = FontFile.File(fileObject)

if arguments.contents:
    print(f"  Fonts in {fileName}:")
    index = 0
    for fontObject in fontFile.fonts:
        print(f"    {index:2d}: {fontObject.getPostscriptName()}")
        index += 1

    print()

fontIndex = None
if arguments.psname:
    index = 0
    for fontObject in fontFile.fonts:
        if fontObject.getPostscriptName() == arguments.psname:
            fontIndex = index
            break
        index += 1

    if fontIndex is None:
        print(f"  {fileName} does not contain a font named {arguments.psname}")

if fontIndex is None:
    fontIndex = min(len(fontFile.fonts) - 1, arguments.index)

fontObject = fontFile.fonts[fontIndex]

print(f"{fileName}/{fontObject.getPostscriptName()}:")

if arguments.list:
    print(f"  {fontObject.getPostscriptName()} contains {len(fontObject.tables):d} tables:")
    
    for table in fontObject.tables:
        print(f"    '{table.tag}' 0x{table.checksum:08X} 0x{table.offset:08X} {table.length:10,d}")
    
    print()

if arguments.dump:
    for tableTag in arguments.dump:
        print(f"  Hex dump of '{tableTag}' table:")
        table = fontObject.getTable(tableTag)
        if table:
            table.dump()
            
        print()

if arguments.format:    
    for tableTag in arguments.format:
        print(f"  Formatted '{tableTag}' table:")
        table = fontObject.getTable(tableTag)
        if table:
            table.format()
            
        print()
