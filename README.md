# Rebane's CTF tools  

This is a set of tools I've written to aid in my tasks, mainly in CTFs  
Feel free to use this stuff, but keep in mind it's very much work in progress and if something doesn't work that's normal  
If you wish to, submit issues and pull reqs

## Tool Overview  
### Decode  
#### decoder.py
A decoding tool, broken atm  
#### missingno.py
A decoding tool, that automatically detects the encoding of a string and decodes it  
It can also work recursively for those CTF challs where some jerk did 42 layers of base64  
Supported encodings: binary, hex, base64, urlsafeb64, brainfuck, urls with rot  
### Generic
#### searchflags.sh  
Looks for a CTF flag recursively through all files and their `strings`  
Looks for plaintext and hex, b64 planned  
Only works on Linux or WSL  
### Stego  
#### pixelprocess.py  
Processes every pixel of an image  
Useful for writing your own image manipulation/stego tools/scripts  
#### fixqrcode.py  
Attempts to fix a broken QR code to make it readable again  
Supports fixing: position, alignment and timing patterns, version and format information  
#### bruteqrcode.py  
Bruteforces fixing a QR code by using fixqrcode.py
