'''
Created on Jan 22, 2020

@author: emader
'''
import math

from datetime import datetime, timedelta, tzinfo, timezone

ldtBase = datetime(1904, 1, 1, tzinfo=timezone.utc)

def formatLongDateTime(ldt):
    dateTime = ldtBase + timedelta(seconds=ldt)
    return dateTime.strftime("%A, %B %_d %Y %I:%M:%S %p %Z")

def formatHex16(value, withPrefix=True):
    if withPrefix:
        formatString = "{:#06X}"
    else:
        formatString = "{:04X}"
        
    return formatString.format(value)

def formatHex32(value, withPrefix=True):
    if withPrefix:
        formatString = "{:#010X}"
    else:
        formatString = "{:08X}"
        
    return formatString.format(value)


def formatDecimal(value):
    return "{:d}".format(value)

def formatFixed(fixed):
    return "{:.3f}".format(floatFromFixed(fixed))

def swapLongDateTime(highWord, lowWord):
    return (highWord << 32) | lowWord

def floatFromFixed(fixed):
    quotient = fixed / 65536.0
    integerPart = math.floor(quotient)
    fractionPart = quotient - integerPart
    
    return integerPart + fractionPart

def roundAndDivide(value, dividend):
    return int((value + dividend - 1) / dividend)
