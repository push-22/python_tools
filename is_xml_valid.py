from lxml import etree
import sys
import colorama
from colorama import Fore

colorama.init()

if len(sys.argv) != 2:
    print(Fore.RED + "need a piece of xml to validate")
    sys.exit(9)

try:
    etree.parse(sys.argv[1])
    print(Fore.GREEN + 'looks ok')
except Exception as e:
    print(Fore.RED + str(e))

