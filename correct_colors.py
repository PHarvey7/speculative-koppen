# (c) 2020 CTA5816 (see LICENSE.txt)

from PIL import Image # import graphics processor
import argparse
import re
import numpy as np # import numpy

# accept command-line arguments
parser = argparse.ArgumentParser(description='Convert non-standard colors in input image to nearest standard colors')
parser.add_argument('input_img', metavar='i', type=str, help='input image filepath')
parser.add_argument('output_img', metavar='o', type=str, help='output image filepath')
parser.add_argument('colors', metavar='c', type=str, help='color profile filepath')
parser.add_argument('--wrap', metavar='w', type=str, help='longitude axis (x or y)')

args = parser.parse_args()

# parse input text file
def readInputProfile(fname):
    fp = open(fname, 'r')
    profTable = []
    try:
        for line in fp:
            if ((line[0] != '#') and (not (line.isspace()))):
                rmatch = re.match(r"""[^:]*:\s*\(([0-9]+,\s*[0-9]+,\s*[0-9]+\s*)\)\s*:\s*(-?[0-9.]*X?O?)""", line)
                if rmatch:
                    iColor = rmatch.group(1)
                    rgbVals = iColor.split(',')
                    rval = int(rgbVals[0].strip())
                    gval = int(rgbVals[1].strip())
                    bval = int(rgbVals[2].strip())
                    if ((rval < 0) or (rval > 255) or (gval < 0) or (gval > 255) or (bval < 0) or (bval > 255)):
                        raise ValueError('Invalid RGB color in input profile: ' + str((rval, gval, bval)))
                    if ((rval, gval, bval) in profTable):
                        print('Warning: Duplicate color in input profile: ' + str((rval, gval, bval)))
                    else:
                        profTable += [(rval, gval, bval)]
                else:
                    raise ValueError('Invalid line in input profile: ' + line)
    finally:
        fp.close()
    return profTable

img_name = args.input_img # input image filepath
color_file = args.colors
colors = readInputProfile(color_file)# set valid colors
wrap = args.wrap
print(wrap)

# open image
im = Image.open(img_name)
pixels = im.load()
print("Loaded image")

# initialize pixel discriminator
sieve = np.zeros((len(colors), im.size[0], im.size[1]))
for i in range(0, len(colors)):
    for j in range(0, im.size[0]):
        for k in range(0, im.size[1]):
            sieve[i,j,k] = pixels[j,k][0:3] == colors[i]
print("Sieve created")
            
def get_pval(loc): # determine whether the color of a given pixel is valid
    # Inputs
    #   loc (np.array, shape=(2)): pixel location
    # Outputs
    #   val (int): index (in colors) of the input pixel's color OR None if not a valid color
    val = None
    for i in range(0,len(sieve)):
        if sieve[i, loc[0], loc[1]]:
            val = i
    return val

def correct(loc): # modify the color of a given pixel to match its nearest valid neighbor
    # Inputs
    # loc (np.array, shape=(2)): pixel location
    # Outputs
    # n_col (int): index (in pcolors) of the nearest valid color
    n_col = None
    pos = np.copy(loc)
    i = 0
    steps = 0
    d = np.array([-1,1])
    ax = np.array([0,0,1])
    while n_col == None: # iterate through nearest pixels in an expanding pinwheel
        if i == 4*steps: # if one rotation completed, increase radius
            steps += 1
            pos += np.array([-1,0])
            i = 0
        if i%steps == 0: # if one quarter-rotation completed, change direction
            d = np.append(d, 0)
            d = np.cross(d,ax)
            d = d[0:2]
        pos += d
        i += 1
        # modify position to fit coordinates, flooring x- or y-coordinate (user's choice); ensures search does not wrap around north pole to south pole or vice versa
        if wrap == 'x':
            pos = np.array([pos[0]%im.size[0], max(pos[1],0)%im.size[1]]) 
        elif wrap == 'y':
            pos = np.array([max(pos[0],0)%im.size[0], pos[1]%im.size[1]])
        else:
            pos = np.array([max(pos[0],0)%im.size[0], max(pos[1],0)%im.size[1]])
        n_col = get_pval(pos)

    print("Corrected pixel at " + str(loc[0]) + ", " + str(loc[1]) + " with " + str(pos[0]) + ", " + str(pos[1]))
    return n_col
    
for i in range(0, im.size[0]): # iterate through and correct all pixels in image
    for j in range(0, im.size[1]):
        loc = np.array([i,j])
        if get_pval(loc)==None:
            n_col = correct(loc)
            pixels[i,j] = colors[n_col]

new_name = args.output_img # output filepath
im.save(new_name) # save image
