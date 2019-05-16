#! /usr/bin/python
# -*- coding: utf-8 -*-

# outputHandler.py
# (c) 2018 Patrick Harvey (see LICENSE.txt)

# Classes and functionality for reading in output profiles and
# formatting output data.

import sys, re

class OutputProfile:
    def __init__(self, oTable, ignColor, unkColor):
        self.colorTable = oTable
        self.ignoredColor = ignColor
        self.unknownColor = unkColor
    
def readOutputProfile(fname):
    try:
        fp = open(fname, 'r')
        profTable = {}
        ignColor = (107, 165, 210)
        unknownColor = (255, 0, 255)
        try:
            for line in fp:
                if ((line[0] != '#') and (not (line.isspace()))):
                    rmatch = re.match(r"""\s*([^:\s]+)\s*:\s*\(\s*([0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s*)\s*\)""", line)
                    if rmatch:
                        oColor = rmatch.group(2)
                        rgbVals = oColor.split(',')
                        rval = int(rgbVals[0].strip())
                        gval = int(rgbVals[1].strip())
                        bval = int(rgbVals[2].strip())
                        key = rmatch.group(1)
                        if ((rval < 0) or (rval > 255) or (gval < 0) or (gval > 255) or (bval < 0) or (bval > 255)):
                            print('Error: Invalid RGB color in output profile: ' + str((rval, gval, bval)))
                            sys.exit(0)
                        if (key == 'Ignored'):
                            ignColor = (rval, gval, bval)
                        if (key == 'Unknown'):
                            unknownColor = (rval, gval, bval)
                        if (key in profTable):
                            print('Warning: Duplicate entries for key | ' + kClass + ' | in output profile')
                        profTable[key] = (rval, gval, bval)
                    else:
                        print('Error: Invalid line in output profile: ' + line)
                        sys.exit(0)
        finally:
            fp.close()
    except:
        print('Error: Could not open output profile: ' + fname)
        sys.exit(0)
    return OutputProfile(profTable, ignColor, unknownColor)
