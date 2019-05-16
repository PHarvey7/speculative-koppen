#! /usr/bin/python
# -*- coding: utf-8 -*-

# inputHandler.py
# (c) 2019 Patrick Harvey (see LICENSE.txt)

# Classes and functionality for reading in input profiles and
# interpreting input data.

import sys, re

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
                print('Error: Invalid color in input data (did not match input profile): (' + str(rgbColor[0]) + ', ' + str(rgbColor[1]) + ', ' + str(rgbColor[2]) + ')')
                sys.exit(1)
            else:
                return self.defaultValue
        else:
            return self.colorTable[rgbColor]

def readInputProfile(fname):
    try:
        fp = open(fname, 'r')
        profTable = {}
        ignoredColors = []
        defaultVal = None
        try:
            for line in fp:
                if ((line[0] != '#') and (not (line.isspace()))):
                    rmatch = re.match(r"""[^:]*:\s*\(([0-9]+,\s*[0-9]+,\s*[0-9]+\s*)\)\s*:\s*(-?[0-9.]*X?)""", line)
                    if rmatch:
                        iColor = rmatch.group(1)
                        if (iColor == 'Default'):
                            iValue = rmatch.group(2)
                            if (not (defaultVal is None)):
                                print('Warning: Duplicate default value in input profile: ' + iValue)
                            if (iValue == 'X'):
                                defaultVal = 'X'
                            else:
                                defaultVal = float(iValue)
                        rgbVals = iColor.split(',')
                        rval = int(rgbVals[0].strip())
                        gval = int(rgbVals[1].strip())
                        bval = int(rgbVals[2].strip())
                        if ((rval < 0) or (rval > 255) or (gval < 0) or (gval > 255) or (bval < 0) or (bval > 255)):
                            print('Error: Invalid RGB color in input profile: ' + str((rval, gval, bval)))
                            sys.exit(0)
                        iValue = rmatch.group(2)
                        if ((rval, gval, bval) in profTable):
                            print('Warning: Duplicate color in input profile: ' + str((rval, gval, bval)))
                        if (iValue == 'X'):
                            ignoredColors.append((rval, gval, bval))
                        else:
                            ival = float(iValue)
                            profTable[(rval, gval, bval)] = ival
                    else:
                        print('Error: Invalid line in input profile: ' + line)
                        sys.exit(1)
        finally:
            fp.close()
    except:
        print('Error: Could not open input profile: ' + fname)
        sys.exit(1)
    return InputProfile(profTable, ignoredColors)

        