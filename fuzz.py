#!/usr/bin/env python3

import requests
import argparse
import sys

def parse_arguments():
    """
    Parses command-line arguments. Requires a wordlist file with the -wordlist flag.
    """
    parser = argparse.ArgumentParser(description="Simple URL fuzzing tool")
    parser.add_argument("-wordlist", required=True, help="Path to the fuzz wordlist file")
    return parser.parse_args()

def load_wordlist(file_path):
    """
    Reads the wordlist file and returns a list of words.
    Each word will be appended to the target domain.
    """
    try:
        with open(file_path, "r") as file:
            words = [line.strip() for line in file if line.strip()]
            return words
    except FileNotFoundError:
        print(f"[!] Wordlist file not found: {file_path}")
        sys.exit(1)

def fuzz_domain(domain, wordlist):
    """
    Appends each word in the wordlist to the domain and makes HTTP requests.
    Displays the status code for each request.
    """
    print(f"\n[+] Starting fuzzing on: {domain}\n")
    
    for word in wordlist:
        url = f"{domain.rstrip('/')}/{word}"  # Ensure no double slashes
        try:
            response = requests.get(url, timeout=5)
            print(f"[{response.status_code}] {url}")
        except requests.RequestException as e:
            print(f"[!] Error accessing {url}: {e}")

def main():
    """
    Main function: parses args, loads wordlist, prompts for domain, and runs fuzzing.
    """
    args = parse_arguments()
    wordlist = load_wordlist(args.wordlist)
    
    domain = input("Enter the full domain or subdomain (e.g., http://example.com): ").strip()
    
    # Basic validation
    if not domain.startswith("http://") and not domain.startswith("https://"):
        print("[!] Please include http:// or https:// in the domain.")
        sys.exit(1)
    
    fuzz_domain(domain, wordlist)

if __name__ == "__main__":
    main()
