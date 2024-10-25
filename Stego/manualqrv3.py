#!/usr/bin/python3
#https://github.com/rebane2001/rc-tools
import sys
from PIL import Image

if not len(sys.argv) == 2:
    print("Usage:",sys.argv[0],"qrfile.png")
    raise SystemExit(0)
filename = sys.argv[1]

SHAPE_RECT_UP = [
    [0,1],
    [2,3],
    [4,5],
    [6,7],
]
SHAPE_RECT_DOWN = [
    [6,7],
    [4,5],
    [2,3],
    [0,1],
]
SHAPE_RECT_DOWN_TALL = [
    [6,7],
    [4,5],
    [9,9],
    [9,9],
    [9,9],
    [9,9],
    [9,9],
    [2,3],
    [0,1],
]

SHAPE_SKEW_UP = [
    [9,0],
    [1,2],
    [3,4],
    [5,6],
    [7,9],
]
SHAPE_SKEW_DOWN = [
    [7,9],
    [5,6],
    [3,4],
    [1,2],
    [9,0],
]
SHAPE_SKEW_UP_GAP = [
    [9,0],
    [1,2],
    [3,4],
    [9,9],
    [5,6],
    [7,9],
]
SHAPE_SKEW_DOWN_GAP = [
    [7,9],
    [5,6],
    [9,9],
    [3,4],
    [1,2],
    [9,0],
]

SHAPE_SKEW_UP_LEFT = [
    [0,1,2],
    [9,3,4],
    [9,5,6],
    [9,7,9],
]

SHAPE_SNUG_UP = [
    [0,],
    [1,],
    [2,],
    [3,],
    [4,5],
    [6,7],
]

SHAPE_UP_LEFT = [
    [0,1,2,3],
    [9,9,4,5],
    [9,9,6,7],
]

SHAPE_RECT_LEFT = [
    [0,1,6,7],
    [2,3,4,5],
]

MASK_PATTERNS = [
    ("j%3",            lambda i,j: j%3==0),
    ("(i+j)%3",        lambda i,j: (i+j)%3==0),
    ("(i+j)%2",        lambda i,j: (i+j)%2==0),
    ("i%2",            lambda i,j: i%2==0),
    ("((i*j)%3+i*j)%2",lambda i,j: ((i*j)%3+i*j)%2==0),
    ("((i*j)%3+i+j)%2",lambda i,j: ((i*j)%3+i+j)%2==0),
    ("(i//2 + j//3)%2",lambda i,j: (i//2 + j//3)%2==0),
    ("(i*j)%2+(i*j)%3",lambda i,j: (i*j)%2+(i*j)%3==0),
]

ENCODINGS = [
[8,"End of message"], # 0 = 0b0000
[10,"Numeric"], # 1 = 0b0001
[9,"Alphanumeric"], # 2 = 0b0010
[8,"Structured append"], # 3 = 0b0011
[8,"Byte encoding"], # 4 = 0b0100
[8,"FNC1 in first position"], # 5 = 0b0101
[8,"ECI"], # 7 = 0b0111
[8,"Kanji encoding"], # 8 = 0b1000
[8,"FNC1 in second position"], # 9 = 0b1001
]

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def read_block(pix,x,y,shape):
    bin_out = 0
    for y1, shape_line in enumerate(shape):
        for x1, shape_val in enumerate(shape_line):
            if shape_val > 7:
                continue
            if pix[(x+x1,y+y1)][0] < 128:
                bin_out += 1<<shape_val
    return bin_out

for MASK_PATTERN in MASK_PATTERNS:
    im      = Image.open("qr_test.png").convert("RGB")
    pix     = im.load()
    width, height = im.size

    for h in range(height):
        for w in range(width):
            is_black = pix[(w,h)][0] < 128
            pix[(w,h)] = (255,255,255) if is_black == MASK_PATTERN[1](h,w) else (0,0,0)

    # read v3 code
    data = [
        read_block(pix,width-2,height-4,SHAPE_RECT_UP),
        read_block(pix,width-2,height-4*3,SHAPE_RECT_UP),
        read_block(pix,width-2,height-4*5,SHAPE_RECT_UP),
        read_block(pix,width-2*2,height-4*4,SHAPE_RECT_DOWN),
        read_block(pix,width-2*2,height-4*2,SHAPE_RECT_DOWN),
        read_block(pix,width-2*3,height-4,SHAPE_RECT_UP),
        read_block(pix,width-2*3,height-4*4-1,SHAPE_RECT_UP),
        read_block(pix,width-2*4,height-4*5+1,SHAPE_RECT_DOWN),
        read_block(pix,width-2*4,height-4*3+1,SHAPE_RECT_DOWN_TALL),
        read_block(pix,width-2*5,height-4*2,SHAPE_SNUG_UP),
        read_block(pix,width-2*5,height-4*4-1,SHAPE_SKEW_UP),
        read_block(pix,width-2*5,height-4*6-2,SHAPE_SKEW_UP_GAP),
        read_block(pix,width-2*6,0,SHAPE_SKEW_DOWN),

        read_block(pix,width-2,height-4*2,SHAPE_RECT_UP),
        read_block(pix,width-2,height-4*4,SHAPE_RECT_UP),
        read_block(pix,width-2*2,height-4*5,SHAPE_RECT_DOWN),
        read_block(pix,width-2*2,height-4*3,SHAPE_RECT_DOWN),
        read_block(pix,width-2*2,height-4*1,SHAPE_RECT_DOWN),
        read_block(pix,width-2*3,height-4*3-1,SHAPE_RECT_UP),
        read_block(pix,width-2*3-2,height-4*5,SHAPE_UP_LEFT),
        read_block(pix,width-2*4,height-4*4+1,SHAPE_RECT_DOWN),
        read_block(pix,width-2*5,height-2,SHAPE_RECT_LEFT),
        read_block(pix,width-2*5,height-4*3-1,SHAPE_SKEW_UP),
        read_block(pix,width-2*5,height-4*5-1,SHAPE_SKEW_UP),
        read_block(pix,width-2*5-1,0,SHAPE_SKEW_UP_LEFT),
        read_block(pix,width-2*6,4,SHAPE_SKEW_DOWN_GAP),
    ]
    
    data_bin_str = ""
    for d in data:
        data_bin_str += "{:08b}".format(d)
    #print(data_bin_str)
    encoding_type = (data[0] & 0b11110000)>>4
    data_length = ((data[0] & 0b1111)<<4) + ((data[1] & 0b11110000)>>4)

    print(f"===")
    print("Mask:",MASK_PATTERN[0])
    print("Enc:",ENCODINGS[encoding_type][1] if encoding_type < 10 else f"INVALID ENCODING ({encoding_type})")
    print("Len:",data_length)
    #print(ENCODINGS[encoding_type] if encoding_type < 10 else f"INVALID ENCODING ({encoding_type})")
    #print(bitstring_to_bytes(data_bin_str[4+(ENCODINGS[encoding_type][0] if encoding_type < 10 else 8):]))
    print(bitstring_to_bytes(data_bin_str[4+8:-4]))

#for h in range(height):
#    for w in range(width):
#        #Do this with every pixel
#        print(w,h,pix[(w,h)])