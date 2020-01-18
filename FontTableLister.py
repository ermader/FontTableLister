'''
Created on Jan 16, 2020

@author: emader
'''

import sys

import font


for fontFileName in sys.argv[1:] :
    fontFile = font.File(fontFileName)
    
    fontName = fontFileName.split("/")[-1:][0] # [-1:] gives a list with 1 string in it, so need [0] to get the string
    
    print("%s contains %d fonts." % (fontName, len(fontFile.fonts)))
    
    fontNumber = 1
    for fontObject in fontFile.fonts:
        print("    Font %d contains %d tables." % (fontNumber, len(fontObject.tables)))
        for table in fontObject.tables :
            print("    '%s' %d" % (table.tag_string(), table.length))
        
        print()
        fontNumber += 1
    print()
    