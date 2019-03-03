#!/usr/bin/python3
#https://github.com/rebane2001/rc-tools
#Has lots of different decodes for ez access


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

#Code from:
#https://eddmann.com/posts/implementing-rot13-and-rot-n-caesar-ciphers-in-python/
def rot(n):
    from string import ascii_lowercase as lc, ascii_uppercase as uc
    lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return lambda s: s.translate(lookup)

if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"encoding string")
    print("List of encodings: rot, b64, bin, hex, bf")
else:
	enc = sys.argv[1]
	s = sys.argv[2]
	if enc == "rot":
		for x in range(26):
			print(rot(x)(s))
	if enc == "b64":
        missing_padding = len(s) % 4
        if missing_padding:
            s += "="* (4 - missing_padding)
        print(base64.b64decode(s.replace(" ","")))
    if enc == "bin":
    	print("this script is very Work IN PROGRES!")