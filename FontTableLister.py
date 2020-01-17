'''
Created on Jan 16, 2020

@author: emader
'''

import struct
import sys

import font


for fontFileName in sys.argv[1:] :
    fontFile = font.Font(fontFileName)
    
    fontName = fontFileName.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string
    
    print(fontName + " contains " + str(fontFile.numTables) + " tables.")
    
    for table in fontFile.tables :
        print("'" + table.tag_string() + "'" + " " + str(table.length))
    
    print()
    