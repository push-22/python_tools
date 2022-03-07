import os.path

import colorama
from colorama import Fore

colorama.init()

fp, _ = os.path.split(__file__)

with open(os.path.join(fp, "contents.txt")) as cmds:
    print()
    for line in cmds:
        first_comma = line.find(',')
        if first_comma > 0:
            line = line.strip('\r\n')
            cmd, txt = line[:first_comma], line[first_comma + 1:]
            print(f'{Fore.BLUE + cmd:>25}\t{Fore.YELLOW + txt}')
print()
