"""
converts minutes (minutes after midnight) to a time of day
"""
from datetime import datetime, date, timedelta
import sys
import colorama
from colorama import Fore


if __name__ == '__main__':

    colorama.init()
    if len(sys.argv) <= 1:
        print(Fore.RED + 'need some minutes/seconds to convert\n')
        print(Fore.RED + 'seconds should end in s')
        sys.exit(1)

    do_secs = sys.argv[1].endswith('s')
    if do_secs:
        num = sys.argv[1][:-1]
    else:
        num = sys.argv[1]

    tod = datetime.combine(date.today(), datetime.min.time())
    if num.lower() == 'now':
        print(int((datetime.now() - tod).total_seconds() / 60))
    else:
        try:
            num = int(num)
        except ValueError:
            print(Fore.RED + f"could not convert '{sys.argv[1]}' to an int")
            sys.exit(1)
        print(tod + timedelta(minutes=num))
