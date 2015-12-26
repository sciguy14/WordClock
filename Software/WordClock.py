#!/usr/bin/python

# WordClock
# Made for Leah Meyerholtz by Jeremy Blum
# (c) 2016 Blum Idea Labs
# www.jeremyblum.com

import sys, os, time, argparse, atexit, signal
from datetime import datetime
from string import digits
# Uses the rgbmatrix.so library that is imported via a git submodule.
# Folder must be added to path to enable import
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/matrix")
from rgbmatrix import Adafruit_RGBmatrix

# Constants
MATRIX_W      = 32 # Number of Actual X Pixels
MATRIX_H      = 32 # Number of Actual Y Pixels
MATRIX_DEPTH  = 3  # Color Depth (RGB=3)
MATRIX_DIV    = 2  # Physical Matrix is Half of Pixel Matrix

# Colors
RED     = [255, 0,   0  ]
LIME    = [0,   255, 0  ]
BLUE    = [0,   0,   255]
YELLOW  = [255, 255, 0  ]
FUCHSIA = [255, 0,   255]
AQUA    = [0,   255, 255]
WHITE   = [255, 255, 255]

# Birthday
BIRTH_MONTH = 8
BIRTH_DAY = 29

#Color Fade Order (for Leah <3)
FADE_COLORS = [LIME, YELLOW, RED, FUCHSIA, BLUE, AQUA]


# Enumerate RGB Matrix Object
matrix = Adafruit_RGBmatrix(MATRIX_H, MATRIX_W/MATRIX_H)

#Word Dictionary
#Uses the Physical Grid mapping for the laser cut grid:
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
    "five2"     : {"row" : 10, "start" : 1,  "length" : 4, "height" : 1},
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
    "evening"   : {"row" : 16, "start" : 3,  "length" : 7, "height" : 1},
    "jeremy"    : {"row" : 16, "start" : 10, "length" : 6, "height" : 1},
    "heart2"    : {"row" : 16, "start" : 16, "length" : 1, "height" : 1}
}

# Generates the Appropriate Word List, given a datetime object. Defaults to Current Time
def getTimeWords(t=None):
    if t is None:
        t= datetime.now()
    words = []

    # If it's morning, we say "Good morning!"
    # Otherwise, we just say Hiya"
    if t.hour > 5 and t.hour <= 10:
        words += ['good','morning!']
    else:
        words += ['hiya']

    # If it's early, it's "Time for Coffee"
    # If it's a little later, we say "Carpe Diem"
    # If it's late, we say "Time for Sleep"
    if t.hour > 5 and t.hour <= 9:
        words += ['time','for','coffee']
    elif t.hour > 9 and t.hour <= 12:
        words += ['carpe','diem']
    elif t.hour > 22 or t.hour < 3:
        words += ['time','for','sleep']

    # Minutes/OClock
    words += ['it','is1']
    if (t.minute <=2 and t.hour != 0 and t.hour !=12) or (t.minute > 57 and t.hour !=23 and t.hour !=11):
        words += ['oclock']
    elif t.minute > 2 and t.minute <= 7:
        words += ['five1','minutes','past']
    elif t.minute > 7 and t.minute <= 12:
        words += ['ten1','minutes','past']
    elif t.minute > 12 and t.minute <= 17:
        words += ['a1','quarter','past']
    elif t.minute > 17 and t.minute <= 22:
        words += ['twenty','minutes','past']
    elif t.minute > 22 and t.minute <= 27:
        words += ['twenty','five1','minutes','past']
    elif t.minute > 27 and t.minute <= 32:
        words += ['half','past']
    elif t.minute > 32 and t.minute <= 37:
        words += ['twenty','five1','minutes','to']
    elif t.minute > 37 and t.minute <= 42:
        words += ['twenty','minutes','to']
    elif t.minute > 42 and t.minute <= 47:
        words += ['a1','quarter','to']
    elif t.minute > 47 and t.minute <= 52:
        words += ['ten1','minutes','to']
    elif t.minute > 52 and t.minute <= 57:
        words += ['five1','minutes','to']

    #Hours
    if t.minute > 32:
        disp_hour = t.hour + 1
    else:
        disp_hour = t.hour

    if disp_hour == 0 or disp_hour == 24:
        words += ['midnight']
    elif disp_hour == 12:
        words += ['noon']
    elif disp_hour == 1 or disp_hour == 13:
        words += ['one']
    elif disp_hour == 2 or disp_hour == 14:
        words += ['two']
    elif disp_hour == 3 or disp_hour == 15:
        words += ['three']
    elif disp_hour == 4 or disp_hour == 16:
        words += ['four']
    elif disp_hour == 5 or disp_hour == 17:
        words += ['five2']
    elif disp_hour == 6 or disp_hour == 18:
        words += ['six']
    elif disp_hour == 7 or disp_hour == 19:
        words += ['seven']
    elif disp_hour == 8 or disp_hour == 20:
        words += ['eight']
    elif disp_hour == 9 or disp_hour == 21:
        words += ['nine']
    elif disp_hour == 10 or disp_hour == 22:
        words += ['ten2']
    elif disp_hour == 11 or disp_hour == 23:
        words += ['eleven']

    #Time of Day
    if (t.hour > 0 and t.hour < 11) or (t.hour == 0 and t.minute > 32) or (t.hour == 11 and t.minute <= 32):
        words += ['in','the','morning']
    elif (t.hour > 12 and t.hour < 18) or (t.hour == 12 and t.minute > 32):
        words += ['in','the','afternoon']
    elif (t.hour >= 18 and t.hour < 23) or (t.hour == 23 and t.minute <= 33):
        words += ['in','the','evening']

    print t.strftime('%I:%M%p'),
    print "- " + (' '.join(words)).translate(None, digits)

    return words

# Generate the Pixel Buffer based on what words should be illuminated
# primary_words: The list of words to light up in the primary_color (usually the time)
# secondary_words: The list of words to light up in the secondary color (usually a special message)
# tertiary_words: The list of words to light up it the tertiary color (the Leah <3 Logo, in our case)
# fade is the transition time in seconds (float) (approximate)
last_buff = [0] * MATRIX_W * MATRIX_H * MATRIX_DEPTH
def setDisplay(primary_words=[], primary_color=RED, secondary_words=[], secondary_color=AQUA, tertiary_words=[], tertiary_color = WHITE, fade=0.1):
    global last_buff
    new_buff = [0] * MATRIX_W * MATRIX_H * MATRIX_DEPTH
    for word in primary_words + secondary_words + tertiary_words:
        ri = ((m[word]["row"] - 1) * MATRIX_DIV * MATRIX_DEPTH * MATRIX_W) + ((m[word]["start"]-1) * MATRIX_DIV * MATRIX_DEPTH)
        gi = ri + 1
        bi = ri + 2
        for y in xrange(m[word]["height"]*MATRIX_DIV):
            for x in xrange(m[word]["length"]*MATRIX_DIV):
                adder = MATRIX_DEPTH*x + MATRIX_DEPTH*MATRIX_H*y
                if word in primary_words:
                    color = primary_color
                elif word in secondary_words:
                    color = secondary_color
                elif word in tertiary_words:
                    color = tertiary_color
                new_buff[ri + adder] = color[0] #Set the Red Channel for this Word
                new_buff[gi + adder] = color[1] #Set the Green Channel for this Word
                new_buff[bi + adder] = color[2] #Set the Blue Channel for this Word

    diff_buff = [j - i for i, j in zip(last_buff, new_buff)]

    for frame in xrange(20):
        frame_buff = [0] * MATRIX_W * MATRIX_H * MATRIX_DEPTH
        for i, val in enumerate(diff_buff):
            frame_buff[i] = last_buff[i] + val*frame/19

        matrix.SetBuffer(frame_buff)
        time.sleep(fade/20.0/4.0) #Approximating this...

    last_buff = new_buff # Use this global var for enabling state fades

# Runs the Word Clock in a certain mode
# mode (pick one):
#   basic_test: Just lights up all the word units in all the colors to test them
#   time_test: Runs through a full day at high speed in the primry color
#   clock: Normal Clock mode. Endless Loop. Can Have modifiers applied. Shows time in primary color
# primary_color: RGB primary color to use for clock words
# secondary_color: RGB color to use for modifiers
# modifiers (pass as a list):
#   "leah":lights up "Leah <3" in slowly changing colors
#   "birthday": Shows the birthday message in the secondary color (if it's Leah's birthday)
#   "friday": Shows the Friday message in the secondary color
#   "iloveyou": Ocassionally show the iloveyou message in the secondary color
#   "byjeremy": Ocassionall the show byjeremy message in the secondary color
def run(mode="clock", primary_color=RED, secondary_color=AQUA, modifiers=[]):
    if mode == "basic_test":
        print "Testing each word & Color..."
        for key in m.iterkeys():
            print "  %s" % (key)
            setDisplay([key], RED)
            time.sleep(0.2)
            setDisplay([key], LIME)
            time.sleep(0.2)
            setDisplay([key], BLUE)
            time.sleep(0.2)
        matrix.Clear()
        print "Done."
    elif mode == "time_test":
        print "Testing All Times..."
        for h in xrange(24):
            for m in xrange(60):
                setDisplay(getTimeWords(datetime(2016, 01, 01, h, m, 0)),primary_color)
                time.sleep(0.2)
        matrix.Clear()
        print "Done."
    elif mode == "clock":
        print "Running the Clock."
        fade_counter = 0
        secondary_counter = 90
        while True:
            t = datetime.now()
            primary_words   = getTimeWords(t)
            secondary_words = []
            tertiary_words  = []
            tertiary_color  = []
            #TODO: Need to Test these.
            if "birthday" in modifiers and t.month == BIRTH_MONTH and t.day == BIRTH_DAY and secondary_counter%5 == 0 and secondary_counter < 100:
                secondary_words += ['happy','birthday']
                print "        - Happy Birthday"
            if "friday" in modifiers and t.weekday() == 4 and (secondary_counter+2)%5 == 0 and secondary_counter < 100:
                secondary_words +=['happy','friday']
                print "        - Happy Friday"
            if "iloveyou" in modifiers and "midnight" not in primary_words and (secondary_counter+3)%20 == 0 and secondary_counter < 100:
                #Uses the "I" in midnight, so it doesn't run if midnight is lit up
                secondary_words += ['i','love','you']
                print "        - I Love You"
            if "byjeremy" in modifiers and "oclock" not in primary_words and secondary_counter>=100 and secondary_counter<=105:
                #Uses "Clock" in "oclock", so it doesn't run if oclock is lit up
                secondary_words += ['this','is2','a2','word','clock','built','with','love','by','jeremy','heart2']
                print "        - This is a word clock built with love by Jeremy <3"
            if "leah" in modifiers:
                tertiary_words = ['leah1', 'heart1']
                tertiary_color = FADE_COLORS[fade_counter]

            setDisplay(primary_words,primary_color,secondary_words,secondary_color,tertiary_words,tertiary_color)
            fade_counter += 1
            if fade_counter > 5:
                fade_counter = 0
            secondary_counter += 1
            if secondary_counter > 105:
                fade_counter = 0

            time.sleep(5)
    else:
        print "Uknown mode."  

def exit_handler():
    print 'Script Aborted. Turning off Clock.'
    matrix.Clear()

#Main Execution
if __name__ == '__main__':
    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))
    run("clock", modifiers=["birthday","friday","iloveyou","byjeremy","leah"])