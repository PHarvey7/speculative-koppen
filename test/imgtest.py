#! /usr/bin/python
# -*- coding: utf-8 -*-

# imgtest.py - Utilities for writing tests for code that produces images.
# (c) 2019 Patrick Harvey [see LICENSE.txt]

import sys, os, itertools
from PIL import Image, ImageMath

class ImgTest:
    def __init__(self, nm, testfn, cleanfn):
        self.name = nm
        self.testFn = testfn
        self.cleanFn = cleanfn

class TestState:
    def __init__(self):
        self.testsRun = 0
        self.testsPassed = 0

    def printResults(self):
        print('Total: Passed %d tests out of %d run' % (self.testsPassed, self.testsRun))
        if (self.testsRun == self.testsPassed):
            print('All tests passed!')
        else:
            print('Failed %d tests!' % (self.testsRun - self.testsPassed))

# Returns True iff the two images have equal contents and False otherwise.
def compareImages(fnameA, fnameB):
    imgA = Image.open(fnameA)
    imgB = Image.open(fnameB)

    bandsA = imgA.split()
    bandsB = imgB.split()
    bandPairs = zip(bandsA, bandsB)
    diffs = []
    for iTuple in bandPairs:
        diffs.append(ImageMath.eval("convert(a - b, 'L')", a=iTuple[0], b=iTuple[1]))    
    
    result = Image.merge('RGB', diffs).getbbox() is None

    return result

# Deletes the files with names listed in fnames.
def deleteFiles(fnames):
    for fname in fnames:
        if os.path.isfile(fname):
            os.remove(fname)

# Runs the given test function.
def runTest(tState, test, doCleanup):
    tState.testsRun += 1
    print('Running test %d: %s...' % (tState.testsRun, test.name))
    try:
        if test.testFn():
            tState.testsPassed += 1
            print('Test passed')
        else:
            print('*** Test failed!')
    except Exception as ex:
        print('*** Error occurred: %s' % str(ex))
        print('*** Test failed!')
    if doCleanup:
        test.cleanFn()

# Runs a set of test functions.
def runTests(tests, doCleanup):
    tState = TestState()
    for test in tests:
        runTest(tState, test, doCleanup)
    tState.printResults()


