import pyperclip
import time
import re
import subprocess
import winsound

print("Waiting for a hashcat value on the clipboard...")
while True:
    clipboard_contents = pyperclip.paste()
    match = re.search(r"hashcash -[mCb0-9]+ (\"?)[0-9a-f]+\1", clipboard_contents)
    if match:
        print(f"Running {match[0]}...")
        winsound.Beep(1500, 100)
        time.sleep(0.02)
        winsound.Beep(1500, 100)
        result = subprocess.check_output(['wsl', *match[0].split(" ")])
        result = result.decode().strip()
        winsound.Beep(1300, 100)
        winsound.Beep(1500, 75)
        winsound.Beep(1750, 150)
        print(f"Got {result}!")
        pyperclip.copy(result)
    time.sleep(1)