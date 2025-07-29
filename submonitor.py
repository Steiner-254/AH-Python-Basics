#!/usr/bin/env python3
"""
Incremental Subdomain Enumerator using subfinder.

This script prompts for a target domain, then uses the external 'subfinder'
 tool to pull subdomains. The first run writes all found subdomains to
 '<domain>.txt'. Every 30 seconds it repeats, computes the difference vs. the
 last snapshot, and if there are any new subdomains, writes them to
 '<domain>1.txt', '<domain>2.txt', etc., incrementing the counter each time.
# Additionally, after discovering new subs, it updates the baseline file
# (domain.txt) to include all known subdomains for more accurate diffs.

Requirements:
  - Python 3.6+
  - subfinder installed and in your PATH:
      https://github.com/projectdiscovery/subfinder

Usage:
    python3 script.py
"""

import subprocess
import time
import sys
from pathlib import Path


def run_subfinder(domain: str) -> set:
    """
    Run 'subfinder -d <domain> -silent' and return a set of subdomains.
    """
    try:
        # Call subfinder silently
        completed = subprocess.run(
            ["subfinder", "-d", domain, "-silent"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True
        )
        # Parse and return unique subdomains
        return set(line.strip() for line in completed.stdout.splitlines() if line.strip())
    except subprocess.CalledProcessError as e:
        print(f"[!] subfinder failed: {e}", file=sys.stderr)
        return set()


def save_list(items: set, filename: Path):
    """
    Save each item in the set to a file, one per line, sorted.
    """
    with filename.open("w") as f:
        for sub in sorted(items):
            f.write(sub + "\n")
    print(f"[+] Wrote {len(items)} entries to {filename}")


def main():
    # Prompt for the target domain
    domain = input("Enter the domain to enumerate (e.g. example.com): ").strip()
    if not domain:
        print("[-] No domain provided, exiting.")
        sys.exit(1)

    # Prepare filenames and output directory
    base_name = domain.replace('.', '_')
    out_dir = Path.cwd() / f"{base_name}_subs"
    out_dir.mkdir(exist_ok=True)
    baseline_file = out_dir / f"{base_name}.txt"
    print(f"[+] Output directory: {out_dir}")

    # Initial enumeration
    print(f"[>] Running initial enumeration for {domain}...")
    previous = run_subfinder(domain)
    save_list(previous, baseline_file)

    counter = 1

    try:
        while True:
            print(f"[>] Sleeping 30s before next enumeration...")
            time.sleep(30)

            print(f"[>] Running enumeration #{counter + 1} for {domain}...")
            current = run_subfinder(domain)

            # New subdomains = current minus previous
            new_subs = current - previous
            if new_subs:
                # Save only the new subdomains
                incremental_file = out_dir / f"{base_name}{counter}.txt"
                save_list(new_subs, incremental_file)

                # Update baseline set and file for future diffs
                previous |= new_subs
                save_list(previous, baseline_file)

                counter += 1
            else:
                print("[*] No new subdomains found.")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
