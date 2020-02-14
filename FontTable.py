'''
Created on Jan 26, 2020

@author: emader
'''

import struct

import utility


def formatLine(label, value):
    print(f"      {label + ':':<25s}{value:>30s}")

class Table(object):
    '''
    classdocs
    '''

    FONT_DIRECTORY_ENTRY_FORMAT = ">4sIII"
    FONT_DIRECTORY_ENTRY_LENGTH = struct.calcsize(FONT_DIRECTORY_ENTRY_FORMAT)

    rawBytes = None

    BYTES_PER_WORD = struct.calcsize(">H")
    WORDS_PER_LINE = 16
    BYTES_PER_LINE = BYTES_PER_WORD * WORDS_PER_LINE

    def __init__(self, fontFile, tagBytes, checksum, offset, length):
        self.fontFile = fontFile
        self.tag = tagBytes.decode("ascii")
        self.checksum = checksum
        self.offset = offset
        self.length = length

    def rawData(self):
        if self.rawBytes == None:
            self.fontFile.seek(self.offset)
            dataLength = (self.length + 1) & 0xFFFFFFFE
            self.rawBytes = self.fontFile.read(dataLength)
        return self.rawBytes

    def dump(self):
        tableData = self.rawData()
        wordsToDump = utility.roundAndDivide(self.length, self.BYTES_PER_WORD)
        linesToDump = utility.roundAndDivide(wordsToDump, self.WORDS_PER_LINE)
        rawWordsFormat = f">{wordsToDump:d}H"
        rawWords = struct.unpack(rawWordsFormat, tableData)

        lineOffset = 0
        for _ in range(linesToDump):
            print(f"      {utility.formatHex32(lineOffset, withPrefix=False):s}", end=":")

            wordsPerLine = min(self.WORDS_PER_LINE, wordsToDump - (lineOffset >> 1))
            for word in range(wordsPerLine):
                print(f" {utility.formatHex16(rawWords[(lineOffset >> 1) + word], withPrefix=False):s}", end="")

            lineOffset += self.BYTES_PER_LINE
            print()
        print()

    def format(self):
        print(f"      Don't know how to format a '{self.tag:s}' table.")
        print()
