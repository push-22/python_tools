import os
import sys
import colorama
from colorama import Fore


def cursor_up(n):
    sys.stdout.write(f'\x1b[{n}A')


def cursor_down(n):
    sys.stdout.write(f'\x1b[{n}B')


colorama.init()
LINES = int(next((arg[2:] for arg in sys.argv if (arg.startswith('/L') or arg.startswith('-L')) and len(arg) >= 3), 20))
NO_COUNT = next((arg[3:] for arg in sys.argv if (arg.startswith('/NC') or arg.startswith('-NC'))), True)
HELP = bool(next((arg for arg in sys.argv if arg == '/?' or arg == '-?'), False))
if HELP:
    fn, _ = os.path.splitext(__file__)
    _, fn = os.path.split(fn)
    print(f'usage: {Fore.LIGHTYELLOW_EX + fn + Fore.RESET} filename [/L/NC/?]')
    print(f'{Fore.LIGHTWHITE_EX}/NC {Fore.YELLOW}don\'t print line count')
    print(f'{Fore.LIGHTWHITE_EX}/L {Fore.YELLOW}number of lines to show')
    print(f'{Fore.LIGHTWHITE_EX}/? {Fore.YELLOW}show this message')
    sys.exit(0)

if len(sys.argv) == 1:
    print('need a file to tail')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print(f'can\'t find {sys.argv[1]}')
    sys.exit(2)

fn = sys.argv[1]
with open(fn) as top:
    for idx in range(1, LINES + 1):
        line = top.readline().strip()
        if not line:
            break
        line_number = f'{Fore.LIGHTMAGENTA_EX + str(idx).rjust(len(str(LINES)))} ' if NO_COUNT else ''
        print(f'{line_number}{Fore.LIGHTCYAN_EX + line}')
