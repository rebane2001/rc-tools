import os
import sys
if os.name == 'nt':
    script = sys.argv[0].split('\\')[-1]
    args = " ".join('\''+arg.replace('\'','\'\\\'\'')+'\'' for arg in sys.argv[1:])
    exit_code = os.system(f"wsl.exe python3 {script} {args}")
    exit(exit_code)
