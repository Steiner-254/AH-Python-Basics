#!/usr/bin/env python3
"""
Simple domain-liveness checker.

This script prompts the user for a domain (or IP), then attempts to ping it
once every 10 seconds. If the ping succeeds, it prints a message indicating
the domain is live.
"""

import subprocess
import time
import platform

def is_live(domain: str) -> bool:
    """
    Ping the given domain once and return True if it responds.

    Uses the system 'ping' command with a single packet.
    Works on Unix-like systems and Windows.
    """
    # Determine the correct flag for count based on OS
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Build the ping command
    cmd = ['ping', param, '1', domain]

    # Suppress output by redirecting to DEVNULL
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # returncode 0 means at least one reply was received
        return result.returncode == 0
    except Exception:
        # In case ping command is not available or fails unexpectedly
        return False

def main():
    """
    Main loop: ask for domain, then ping every 10 seconds.
    """
    # Prompt the user
    domain = input("Enter the domain or IP address to check: ").strip()

    # Inform the user that the loop has started
    print(f"Checking '{domain}' every 10 seconds. Press Ctrl+C to stop.")

    # Loop indefinitely
    while True:
        if is_live(domain):
            # Print only when the host is reachable
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {domain} is live!")
        # Wait for 10 seconds before the next check
        time.sleep(10)

if __name__ == "__main__":
    main()
