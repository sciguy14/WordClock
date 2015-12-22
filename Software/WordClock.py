#!/usr/bin/python

# Simple RGBMatrix example, using only Clear(), Fill() and SetPixel().
# These functions have an immediate effect on the display; no special
# refresh operation needed.

import sys, os, time, argparse
# Uses the rgbmatrix.so library that is imported via a git submodule.
# Folder must be added to path to enable import
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/matrix")
from rgbmatrix import Adafruit_RGBmatrix

# Constants
MATRIX_W      = 32 # Number of Actual X Pixels
MATRIX_H      = 32 # Number of Actual Y Pixels
MATRIX_DEPTH  = 3  # Color Depth (RGB=3)
MATRIX_DIV    = 2  # Physical Matrix is Half of Pixel Matrix

# Number of Rows & Number of Chained Displays
matrix = Adafruit_RGBmatrix(MATRIX_H, MATRIX_W/MATRIX_H)


#Word Dictionary
#Uses the Physical Grad mapping for the laser cut grid:
# X is 1 - 16 inclusive
# Y is 1 - 16 includive
# Origin is top left corner 
m = {
    "good"      : {"row" : 1,  "start" : 1,  "length" : 4, "height" : 1},
    "hiya"      : {"row" : 1,  "start" : 5,  "length" : 4, "height" : 1},
    "morning!"  : {"row" : 2,  "start" : 1,  "length" : 8, "height" : 1},
    "leah1"     : {"row" : 1,  "start" : 9,  "length" : 6, "height" : 2},
    "heart1"    : {"row" : 1,  "start" : 15, "length" : 2, "height" : 2},
    "time"      : {"row" : 3,  "start" : 1,  "length" : 4, "height" : 1},
    "carpe"     : {"row" : 3,  "start" : 5,  "length" : 5, "height" : 1},
    "for"       : {"row" : 3,  "start" : 10, "length" : 3, "height" : 1},
    "diem"      : {"row" : 3,  "start" : 13, "length" : 4, "height" : 1},
    "happy"     : {"row" : 4,  "start" : 1,  "length" : 5, "height" : 1},
    "sleep"     : {"row" : 4,  "start" : 6,  "length" : 5, "height" : 1},
    "coffee"    : {"row" : 4,  "start" : 11, "length" : 6, "height" : 1},
    "it"        : {"row" : 5,  "start" : 1,  "length" : 2, "height" : 1},
    "friday"    : {"row" : 5,  "start" : 3,  "length" : 6, "height" : 1},
    "birthday"  : {"row" : 5,  "start" : 9,  "length" : 8, "height" : 1},
    "hi"        : {"row" : 6,  "start" : 1,  "length" : 2, "height" : 1},
    "is1"       : {"row" : 6,  "start" : 2,  "length" : 2, "height" : 1},
    "leah2"     : {"row" : 6,  "start" : 4,  "length" : 4, "height" : 1},
    "ten1"      : {"row" : 6,  "start" : 8,  "length" : 3, "height" : 1},
    "twenty"    : {"row" : 6,  "start" : 11, "length" : 6, "height" : 1},
    "half"      : {"row" : 7,  "start" : 1,  "length" : 4, "height" : 1},
    "a1"        : {"row" : 7,  "start" : 5,  "length" : 1, "height" : 1},
    "five1"     : {"row" : 7,  "start" : 6,  "length" : 4, "height" : 1},
    "quarter"   : {"row" : 7,  "start" : 10, "length" : 7, "height" : 1},
    "minutes"   : {"row" : 8,  "start" : 1,  "length" : 7, "height" : 1},
    "this"      : {"row" : 8,  "start" : 8,  "length" : 4, "height" : 1},
    "past"      : {"row" : 8,  "start" : 12, "length" : 4, "height" : 1},
    "to"        : {"row" : 8,  "start" : 15, "length" : 2, "height" : 1},
    "one"       : {"row" : 9,  "start" : 1,  "length" : 3, "height" : 1},
    "two"       : {"row" : 9,  "start" : 4,  "length" : 3, "height" : 1},
    "three"     : {"row" : 9,  "start" : 7,  "length" : 5, "height" : 1},
    "eight"     : {"row" : 9,  "start" : 12, "length" : 5, "height" : 1},
    "five"      : {"row" : 10, "start" : 1,  "length" : 4, "height" : 1},
    "is2"       : {"row" : 10, "start" : 5,  "length" : 2, "height" : 1},
    "eleven"    : {"row" : 10, "start" : 7,  "length" : 6, "height" : 1},
    "nine"      : {"row" : 10, "start" : 13, "length" : 4, "height" : 1},
    "four"      : {"row" : 11, "start" : 1,  "length" : 4, "height" : 1},
    "a2"        : {"row" : 11, "start" : 5,  "length" : 1, "height" : 1},
    "six"       : {"row" : 11, "start" : 6,  "length" : 3, "height" : 1},
    "seven"     : {"row" : 11, "start" : 9,  "length" : 5, "height" : 1},
    "ten2"      : {"row" : 11, "start" : 14, "length" : 3, "height" : 1},
    "twelve"    : {"row" : 12, "start" : 1,  "length" : 6, "height" : 1},
    "word"      : {"row" : 12, "start" : 7,  "length" : 4, "height" : 1},
    "oclock"    : {"row" : 12, "start" : 11, "length" : 6, "height" : 1},
    "clock"     : {"row" : 12, "start" : 12, "length" : 5, "height" : 1},
    "midnight"  : {"row" : 13, "start" : 1,  "length" : 8, "height" : 1},
    "i"         : {"row" : 13, "start" : 2,  "length" : 1, "height" : 1},
    "in"        : {"row" : 13, "start" : 9,  "length" : 2, "height" : 1},
    "noon"      : {"row" : 13, "start" : 10, "length" : 4, "height" : 1},
    "the"       : {"row" : 13, "start" : 14, "length" : 3, "height" : 1},
    "built"     : {"row" : 14, "start" : 1,  "length" : 5, "height" : 1},
    "morning"   : {"row" : 14, "start" : 6,  "length" : 7, "height" : 1},
    "with"      : {"row" : 14, "start" : 13, "length" : 4, "height" : 1},
    "love"      : {"row" : 15, "start" : 1,  "length" : 4, "height" : 1},
    "afternoon" : {"row" : 15, "start" : 5,  "length" : 9, "height" : 1},
    "you"       : {"row" : 15, "start" : 14, "length" : 3, "height" : 1},
    "by"        : {"row" : 16, "start" : 1,  "length" : 2, "height" : 1},
    "bye"       : {"row" : 16, "start" : 1,  "length" : 3, "height" : 1},
    "evening"   : {"row" : 16, "start" : 3,  "length" : 7, "height" : 1},
    "jeremy"    : {"row" : 16, "start" : 10, "length" : 6, "height" : 1},
    "heart2"    : {"row" : 16, "start" : 16, "length" : 1, "height" : 1}
}

#generate the Pixel Buffer based on what words should be illuminated
def setDisplay(words = []):
    buff = [0] * MATRIX_W * MATRIX_H * MATRIX_DEPTH
    for word in words:
        ri = ((m[word]["row"] - 1) * MATRIX_DIV * MATRIX_DEPTH * MATRIX_W) + ((m[word]["start"]-1) * MATRIX_DIV * MATRIX_DEPTH)
        gi = ri + 1
        bi = ri + 2
        for y in xrange(m[word]["height"]*MATRIX_DIV):
            for x in xrange(m[word]["length"]*MATRIX_DIV):
                adder = MATRIX_DEPTH*x + MATRIX_DEPTH*MATRIX_H*y
                buff[ri + adder] = 255 #Set the Red Channel for this Word
                buff[gi + adder] = 0 #Set the Green Channel for this Word
                buff[bi + adder] = 0 #Set the Blue Channel for this Word

    matrix.SetBuffer(buff)

setDisplay(['good', 'leah1', 'heart1', 'time', 'diem'])
time.sleep(20.0)
matrix.Clear()
