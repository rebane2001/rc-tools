#!/usr/bin/python3
#https://github.com/rebane2001/rc-tools
#Attempts to fix a QR code
#You can also apply this script to random images for hilarious laughter
from argparse import ArgumentParser
from PIL import Image
from PIL import ImageFilter

parser = ArgumentParser()
parser.add_argument("qrimage", help="The source QR image you want to fix")
parser.add_argument("qroutput", help="Where to save the fixed QR")
parser.add_argument("-p", help="Add padding to the QR code", action="store_true")
parser.add_argument("-vf", help="Attempt to also fix the version information (0 or 1, pick one or the other)")
parser.add_argument("-ff", help="Attempt to also fix the format information (0 and 1 work the best, but the range is 0-7)")
parser.add_argument("-np", help="Don't fix position info", action="store_true")
parser.add_argument("-na", help="Don't fix alignment info", action="store_true")
parser.add_argument("-nt", help="Don't fix timing info", action="store_true")
try:
    args = parser.parse_args()
except:
    print("(-h for help)")
    raise SystemExit(0)

def apply_pattern(pix, pattern, x1, y1):
    for xi,x2 in enumerate(pattern):
        for yi,y2 in enumerate(x2):
            #y2 == -1 means keep original color
            #if we draw outside the canvas, do not draw outside the canvas
            if y2 == -1 or x1+xi < 0 or y1+yi < 0:
                continue
            try: #prevent out-of-bounds from crashing
                pix[x1+xi,y1+yi] = (y2)
            except:
                pass
    return pix


#Fixed version of:
#https://stackoverflow.com/questions/13238704/calculating-the-position-of-qr-code-alignment-patterns
def alignment_coord_list(size):
    if not (size-17)/4 == round((size-17)/4):
        #The size of a proper QR can only be 17 + x*4 where x is any positive int
        print("Warning: couldn't accurately calculate version, wrong QR code size?")
    version = int((size-17)/4)
    if version == 1:
        return []
    #The stackoverflow answer messes up v36 and v39 align coords
    #This fixes it using Table E.1 from http://www.arscreatio.com/repositorio/images/n_23/SC031-N-1915-18004Text.pdf
    if version == 36:
        return [6, 24, 50, 76, 102, 128, 154]
    if version == 39:
        return [6, 26, 54, 82, 110, 138, 166]
    divs = 2 + version // 7
    total_dist = size - 7 - 6
    divisor = 2 * (divs - 1)
    # Step must be even, for alignment patterns to agree with timing patterns
    step = (total_dist + divisor // 2 + 1) // divisor * 2 # Get the rounding right
    coords = [6]
    for i in range(divs - 2, -1, -1): # divs-2 down to 0, inclusive
        coords.append(size - 7 - i * step)
    return coords

position_marker = [
[1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,1,0,1],
[1,0,1,0,0,0,1,0,1],
[1,0,1,0,0,0,1,0,1],
[1,0,1,0,0,0,1,0,1],
[1,0,1,1,1,1,1,0,1],
[1,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1]]

alignment_marker = [
[0,0,0,0,0],
[0,1,1,1,0],
[0,1,0,1,0],
[0,1,1,1,0],
[0,0,0,0,0]]

filename = args.qrimage
im      = Image.open(filename)
im      = im.convert('1') #convert to black and white
pix     = im.load()
width, height = im.size
if width != height:
    #This message is very funny
    print("Warning: the QR is not square shaped, this is illegal in 67 countries")
if not args.np: #Fix position info
    pix = apply_pattern(pix,position_marker,-1,-1)
    pix = apply_pattern(pix,position_marker,width-8,-1)
    pix = apply_pattern(pix,position_marker,-1,height-8)
if not args.nt: #Fix timing info
    for h in range(height-16):
        pix[(6,h+8)] = (h % 2)
    for w in range(width-16):
        pix[(w+8,6)] = (w % 2)
if not args.na: #Fix alignment info
    alignment_coords = alignment_coord_list(width)
    for x in alignment_coords:
        for y in alignment_coords:
            #uggo code, but it pretty much checks that we don't place the alignment pieces over position info
            if not ((x == alignment_coords[0] and y == alignment_coords[0]) or (x == alignment_coords[0] and y == alignment_coords[-1]) or (x == alignment_coords[-1] and y == alignment_coords[0])):
                pix = apply_pattern(pix,alignment_marker,x-2,y-2)
if not args.vf == None:
    vf = int(args.vf)
    for h in range(6):
        for w in range(3):
            if vf == 0:
                pix[(h,height-11+w)] = pix[(width-11+w,h)]
            else:
                pix[(width-11+w,h)] = pix[(h,height-11+w)]

if not args.ff == None:
    ff = int(args.ff)
    if ff < 4 or ff > 5:
        if ff == 1 or ff == 2 or ff == 7:
            for i in range(6):
                pix[(8,i)] = pix[(width-i-1,8)]
            for i in range(2):
                pix[(8,i+7)] = pix[(width-i-7,8)]
        else:
            for i in range(6):
                pix[(width-i-1,8)] = pix[(8,i)]
            for i in range(2):
                pix[(width-i-7,8)] = pix[(8,i+7)]
    if ff < 6:
        if ff == 1 or ff == 3 or ff == 5:
            for i in range(6):
                pix[(i,8)] =pix[8,(height-i-1)]
            pix[(7,8)] = pix[(8,height-7)]
        else:
            for i in range(6):
                pix[8,(height-i-1)] = pix[(i,8)]
            pix[(8,height-7)] = pix[(7,8)]

if args.p: #Increase the canvas size, so we have a 10px padding
    imn = Image.new("1", (width+20,height+20), (1))
    imn.paste(im, (10,10,10+width,10+height))
    im = imn
im.save(args.qroutput,'PNG')