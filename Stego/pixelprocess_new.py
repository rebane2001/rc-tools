#!/usr/bin/python3
#https://github.com/rebane2001/rc-tools
#Generates a new image
import sys
from PIL import Image
from PIL import ImageFilter

im		= Image.new("RGB", (512, 512), "white")
pix		= im.load()
width, height = im.size
for h in range(height):
	for w in range(width):
		#Do this with every pixel
		pix[(w,h)] = (255, 255, 255) #(R, G, B)
im.save("out.png","PNG")