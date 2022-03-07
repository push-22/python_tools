import sys
from pathlib import Path

try:
    Path(sys.argv[1]).touch()
except OSError as ose:
    print(ose)
