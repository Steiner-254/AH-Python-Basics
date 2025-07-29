#!/usr/bin/env python3
# parse_logs.py
#
# Usage:
#   python3 parse_logs.py -file logs.txt
#
# Reads the given logs file and extracts any lines that look like they
# contain a username and password.

import argparse
import re
import sys

def parse_args():
    """
    Set up command-line argument parsing.
    Requires exactly one argument: -file <path_to_logs>
    """
    parser = argparse.ArgumentParser(description="Parse logs for usernames and passwords")
    parser.add_argument(
        "-file",
        required=True,
        help="Path to the logs file to analyze"
    )
    return parser.parse_args()

def load_logs(path):
    """
    Reads all lines from the given file path.
    Exits with an error message if the file cannot be opened.
    """
    try:
        with open(path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"[!] Error: File not found: {path}")
        sys.exit(1)
    except IOError as e:
        print(f"[!] Error reading {path}: {e}")
        sys.exit(1)

def find_credentials(lines):
    """
    Scans each line for patterns like:
      USER=alice; PASS=secret123
      username: bob password: hunter2
      login failed for charlie/letmein
    Returns a list of tuples: (line_number, username, password)
    """
    creds = []
    # A few regex patterns to catch common log formats
    patterns = [
        re.compile(r"USER\s*=\s*(?P<user>\w+)\s*;\s*PASS\s*=\s*(?P<pass>\S+)", re.IGNORECASE),
        re.compile(r"username\s*:\s*(?P<user>\w+)\s+password\s*:\s*(?P<pass>\S+)", re.IGNORECASE),
        re.compile(r"login (?:succeeded|failed) for\s+(?P<user>\w+)[/\\](?P<pass>\S+)", re.IGNORECASE),
    ]

    for idx, line in enumerate(lines, start=1):
        for pat in patterns:
            m = pat.search(line)
            if m:
                creds.append((idx, m.group("user"), m.group("pass")))
                break  # stop after first match per line

    return creds

def main():
    """
    Main workflow:
    1. Parse arguments
    2. Load log lines
    3. Extract credentials
    4. Print any found usernames/passwords
    """
    args = parse_args()
    lines = load_logs(args.file)
    creds = find_credentials(lines)

    if not creds:
        print("[*] No credentials found in the log.")
    else:
        print(f"[*] Found {len(creds)} credential entr{'y' if len(creds)==1 else 'ies'}:\n")
        for lineno, user, pwd in creds:
            print(f"  Line {lineno}: username = {user!r}, password = {pwd!r}")

if __name__ == "__main__":
    main()
