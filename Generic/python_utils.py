# rc-tools | python_utils.py

## long/bytes
from Crypto.Util.number import *
long_to_bytes(1337)
bytes_to_long(b'\x059')

## xor
import math

def xor_bytes(var, key, byteorder=sys.byteorder):
    key = (key*math.ceil(len(var)/len(key)))[:len(var)]
    int_var = int.from_bytes(var, byteorder)
    int_key = int.from_bytes(key, byteorder)
    int_enc = int_var ^ int_key
    return int_enc.to_bytes(len(var), byteorder)
    return bytes(a ^ b for a, b in zip(var, key))

print(xor_bytes(b'\x04\x10^A\x05^\x1fA\x00\x00\x00\x00M', b"lyra"))

## grep
import re

def grep_s(s, pattern, case_insensitive=True, use_regex=True, print_result=True, only_match=False):
    grep_matches = []
    for l in s.split("\n"):
        if use_regex:
            matches = re.findall(pattern, l, flags=(re.IGNORECASE*case_insensitive))
            if len(matches):
                if only_match:
                    for match in matches:
                        grep_matches.append(match)
                        if print_result:
                            print(match)
                else:
                    grep_matches.append(l)
                    if print_result:
                        print(l)
        else:
            if pattern.lower() in l.lower():
                if only_match:
                    for i in range(l.lower().count(pattern.lower())):
                        # note: does not handle case for output!!
                        grep_matches.append(pattern)
                        if print_result:
                            print(pattern)
                else:
                    grep_matches.append(l)
                    if print_result:
                        print(l)
    return grep_matches

print(grep_s("Test t4t foobar toot!\nrandom line\ni love T4T\nyay!", "T..?t", only_match=True))

## rgb to hex
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(c*255) for c in rgb)

print(rgb_to_hex((0.2, 1.0, 0.5)))

## random seeded color
import colorsys
import random

def get_color(t):
    r = random.Random()
    r.seed(t)
    rgb = colorsys.hsv_to_rgb(r.random(), r.random()*0.5 + 0.5, r.random()*0.5 + 0.5)
    return rgb

print(get_color(1337))


## hexdump
import string

def hexdump(data, addr=0, length=-1):
    if length == -1:
        data = data[addr:]
    else:
        data = data[addr:addr+length]
    out = ""
    good_chars = string.printable[:-5].encode()
    while len(data):
        line = data[:0x10]
        line_hex = " ".join(["  " if a >= len(line) else hex(line[a])[2:].zfill(2) for a in range(0x10)])
        line_text = b"".join([line[i:i+1] if line[i:i+1] in good_chars else b"." for i in range(len(line))]).decode()
        out += f"{hex(addr)[2:].zfill(8)}\t{line_hex}\t{line_text}\n"
        data = data[0x10:]
        addr += 0x10
    return out

print(hexdump(b"A"*10 + b"\x00 sample text 123"))
