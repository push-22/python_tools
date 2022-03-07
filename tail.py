"""read the last N lines of a file and display them, wait some seconde and repeat"""
import os
import sys
import time
import colorama
from colorama import Fore
from cursor import HiddenCursor


def cursor_up(n):
    sys.stdout.write(f'\x1b[{n}A')


def cursor_down(n):
    sys.stdout.write(f'\x1b[{n}B')


colorama.init()
NEXT_UPDATE = int(next((a[2:] for a in sys.argv if (a.startswith('/T') or a.startswith('-T')) and len(a) >= 3), 10))
LINES = int(next((a[2:] for a in sys.argv if (a.startswith('/L') or a.startswith('-L')) and len(a) >= 3), 5))
HELP = bool(next((a for a in sys.argv if a == '/?' or a == '-?'), False))
if HELP:
    fn, _ = os.path.splitext(__file__)
    _, fn = os.path.split(fn)
    print(f'usage: {Fore.LIGHTYELLOW_EX + fn + Fore.RESET} filename [/T/L/?]')
    print(f'{Fore.LIGHTWHITE_EX}/T {Fore.YELLOW}time between updates')
    print(f'{Fore.LIGHTWHITE_EX}/L {Fore.YELLOW}number of lines to tail')
    print(f'{Fore.LIGHTWHITE_EX}/? {Fore.YELLOW}show this message')
    sys.exit(0)

if len(sys.argv) == 1:
    print('need a file to tail')
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print(f'can\'t find {sys.argv[1]}')
    sys.exit(2)


def trim_string(s: str, limit: int, dotdotdot='…') -> str:
    s = s.strip()
    if len(s) > limit:
        return s[:limit].strip() + dotdotdot
    return s


with HiddenCursor():  # hide the cursor
    try:
        fn = sys.argv[1]
        with open(fn) as log:
            counter = 0
            while True:
                counter += 1
                lines = log.readlines()
                out = lines[-LINES:]
                line_start_no = len(lines) - len(out) + 1
                # read the file and take as many of the lines as
                # possible
                # draw the lines of the screen one line at a time
                # make sure each line is wide enough to cover over
                # any previous line that was drawn
                # sleep for requested amount then repeat from the top
                size = os.get_terminal_size(sys.__stdout__.fileno())
                for idx, line in enumerate(out):
                    line_no = str(line_start_no + idx).rjust(len(str(len(lines))))
                    line = Fore.LIGHTMAGENTA_EX + f'{line_no} ' + Fore.LIGHTCYAN_EX + line.strip()
                    # trim the line to fit the screen
                    if len(line) >= size.columns:
                        print(trim_string(line, size.columns))
                    else:
                        # draw the line and pad with space to draw across the whole row
                        print(line.ljust(size.columns))
                print(Fore.BLUE + f'UPDATE #{counter}')
                time.sleep(NEXT_UPDATE)
                log.seek(0, 0)  # begin from the beginning
                cursor_up(len(out) + 1)  # push the cursor back up to the top to overwrite what's already there

    except KeyboardInterrupt:
        pass
    cursor_down(1)
