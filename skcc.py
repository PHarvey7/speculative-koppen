#! /usr/bin/python
# -*- coding: utf-8 -*-

# Speculative Köppen-Geiger Climate Classifier
# (c) 2018 Patrick Harvey (see LICENSE.txt)

import sys, getopt, itertools, re, time
from PIL import Image

versionNumber = '0.0.3'

kColorTableDefault = {'Af':(11, 36, 250), 'As':(76, 171, 247), 'Aw':(76, 171, 247), 'Am':(21, 123, 251), 
               'Cfa':(199, 253, 92), 'Csa':(255, 253, 56), 'Cwa':(153, 253, 154),
               'Cfb':(109, 253, 70), 'Csb':(198, 197, 41), 'Cwb':(103, 197, 104),
               'Cfc':(60, 197, 35), 'Csc':(198, 197, 41), 'Cwc':(103, 197, 104),
               'Dfa':(45, 255, 254), 'Dsa':(252, 40, 251), 'Dwa':(172, 179, 253),
               'Dfb':(66, 200, 252), 'Dsb':(196, 29, 197), 'Dwb':(92, 122, 216),
               'Dfc':(16, 126, 124), 'Dsc':(149, 55, 147), 'Dwc':(77, 84, 178),
               'Dfd':(6, 69, 93), 'Dsd':(149, 101, 148), 'Dwd':(50, 14, 133),
               'ET':(178, 178, 178), 'EF':(104, 104, 104),
               'BSh':(243, 162, 39), 'BSk':(254, 218, 108), 'BWh':(251, 13, 27), 'BWk':(252, 151, 151)}

tColorTableDefault = {(160, 0, 65):38, (210, 60, 80):31, (245, 110, 65):25, (250, 175, 95):20,
               (255, 225, 140):14, (230, 245, 150):5, (170, 220, 165):-5, (100, 195, 165):-18,
               (50, 135, 190):-32, (95, 80, 160):-40}

pColorTableDefault = {(135, 0, 180):300.0, (130, 60, 200):170.0, (105, 70, 200):105.0, (60, 60, 180):55.0, 
               (70, 95, 150):30.0, (55, 85, 100):15.0, (35, 50, 50):7.5, (20, 20, 20):2.5}

class InputProfile:
    def __init__(self, iTable, oceanC):
        self.colorTable = iTable
        self.oceanColor = oceanC

class OutputProfile:
    def __init__(self, cTable):
        self.colorTable = cTable

defaultOceanColor = (107, 165, 210)

def usage():
    print('''skcc.py : Speculative Köppen-Geiger Climate Classifier
  Converts input temperature and precipitation data into a map painted with
  the matching Köppen-Geiger climate categories.
  Options:
    -h, --help    : Displays this message
    -v, --version : Displays the current version of skcc.py
    -s, --quiet   : Silences successful completion output
    -o:<fname>, --outfile=<fname>  : Outputs the resulting image to the filepath '<fname>', 
                                    requires two temperature and two precipitation inputs. Required.
    -t:<fname>, --tempnw=<fname>   : Takes temperature input data for northern-hemisphere winter 
                                    from the image '<fname>'. Required.
    -u:<fname>, --tempns=<fname>   : Takes temperature input data for northern-hemisphere summer
                                    from the image '<fname>'. Required.
    -p:<fname>, --precnw=<fname>   : Take precipitation input for northern-hemisphere winter from the image '<fname>'. Required.
    -q:<fname>, --precns=<fname>   : Take precipitation input for northern-hemisphere summer from the image '<fname>'. Required.
    -v:<fname>, --tempprof=<fname> : Take the input temperature color profile from the filename '<fname>'. 
    -r:<fname>, --precprof=<fname> : Take the input precipitation color profile from the filename '<fname>'.
    -k:<fname>, --outprof=<fname>  : Take the output color profile from the filename '<fname>'. ''')
    sys.exit(0)

def version():
    print('''skcc.py: v''' + versionNumber)
    sys.exit(0)

def optErr():
    print('Error: Invalid options. Use the \'-h\' or \'--help\' options for usage information.')
    sys.exit(0)

def outputToFile(filename, img):
    try:
        img.save(filename)
    except:
        print('Error: Could not write to file ' + filename)
        sys.exit(0)

# Converts an input pixel color to a temperature value.
def getTemperatureCategory(tPixel, tempProfile):
    if (tPixel in tempProfile.colorTable):
        return tempProfile.colorTable[tPixel]
    else:
        print('Error: Invalid temperature map color value: ' + str(tPixel))
        sys.exit(0)

# Converts an input pixel color to a precipitation value.
def getPrecipCategory(pPixel, precProfile):
    if (pPixel in precProfile.colorTable):
        return precProfile.colorTable[pPixel]
    else:
        print('Error: Invalid precipitation map color value: ' + str(pPixel))
        sys.exit(0)

# Returns (summer temp, winter temp), (summer precip category, winter precip category)
# tuples from raw pixel data 
def convertPixelData(pxTuple, tempProfile, precProfile, isNorthernHemis):
    if isNorthernHemis:
        return ((getTemperatureCategory(pxTuple[0], tempProfile), getTemperatureCategory(pxTuple[1], tempProfile)), 
                (getPrecipCategory(pxTuple[2], precProfile), getPrecipCategory(pxTuple[3], precProfile)))
    else:
        return ((getTemperatureCategory(pxTuple[1], tempProfile), getTemperatureCategory(pxTuple[0], tempProfile)),
                (getPrecipCategory(pxTuple[3], precProfile), getPrecipCategory(pxTuple[2], precProfile)))

# Returns the climate letter (first part) of the climate classification
# based on the temperature and assuming it is not arid
def getTemperatureType(tempTuple):
    maxTemp = max(tempTuple[0], tempTuple[1])
    minTemp = min(tempTuple[0], tempTuple[1])
    if (minTemp > 18):
        #If cold month has above 18 degrees C
        return 'A'
    elif (maxTemp < 10):
        #If hot month has below 10 degrees C
        return 'E'
    elif (minTemp >= 0):
        #If cold month has above 0 degrees C
        return 'C'
    else:
        return 'D'

# Returns (evaporation estimate R, annual precipitation estimate)
# The aridity threshold formulae are adapted from 'World Map of the Köppen-Geiger 
# climate classification updated', Kottek et al. 2006.
def getEvaEstimate(tempTuple, precTuple):
    tAnn = (tempTuple[0] + tempTuple[1]) / 2.0
    summerPrecip = precTuple[0]
    winterPrecip = precTuple[1]
    summerEst = summerPrecip * 6.0
    winterEst = winterPrecip * 6.0
    annualEst = summerEst + winterEst
    summerPrecipPercent = (summerEst / annualEst) * 100.0
    if (summerPrecipPercent > 66.667):
        return (10.0 * ((2.0 * tAnn) + 28.0), annualEst)
    elif (summerPrecipPercent < 33.333):
        return (10.0 * (2.0 * tAnn), annualEst)
    else:
        return (10.0 * ((2.0 * tAnn) + 14.0), annualEst)

# Returns the precipitation pattern for a pixel's climate class
# for non-arid climates.
def getPrecipitationPattern(tType, tempTuple, precTuple, annualPrecip):
    if (tType == 'A'):
        if ((precTuple[0] > 60) and (precTuple[1] > 60)):
            return 'f'
        else:
            wThresh = 100 - (annualPrecip / 25.0)
            dryPrecip = min(precTuple[0], precTuple[1])
            if (dryPrecip >= wThresh):
                return 'm'
            elif (precTuple[1] < 60):
                return 'w'
            else:
                return 's'
    elif ((tType == 'C') or (tType == 'D')):
        if (precTuple[1] < (precTuple[0] * 0.1)):
            return 'w'
        elif ((precTuple[0] < (precTuple[1] * 0.33)) and (precTuple[0] < 40)):
            return 's'
        else:
            return 'f'
    elif (tType == 'E'):
        if (max(tempTuple[0], tempTuple[1]) < 0):
            return 'F'
        else:
            return 'T'
    else:
        print('Error: invalid climate category for getPrecipitationPattern; should never happen')
        sys.exit(0)

# Gets the seasonal pattern (third letter) for non-A/E climates.
# A or E climates simply return 'x' which is used as a placeholder marker value
def getSeasonalPattern(tType, tempTuple):
    if (tType == 'B'):
            avgTemp = (tempTuple[0] + tempTuple[1]) / 2.0
            if (avgTemp >= 18.0):
                return 'h'
            else:
                return 'k'
    elif (tType == 'C'):
            if (tempTuple[0] >= 22):
                return 'a'
            elif ((tempTuple[1] < 10) and (tempTuple[0] < 13)):
                return 'c'
            else:
                return 'b'
    elif (tType == 'D'):
            if (tempTuple[0] >= 22):
                return 'a'
            elif (tempTuple[1] < -38):
                return 'd'
            elif ((tempTuple[1] < -10) and (tempTuple[0] <= 14)):
                return 'c'
            else:
                return 'b'
    else:
        return 'x'

# Given an input pixel from each input map, returns an output color value
# corresponding to its climate class according to the output profile's color mapping.
def getClimateColor(pxTuple, tempProfile, precProfile, outProfile, isNorthernHemis):
    #pxTuple contains a tuple of four pixels, for (temp1, temp2, precip1, precip2).
    #If either temperature is the ocean color we treat this pixel as ocean and ignore it.
    if ((pxTuple[0] == tempProfile.oceanColor) or (pxTuple[1] == tempProfile.oceanColor)):
        return tempProfile.oceanColor
    else:
        tempTuple, precTuple = convertPixelData(pxTuple, tempProfile, precProfile, isNorthernHemis)
        #Temptuple is (avg. for summer, avg. for winter)
        #precTuple is (category for summer, category for winter)
        tType = getTemperatureType(tempTuple)
        pType = 'f' #Placeholder value

        annualPrecip = 0.0 # Placeholder value
        #Check for aridity (polar climate category exempted)
        if (tType != 'E'):
            evaporation, annualPrecip = getEvaEstimate(tempTuple, precTuple)
            if (annualPrecip < (evaporation / 2.0)):
                tType = 'B'
                pType = 'W'
            elif (annualPrecip < evaporation):
                tType = 'B'
                pType = 'S'

        if (tType != 'B'):
            pType = getPrecipitationPattern(tType, tempTuple, precTuple, annualPrecip)
        
        stType = getSeasonalPattern(tType, tempTuple)

        climateCode = tType + pType
        if (stType != 'x'):
            climateCode = climateCode + stType
        if (climateCode in outProfile.colorTable):
            return outProfile.colorTable[climateCode]
        else:
            print('Error: Invalid Köppen-Geiger climate class (should never happen): ' + climateCode)
            sys.exit(0)

# Returns a function to retrieve the RGB color values of a pixel.
def makeRGBConversion(img1, img2, img3, img4):
    bands = [img1.getbands(), img2.getbands(), img3.getbands(), img4.getbands()]
    bandIds = []
    for bandList in bands:
        if not ('R' in bandList):
            print('Error: No red color channel in one or more input images.')
            sys.exit(0)
        elif not ('G' in bandList):
            print('Error: No green color channel in one or more input images.')
            sys.exit(0)
        elif not ('B' in bandList):
            print('Error: No blue color channel in one or more input images.')
            sys.exit(0)
        else:
            bandIds.append((bandList.index('R'), bandList.index('G'), bandList.index('B')))
    if (bandList[0] == ('R', 'G', 'B')) and (bandList[1] == ('R', 'G', 'B')) and (bandIds[2] == ('R', 'G', 'B')) and (bandIds[3] == ('R', 'G', 'B')):
        # Special case to improve performance if input is all RGB images with no channels
        def retRGB(pxTuple):
            return pxTuple
        return retRGB
    else:
        def getRGB(pxTuple):
            return ((pxTuple[0][bandIds[0][0]], pxTuple[0][bandIds[0][1]], pxTuple[0][bandIds[0][2]]),
                    (pxTuple[1][bandIds[1][0]], pxTuple[1][bandIds[1][1]], pxTuple[1][bandIds[1][2]]),
                    (pxTuple[2][bandIds[2][0]], pxTuple[2][bandIds[2][1]], pxTuple[2][bandIds[2][2]]),
                    (pxTuple[3][bandIds[3][0]], pxTuple[3][bandIds[3][1]], pxTuple[3][bandIds[3][2]]))
        return getRGB
    

# Builds a raw image representing the Köppen-Geiger climate classification based on
# the input temperature and precipitation maps interpreted via the input temperature
# and precipitation color profiles.
def buildClimates(t1name, t2name, p1name, p2name, tempProfile, precProfile, outProfile):
#    try:
        temperature1 = Image.open(t1name)
        temperature2 = Image.open(t2name)
        precipitation1 = Image.open(p1name)
        precipitation2 = Image.open(p2name)
        temps1 = temperature1.getdata()
        temps2 = temperature2.getdata()
        precs1 = precipitation1.getdata()
        precs2 = precipitation2.getdata()
        rawData = zip(temps1, temps2, precs1, precs2)
        getRGBs = makeRGBConversion(temperature1, temperature2, precipitation1, precipitation2)
        newPix = [getClimateColor(getRGBs(pxTuple), tempProfile, precProfile, outProfile, idx < (len(temps1) / 2)) 
                  for idx, pxTuple in enumerate(rawData)]
        climateImg = Image.new('RGB', (temperature1.size[0], temperature1.size[1]))
        climateImg.putdata(newPix)
#    except:
#        print('Error: General error occurred (check input data filenames and correctness)')
#        sys.exit(0)
        return climateImg

# Reads an input profile specification and returns an InputProfile object
# from it.
def readInputProfile(fname):
    try:
        fp = open(fname, 'r')
        profTable = {}
        oceanColor = defaultOceanColor
        try:
            for line in fp:
                if ((line[0] != '#') and (not (line.isspace()))):
                    rmatch = re.match(r"""[^:]*:\s*\(\s*([0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s*)\)\s*:\s*(-?[0-9.]*O?)""", line)
                    if rmatch:
                        iColor = rmatch.group(1)
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
                        if (iValue == 'O'):
                            oceanColor = (rval, gval, bval)
                        else:
                            ival = float(iValue)
                            profTable[(rval, gval, bval)] = ival
                    else:
                        print('Error: Invalid line in input profile: ' + line)
                        sys.exit(0)
        finally:
            fp.close()
    except:
        print('Error: Could not open input profile: ' + fname)
        sys.exit(0)
    return InputProfile(profTable, oceanColor)

# Reads an output profile file and creates an OutputProfile object
# from it.
def readOutputProfile(fname):
    try:
        fp = open(fname, 'r')
        profTable = {}
        try:
            for line in fp:
                if ((line[0] != '#') and (not (line.isspace()))):
                    rmatch = re.match(r"""\s*([A-Za-z]+)\s*:\s*\(\s*([0-9]+\s*,\s*[0-9]+\s*,\s*[0-9]+\s*)\s*\)""", line)
                    if rmatch:
                        oColor = rmatch.group(2)
                        rgbVals = oColor.split(',')
                        rval = int(rgbVals[0].strip())
                        gval = int(rgbVals[1].strip())
                        bval = int(rgbVals[2].strip())
                        kClass = rmatch.group(1)
                        if (not ((kClass in kColorTableDefault) or (kClass == 'Ocean'))):
                            print('Error: Invalid Köppen-Geiger class in output profile: ' + kClass)
                            sys.exit(0)
                        if (kClass in profTable):
                            print('Warning: Duplicate entries for Köppen-Geiger class ' + kClass + ' in output profile')
                        profTable[kClass] = (rval, gval, bval)
                    else:
                        print('Error: Invalid line in output profile: ' + line)
                        sys.exit(0)
        finally:
            fp.close()
    except:
        print('Error: Could not open output profile: ' + fname)
        sys.exit(0)
    return OutputProfile(profTable)

# Begin script

try:
    options, xarguments = getopt.getopt(sys.argv[1:], 'hvso:t:u:p:q:v:r:k:', ['help', 'version', 'quiet', 'outfile=', 'tempnw=', 
                                                                       'tempns=', 'precnw=', 'precns=', 'tempprof=',
                                                                           'precprof=', 'outprof='])
except getopt.error:
    optErr()

startTime = time.time()

tempFileNameNW = ''
tempFileNameNS = ''
precFileNameNW = ''
precFileNameNS = ''
outfileName = ''

# Set up default color profiles
tempProfile = InputProfile(tColorTableDefault, defaultOceanColor)
precProfile = InputProfile(pColorTableDefault, defaultOceanColor)
outProfile = OutputProfile(kColorTableDefault)

quiet = False

#Parse options
for a in options[:]:
    if a[0] == '-h' or a[0] == '--help':
        usage()
for a in options[:]:
    if a[0] == '-v' or a[0] == '--version':
        version()
for a in options[:]:
    if a[0] == '-o' or a[0] == '--outfile':
        if a[1] == '':
            optErr()
        else:
            outfileName = a[1]
    if a[0] == '-t' or a[0] == '--tempnw':
        if a[1] == '':
            optErr()
        else:
            tempFileNameNW = a[1]
    if a[0] == '-u' or a[0] == '--tempns':
        if a[1] == '':
            optErr()
        else:
            tempFileNameNS = a[1]
    if a[0] == '-p' or a[0] == '--precnw':
        if a[1] == '':
            optErr()
        else:
            precFileNameNW = a[1]
    if a[0] == '-q' or a[0] == '--precns':
        if a[1] == '':
            optErr()
        else:
            precFileNameNS = a[1]
    if a[0] == '-v' or a[0] == '--tempprof':
        if a[1] == '':
            optErr()
        else:
            tempProfile = readInputProfile(a[1])
    if a[0] == '-r' or a[0] == '--precprof':
        if a[1] == '':
            optErr()
        else:
            precProfile = readInputProfile(a[1])
    if a[0] == '-k' or a[0] == '--outprof':
        if a[1] == '':
            optErr()
        else:
            outProfile = readOutputProfile(a[1])
    if a[0] == '-s' or a[0] == '--quiet':
        quiet = True
if ((not tempFileNameNS) or (not tempFileNameNW) or (not precFileNameNS) or (not precFileNameNW)):
    print('Error: One or more required input data files were not specified.')
    sys.exit(0)
if (not outfileName):
    print('Error: No output filename specified.')
    sys.exit(0)
outputToFile(outfileName, buildClimates(tempFileNameNS, tempFileNameNW, precFileNameNS, precFileNameNW, 
                                        tempProfile, precProfile, outProfile))
if not quiet:
    stopTime = time.time()
    timeDiffRounded = format(stopTime - startTime, '.2f')
    print('Output climate map to ' + outfileName + ' (' + timeDiffRounded + 's).')
