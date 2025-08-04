#!/usr/bin/python3
#https://github.com/rebane2001/rc-tools
#Attempts a lot of different decoding techniques
#Atm supports binary, hex and b64
import sys
import re
import binascii
import base64

r_hex = re.compile(r"^([a-f0-9]+|[A-F0-9]+)$")
r_bin = re.compile(r"^[01 ]+$")
r_b64 = re.compile(r"^[a-zA-Z0-9 =+/-_]+$")
r_bf = re.compile(r"^[+-<>\[\] ]+$")
r_url = re.compile(r".*:\/\/.*")
r_morse = re.compile(r"^[-\./# ) ]+$")

def bits2string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def recursiveDecode(s,i):
    global r_hex
    global r_bin
    global r_b64
    print(s)
    if i != 0:
        if re.match(r_bin, s):
            try:

                recursiveDecode(bits2string(s.replace(" ","")),i-1)
            except:
                pass
        if re.match(r_morse, s):
            try:

                recursiveDecode(morse(s),i-1)
            except:
                pass
        if re.match(r_bf,s):
            try:
                recursiveDecode(evaluateBF(s.replace(" ","")),i-1)
            except:
                pass
        if re.match(r_hex,s):
            try:
                recursiveDecode(bytearray.fromhex(s).decode("UTF-8"),i-1)
            except:
                pass
        if re.match(r_b64,s):
            try:
                #urlsafeb64 > normal b64
                s = s.replace("-","+").replace("_","/")
                #we fix padding so b64decode doesn't error
                missing_padding = len(s) % 4
                if missing_padding:
                    s += "="* (4 - missing_padding)
                recursiveDecode(base64.b64decode(s.replace(" ","")).decode("UTF-8"),i-1)
            except:
                pass
        if re.match(r_url,s):
            if "http" in s:
                print(s)
            else:
                for x in range(26):
                    if "http" in rot(x)(s):
                        print(rot(x)(s))
                        break

#Code from:
#https://eddmann.com/posts/implementing-rot13-and-rot-n-caesar-ciphers-in-python/
def rot(n):
    from string import ascii_lowercase as lc, ascii_uppercase as uc
    lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return lambda s: s.translate(lookup)

#Code from:
#https://gist.github.com/ebuckley/1842461
morseAlphabet = {
   ".-" : "A",
   "-..." : "B",
   "-.-." : "C",
   "-.." : "D",
   "." : "E",
   "..-." : "F",
   "--." : "G",
   "...." : "H",
   ".." : "I",
   ".---" : "J",
   "-.-" : "K",
   ".-.." : "L",
   "--" : "M",
   "-." : "N",
   "---" : "O",
   ".--." : "P",
   "--.-" : "Q",
   ".-." : "R",
   "..." : "S",
   "-" : "T",
   "..-" : "U",
   "...-" : "V",
   ".--" : "W",
   "-..-" : "X",
   "-.--" : "Y",
   "--.." : "Z",
   "/" : " ",
   ".----" : "1",
   "..---" : "2",
   "...--" : "3",
   "....-" : "4",
   "....." : "5",
   "-...." : "6",
   "--..." : "7",
   "---.." : "8",
   "----." : "9",
   "-----" : "0",
   ".-.-.-" : ".",
   "--..--" : ",",
   "---..." : ":",
   "..--.." : "?",
   ".----." : "'",
   "-....-" : "-",
   "-..-." : "/",
   ".--.-." : "@",
   "-...-" : "="
}
def morse(message):
    messageSeparated = message.split(' ')
    decodeMessage = ''
    for char in messageSeparated:
        if char in morseAlphabet:
            decodeMessage += morseAlphabet[char]
        else:
            # CNF = Character not found
            decodeMessage += '<CNF>'
    return decodeMessage

### Brainfuck code, original not by Rebane, here are the credits of the guy who made this:
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
# https://github.com/pocmo/Python-Brainfuck
def evaluateBF(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)
  cells, codeptr, cellptr = [0], 0, 0
  output = ""
  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": output += chr(cells[cellptr])
    #if command == ",": cells[cellptr] = ord(getch.getch())  
    codeptr += 1
  return output
def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))
def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap
### BRAINFUCK END

if len(sys.argv) == 2:
    recursiveDecode(sys.argv[1],1)
elif len(sys.argv) != 3:
    print("Usage:",sys.argv[0],"string depth")
else:
    recursiveDecode(sys.argv[1],int(sys.argv[2]))
