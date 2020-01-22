'''
Created on Jan 16, 2020

@author: emader
'''

import sys

import font


for fontFileName in sys.argv[1:] :
    fontFile = font.File(fontFileName)
    
    fontName = fontFileName.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string
    
    print("{:s} contains {:d} fonts.".format(fontName, len(fontFile.fonts)))
    
    fontNumber = 1
    for fontObject in fontFile.fonts:
        print("    Font {:d} contains {:d} tables.".format(fontNumber, len(fontObject.tables)))
        for table in fontObject.tables :
            print("    '{:s}' {:10,d}".format(table.tag, table.length))
            if table.tag == 'head':
                table.format()
            elif table.tag == 'hhea':
                table.dump()
            elif table.tag == 'cmap':
                table.format()
        
        print()
        fontNumber += 1
    print()
    