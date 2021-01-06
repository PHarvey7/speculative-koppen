#! /usr/bin/python
# -*- coding: utf-8 -*-

# outputHandler.py
# (c) 2018-2020 Patrick Harvey (see LICENSE.txt)

# Classes and functionality for reading in output profiles and
# formatting output data.

import sys, re, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.errors import SKCCError

class OutputProfile:
    def __init__(self, oTable, ignColor, unkColor):
        self.colorTable = oTable
        self.ignoredColor = ignColor
        self.unknownColor = unkColor
    
def readOutputProfile(fname):
    fp = open(fname, 'r')
    profTable = {}
    ignColor = (107, 165, 210)
    unknownColor = (255, 0, 255)
    try:
        for line in fp:
            if ((line[0] != '#') and (not (line.isspace()))):
                rmatch = re.match(r"""\s*([^:]+)\s*:\s*\(\s*([0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s*)\s*\)""", line)
                if rmatch:
                    oColor = rmatch.group(2)
                    rgbVals = oColor.split(',')
                    rval = int(rgbVals[0].strip())
                    gval = int(rgbVals[1].strip())
                    bval = int(rgbVals[2].strip())
                    key = rmatch.group(1).strip()
                    if ((rval < 0) or (rval > 255) or (gval < 0) or (gval > 255) or (bval < 0) or (bval > 255)):
                        raise SKCCError('Invalid RGB color in output profile: ' + str((rval, gval, bval)))
                    if (key == 'Ignored') or (key == 'Ocean'):
                        ignColor = (rval, gval, bval)
                    if (key == 'Unknown'):
                        unknownColor = (rval, gval, bval)
                    if (key in profTable):
                        print('Warning: Duplicate entries for key | ' + kClass + ' | in output profile')
                    profTable[key] = (rval, gval, bval)
                else:
                    raise SKCCError('Invalid line in output profile: ' + line)
    finally:
        fp.close()
    return OutputProfile(profTable, ignColor, unknownColor)
