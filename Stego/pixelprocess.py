#https://github.com/rebane2001/rc-tools
#Goes through every pixel of image
import sys
from PIL import Image
from PIL import ImageFilter

filename = sys.argv[1]
im		= Image.open(filename)
pix		= im.load()
width, height = im.size
for h in range(height):
	for w in range(width):
		#Do this with every pixel
		print(w,h,pix[(w,h)])