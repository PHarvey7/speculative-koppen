#! /usr/bin/python
# -*- coding: utf-8 -*-

# inputHandler.py
# (c) 2019-2020 Patrick Harvey (see LICENSE.txt)

# Classes and functionality for reading in input profiles and
# interpreting input data.

import sys, re, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.errors import SKCCError

class InputProfile:
    def __init__(self, iTable, ignoredColors, default=None):
        self.colorTable = iTable
        self.ignoreColors = ignoredColors
        self.defaultValue = default

    def isIgnored(self, rgbColor):
        if ((rgbColor in self.ignoreColors) or ((not (rgbColor in self.colorTable.keys())) and (self.defaultValue == 'X'))):
            return True
        else:
            return False

    def getValue(self, rgbColor):
        if not (rgbColor in self.colorTable):
            if self.defaultValue is None:
                raise SKCCError('Invalid color in input data (did not match input profile): (' + str(rgbColor[0]) + ', ' + str(rgbColor[1]) + ', ' + str(rgbColor[2]) + ')')
            else:
                return self.defaultValue
        else:
            return self.colorTable[rgbColor]

def readInputProfile(fname):
    fp = open(fname, 'r')
    profTable = {}
    ignoredColors = []
    defaultVal = None
    try:
        for line in fp:
            if ((line[0] != '#') and (not (line.isspace()))):
                rmatch = re.match(r"""[^:]*:\s*\((Default|[0-9]+,\s*[0-9]+,\s*[0-9]+\s*)\)\s*:\s*(-?[0-9.]*X?O?)""", line)
                if rmatch:
                    iColor = rmatch.group(1)
                    if (iColor == 'Default'):
                        iValue = rmatch.group(2)
                        if (not (defaultVal is None)):
                            print('Warning: Duplicate default value in input profile: ' + iValue)
                        if ((iValue == 'X') or (iValue == 'O')):
                            defaultVal = 'X'
                        else:
                            defaultVal = float(iValue)
                    else:
                        rgbVals = iColor.split(',')
                        rval = int(rgbVals[0].strip())
                        gval = int(rgbVals[1].strip())
                        bval = int(rgbVals[2].strip())
                        if ((rval < 0) or (rval > 255) or (gval < 0) or (gval > 255) or (bval < 0) or (bval > 255)):
                            raise SKCCError('Invalid RGB color in input profile: ' + str((rval, gval, bval)))
                        iValue = rmatch.group(2)
                        if ((rval, gval, bval) in profTable):
                            print('Warning: Duplicate color in input profile: ' + str((rval, gval, bval)))
                        if ((iValue == 'X') or (iValue == 'O')):
                            ignoredColors.append((rval, gval, bval))
                        else:
                            ival = float(iValue)
                            profTable[(rval, gval, bval)] = ival
                else:
                    raise SKCCError('Invalid line in input profile: ' + line)
    finally:
        fp.close()
    return InputProfile(profTable, ignoredColors, default=defaultVal)

        
