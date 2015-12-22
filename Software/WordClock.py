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
    "good"     : {"row" : 1,  "start" : 1,  "length" : 4, "height" : 1},
    "hiya"     : {"row" : 1,  "start" : 5,  "length" : 4, "height" : 1},
    "morning!" : {"row" : 2,  "start" : 1,  "length" : 8, "height" : 1},
    "leah1"    : {"row" : 1,  "start" : 9,  "length" : 6, "height" : 2},
    "heart1"   : {"row" : 1,  "start" : 15, "length" : 2, "height" : 2},
    "time"     : {"row" : 3,  "start" : 1,  "length" : 4, "height" : 1},
    "carpe"    : {"row" : 3,  "start" : 5,  "length" : 5, "height" : 1},
    "for"      : {"row" : 3,  "start" : 10, "length" : 3, "height" : 1},
    "diem"     : {"row" : 3,  "start" : 13, "length" : 4, "height" : 1}
}

#generate the Pixel Buffer based on what words should be illuminated
def setDisplay(words = []):
    buff = [0] * MATRIX_W * MATRIX_H * MATRIX_DEPTH
    for word in words:
        ri = ((m[word]["row"] - 1) * MATRIX_DIV * MATRIX_DEPTH * MATRIX_W) + ((m[word]["start"]-1) * MATRIX_DIV * MATRIX_DEPTH)
        print "Red Index Point: " + str(ri)
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
