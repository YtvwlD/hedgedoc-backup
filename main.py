#!/usr/bin/env python3

from pathlib import Path
try:
    import huepy  # type: ignore
except ImportError:
    class huepy:
        def bad(text: str) -> str:
            return "[-] " + text
    
from sys import argv

if len(argv) == 1:
    print(huepy.bad("Please specify a history file to load"))
    exit(1)

history_file = Path(argv[1])
if not history_file.exists() or not history_file.is_file():
    print(huepy.bad("The specified path does not exist (or it's not regular file)"))
    exit(1)
