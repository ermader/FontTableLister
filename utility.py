'''
Created on Jan 22, 2020

@author: emader
'''
import math

from datetime import datetime, timedelta, tzinfo, timezone

ldtBase = datetime(1904, 1, 1, tzinfo=timezone.utc)

def formatLongDateTime(ldt):
    dateTime = ldtBase + timedelta(seconds=ldt)
    # return dateTime.strftime("%A, %B %_d %Y %I:%M:%S %p %Z")
    return dateTime.strftime("%b %_d %Y %I:%M:%S %p %Z")

def formatHex8(value, withPrefix=True):
    if withPrefix:
        return f"0x{value:02X}"

    return f"{value:02X}"

def formatHex16(value, withPrefix=True):
    if withPrefix:
        return f"0x{value:04X}"

    return f"{value:04X}"

def formatHex32(value, withPrefix=True):
    if withPrefix:
        return f"0x{value:08X}"

    return f"{value:08X}"

def formatDecimal(value):
    return f"{value:d}"

def formatFloat3(float):
    return f"{float:.3f}"

def formatFixed(fixed):
    return formatFloat3(floatFromFixed(fixed))

def swapLongInt(highWord, lowWord):
    return (highWord << 16) | lowWord

def swapLongDateTime(highWord, lowWord):
    return (highWord << 32) | lowWord

def floatFromFixed(fixed):
    quotient = fixed / 65536.0
    integerPart = math.floor(quotient)
    fractionPart = quotient - integerPart
    
    return integerPart + fractionPart

def roundAndDivide(value, dividend):
    return int((value + dividend - 1) / dividend)
