#!/usr/bin/python3
# rc-tools | pixelprocess_universal.py
from PIL import Image

# im = Image.open("file.png")
im = Image.new("RGB", (512, 512), "white")
pix = im.load()
width, height = im.size
for h in range(height):
    for w in range(width):
        # Get pixel value
        print(w,h,pix[(w,h)])
        # Set pixel value
        pix[(w,h)] = (255, 255, 255)

im.show()
#im.save("out.png","PNG")
