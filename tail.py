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
NEXT_UPDATE = int(next((a[2:] for a in sys.argv if (a.startswith('/T') or a.startswith('-T')) and len(a) >= 3), 5))
LINES = int(next((a[2:] for a in sys.argv if (a.startswith('/L') or a.startswith('-L')) and len(a) >= 3), 15))
NO_LINE_NOS = bool(next((a for a in sys.argv if a == '/NL' or a == '-NL'), False))
HELP = bool(next((a for a in sys.argv if a == '/?' or a == '-?'), False))
if HELP:
    fn, _ = os.path.splitext(__file__)
    _, fn = os.path.split(fn)
    print(f'usage: {Fore.LIGHTYELLOW_EX + fn + Fore.RESET} filename [/T/L/?]')
    print(f'{Fore.LIGHTWHITE_EX}/T  {Fore.YELLOW}time between updates')
    print(f'{Fore.LIGHTWHITE_EX}/L  {Fore.YELLOW}number of lines to tail')
    print(f"{Fore.LIGHTWHITE_EX}/NL {Fore.YELLOW}don't display line numbers")
    print(f'{Fore.LIGHTWHITE_EX}/?  {Fore.YELLOW}show this message')
    sys.exit(0)

if len(sys.argv) == 1:
    print('need a file to tail')
    sys.exit(1)

# if not os.path.isfile(sys.argv[1]):
#     print(f'can\'t find {sys.argv[1]}')
#     sys.exit(2)


def trim_string(s: str, limit: int, dotdotdot='…') -> str:
    # s = Fore.LIGHTBLACK_EX + ("D" * limit)
    s = s[:limit - len(dotdotdot)] + dotdotdot if len(s) > limit else s
    return s


# if the output has been redirected elsewhere then
# DON'T DISPLAY LINE NUMBER
# DON'T DO ANYTHING THAT WILL BREAK THE APP (os.get_terminal_size)
# DON'T BOTHER TO DO THE TAIL CONTINUOUSLY
has_been_redirected = not os.isatty(sys.__stdout__.fileno())
if has_been_redirected:
    NO_LINE_NOS = True

with HiddenCursor():  # hide the cursor
    try:
        fn = sys.argv[1]
        counter = 0

        # read the file, if there's no file display ?s
        # else display what lines the file has in it
        # always display the asked for amount of lines even if blank
        while True:
            counter += 1

            if has_been_redirected:
                num_columns = 200
            else:
                tsize = os.get_terminal_size(sys.__stdout__.fileno())
                num_columns = tsize.columns

            # output if the file doesn't exist
            out = []
            line_no_len = len(str(LINES)) + 1
            for idx in range(0, LINES):
                out.append("?" * (num_columns - line_no_len))
            got_file_data = False

            # merge the file contents into the output
            if os.path.isfile(fn):
                with open(fn) as log:
                    lines = log.readlines()
                    if len(lines):
                        got_file_data = True
                        lines = lines[-LINES:]
                        start = len(out) - len(lines)
                        lidx = 0
                        for idx, line in enumerate(range(0, LINES)):
                            if idx < start:
                                out[idx] = (" " * (num_columns - line_no_len))
                            else:
                                out[idx] = lines[lidx].strip()
                                lidx += 1

            # now print the lines to the screen
            if not has_been_redirected:
                line_clr = Fore.LIGHTBLACK_EX if not got_file_data else Fore.LIGHTCYAN_EX
                line_no_clr = Fore.LIGHTMAGENTA_EX
            else:
                line_clr = ''
                line_no_clr = ''
                if not got_file_data:
                    sys.exit(0)

            for idx, line in enumerate(out, 1):
                if NO_LINE_NOS:
                    line = line_clr + line if has_been_redirected else line.ljust(num_columns)
                else:
                    line_no = str(idx).rjust(len(str(len(out))))
                    # print the line and using ljust, make sure the line fills the
                    # screen - getting rid of the need to clear the background first
                    line = line_no_clr + f'{line_no} ' + line_clr + line
                    line = line.ljust(num_columns + 10)
                print(trim_string(line, num_columns + 10))

            if has_been_redirected:
                sys.exit(0)
            print(Fore.YELLOW + f'UPDATE #{counter}, CTRL+C to quit')
            time.sleep(NEXT_UPDATE)
            cursor_up(len(out) + 1)  # push the cursor back up to the top to overwrite what's already there

    except KeyboardInterrupt:
        pass
    cursor_down(1)
