#! /usr/bin/python
# -*- coding: utf-8 -*-

# skcctest.py - Script and tests for testing functionality of skcc.py.
# (c) 2019 Patrick Harvey [see LICENSE.txt]

import sys, os, getopt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from imgtest import ImgTest, compareImages, deleteFiles, runTests
from skcc import outputToFile, readInputProfile, readOutputProfile, buildClimates, tColorTableDefault, defaultOceanColor, pColorTableDefault, kColorTableDefault, InputProfile, OutputProfile

def getTestDirPath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))

def getParentDirPath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', fname))

def getProfiaInputs():
    return getTestDirPath('ProfiaTempJul.png'), getTestDirPath('ProfiaTempJan.png'), getTestDirPath('ProfiaPrecJul.png'), getTestDirPath('ProfiaPrecJan.png')

def test1Fn():
    tempProf = InputProfile(tColorTableDefault, defaultOceanColor)
    precProf = InputProfile(pColorTableDefault, defaultOceanColor)
    outProf = OutputProfile(kColorTableDefault)

    outputPath = getTestDirPath('test1-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputs()

    comparePath = getTestDirPath('ProfiaOutputDefault.png')

    outputToFile(outputPath, buildClimates(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test1Clean():
    outputPath = getTestDirPath('test1-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def runAll(doCleanup):
    tests = []
    tests.append(ImgTest('All default profiles - Profia test', test1Fn, test1Clean))
    runTests(tests, doCleanup)

if __name__ == '__main__':
    try:
        options, xarguments = getopt.getopt(sys.argv[1:], 'v', ['leave-output'])
    except getopt.error:
        print('Error: Bad arguments to test script')

    cleanup = True

    for a in options[:]:
        if a[0] == '-v' or a[0] == '--leave-output':
            cleanup = False

    runAll(cleanup)
