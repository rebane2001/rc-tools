#!/usr/bin/python3
#https://github.com/rebane2001/rc-tools
#Attempts to brute fixing QR codes using the fixqrcode.py script
#Is missing a feature where it generates vf/ff itself
import os
import sys
from pyzbar.pyzbar import decode
from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool 

def tryqr(vfff):
    vf, ff = vfff
    #print("Trying",vf,ff)
    command = "fixqrcode.py -p "
    fn = (str(vf) + "x" + str(ff) + "qrtemp.png").replace("-","z")
    if not vf == -1:
        command += "-vf " + str(vf) + " "
    if not ff == -1:
        command += "-ff " + str(ff) + " "
    command += sys.argv[1] + " " + fn
    os.system(command)
    dec = decode(Image.open(fn))
    os.remove(fn)
    if len(dec) > 0:
        print(dec)
    return dec
pool = ThreadPool(27) 
parray = []
for vf in range(-1,2):
    for ff in range(-1,8):
        parray.append((vf,ff))
results = pool.map(tryqr, parray)
'''
for r in results:
    if len(r) > 0:
        print(r)
'''