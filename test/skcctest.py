#! /usr/bin/python
# -*- coding: utf-8 -*-

# skcctest.py - Script and tests for testing functionality of skcc.py.
# (c) 2019 Patrick Harvey [see LICENSE.txt]

import sys, os, getopt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from imgtest import ImgTest, compareImages, deleteFiles, runTests
from skcc import outputToFile, buildOutput, tColorTableDefault, defaultOceanColor, pColorTableDefault, kColorTableDefault, readAndValidateKoppenOutputProfile, defaultUnknownColor, hColorTableDefault
from ioHandling.inputHandler import readInputProfile, InputProfile
from ioHandling.outputHandler import OutputProfile
from utils.errors import SKCCError

def getTestDirPath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), fname))

def getParentDirPath(fname):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', fname))

def getProfiaInputs():
    return getTestDirPath('ProfiaTempJul.png'), getTestDirPath('ProfiaTempJan.png'), getTestDirPath('ProfiaPrecJul.png'), getTestDirPath('ProfiaPrecJan.png')

def getBoxesInputs():
    return getTestDirPath('BoxesTempJul.png'), getTestDirPath('BoxesTempJan.png'), getTestDirPath('BoxesPrecJul.png'), getTestDirPath('BoxesPrecJan.png')

def getBoxesInputsSwappedPrecipitations():
    return getTestDirPath('BoxesTempJul.png'), getTestDirPath('BoxesTempJan.png'), getTestDirPath('BoxesPrecJan.png'), getTestDirPath('BoxesPrecJul.png')

def getProfiaInputsPrecipOcean():
    return getTestDirPath('ProfiaTempJul.png'), getTestDirPath('ProfiaTempJan.png'), getTestDirPath('ProfiaPrecJul.png'), getTestDirPath('ProfiaPrecJanExtraOcean.png')

def getProfiaInputsBadPixel():
    return getTestDirPath('ProfiaTempJul.png'), getTestDirPath('ProfiaTempJan.png'), getTestDirPath('ProfiaPrecJulBadPixel.png'), getTestDirPath('ProfiaPrecJan.png')

def getBallInputs():
    return getTestDirPath('BallTempJul.png'), getTestDirPath('BallTempJan.png'), getTestDirPath('BallPrecJul.png'), getTestDirPath('BallPrecJan.png')

def getProfiaInputsOceanDefault():
    return getTestDirPath('ProfiaTempJulRandomOcean.png'), getTestDirPath('ProfiaTempJanRandomOcean.png'), getTestDirPath('ProfiaPrecJulFilledOcean.png'), getTestDirPath('ProfiaPrecJanFilledOcean.png')

def test1Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test1-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputs()

    comparePath = getTestDirPath('ProfiaOutputDefault.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test1Clean():
    outputPath = getTestDirPath('test1-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test2Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = readAndValidateKoppenOutputProfile(getParentDirPath('altOutputProfile'))

    outputPath = getTestDirPath('test2-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputs()

    comparePath = getTestDirPath('ProfiaOutputAlt.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test2Clean():
    outputPath = getTestDirPath('test2-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test3Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = readAndValidateKoppenOutputProfile(getParentDirPath('defaultOutputProfile'))

    outputPath = getTestDirPath('test3-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getBoxesInputs()

    comparePath = getTestDirPath('BoxesOutputDefault.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))
                                
    return compareImages(outputPath, comparePath)

def test3Clean():
    outputPath = getTestDirPath('test3-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test4Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = readAndValidateKoppenOutputProfile(getParentDirPath('defaultOutputProfile'))

    outputPath = getTestDirPath('test4-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getBoxesInputsSwappedPrecipitations()

    comparePath = getTestDirPath('BoxesOutputSwapped.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test4Clean():
    outputPath = getTestDirPath('test4-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test5Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test5-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputsPrecipOcean()

    comparePath = getTestDirPath('ProfiaOutputPrecipOcean.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test5Clean():
    outputPath = getTestDirPath('test5-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test6Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test6-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputsBadPixel()

    correctError = False
    try:
        buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf)
    except SKCCError as e:
        if (str(e) == 'Invalid color in input data (did not match input profile): (255, 0, 0)'):
            correctError = True
        else:
            raise
    return correctError

def test6Clean():
    outputPath = getTestDirPath('test6-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test7Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = OutputProfile(hColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test7-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputs()

    comparePath = getTestDirPath('ProfiaHoldridgeOutput.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf, 'holdridge'))

    return compareImages(outputPath, comparePath)

def test7Clean():
    outputPath = getTestDirPath('test7-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test8Fn():
    tempProf = readInputProfile(getParentDirPath('defaultTempProfile'))
    precProf = readInputProfile(getParentDirPath('defaultPrecProfile'))
    outProf = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test8-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputs()

    comparePath = getTestDirPath('ProfiaOutputDefault.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test8Clean():
    outputPath = getTestDirPath('test8-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test9Fn():
    tempProf = InputProfile(tColorTableDefault, [defaultOceanColor])
    precProf = readInputProfile(getParentDirPath('altPrecProfile'))
    outProf = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test9-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getBallInputs()

    comparePath = getTestDirPath('BallOutput.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test9Clean():
    outputPath = getTestDirPath('test9-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def test10Fn():
    correctError = False
    try:
        tempProf = readInputProfile(getTestDirPath('testBrokenTempProfile'))
    except SKCCError as e:
        if (str(e) == 'Invalid RGB color in input profile: (275, 225, 140)'):
            correctError = True
        else:
            raise
    return correctError

def test10Clean():
    pass

def test11Fn():
    tempProf = readInputProfile(getTestDirPath('testDefaultOceanTempProfile'))
    precProf = InputProfile(pColorTableDefault, [defaultOceanColor])
    outProf = OutputProfile(kColorTableDefault, defaultOceanColor, defaultUnknownColor)

    outputPath = getTestDirPath('test11-out.png')
    tempnsPath, tempnwPath, precnsPath, precnwPath = getProfiaInputsOceanDefault()

    comparePath = getTestDirPath('ProfiaOutputDefault.png')

    outputToFile(outputPath, buildOutput(tempnsPath, tempnwPath, precnsPath, precnwPath, tempProf, precProf, outProf))

    return compareImages(outputPath, comparePath)

def test11Clean():
    outputPath = getTestDirPath('test11-out.png')
    dPaths = [outputPath]
    deleteFiles(dPaths)

def runAll(doCleanup):
    tests = []
    tests.append(ImgTest('All default profiles - Profia test', test1Fn, test1Clean))
    tests.append(ImgTest('Alternate output profile - Profia test', test2Fn, test2Clean))
    tests.append(ImgTest('All default profiles - Boxes test', test3Fn, test3Clean))
    tests.append(ImgTest('All default profiles - Boxes test (swapped summer/winter precipitation)', test4Fn, test4Clean))
    tests.append(ImgTest('Test for successful output when precipitation maps have ocean where temperature maps have land', test5Fn, test5Clean))
    tests.append(ImgTest('Test that correct error is thrown for invalid pixel colors in input data', test6Fn, test6Clean))
    tests.append(ImgTest('All default profiles - Holdridge mode Profia test', test7Fn, test7Clean))
    tests.append(ImgTest('Test of reading in input profiles - read in of defaults - Profia test', test8Fn, test8Clean))
    tests.append(ImgTest('Test of input profiles with (Default) colors - Ball test', test9Fn, test9Clean))
    tests.append(ImgTest('Test that correct error is thrown for invalid colors in input profiles', test10Fn, test10Clean))
    tests.append(ImgTest('Test of input profiles that (Default) to ocean - Profia test', test11Fn, test11Clean))
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
