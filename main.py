#!/usr/bin/env python3

from pathlib import Path
import json
from requests.sessions import Session
from time import sleep
from typing import Iterable
try:
    import huepy  # type: ignore
except ImportError:
    class huepy:
        def good(text: str) -> str:
            return "[+] " + text

        def info(text: str) -> str:
            return "[!] " + text
        
        def bad(text: str) -> str:
            return "[-] " + text

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(it: Iterable) -> Iterable:
        return it

from sys import argv

if len(argv) <= 2:
    print(huepy.bad("Usage: ./main.py <URL> <history file>"))
    exit(1)

url = argv[1]
history_file = Path(argv[2])
if not history_file.exists() or not history_file.is_file():
    print(huepy.bad("The specified path does not exist (or it's not regular file)"))
    exit(1)

current_dir = Path(".")
files_in_current_dir = list(current_dir.iterdir())
if history_file in files_in_current_dir:
    files_in_current_dir.remove(history_file)
if files_in_current_dir:
    print(huepy.info("The current folder is not empty, waiting 10 seconds for you to quit"))
    sleep(10)

with history_file.open("rt") as f:
    history = json.load(f)

session = Session()
try:
    session.get(f"{url}/status").raise_for_status()
except Exception as exc:
    print(huepy.bad(f"Failed to connect to the server: {exc}"))

for pad in tqdm(history):
    id = pad["id"]
    try:
        req = session.get(f"{url}/{id}/download")
        Path(f"{id}.md").write_bytes(req.content)
    except Exception as exc:
        print(huepy.info("Failed to download {id}: {exc}"))

print(huepy.good("Done."))
    
