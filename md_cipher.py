#!/usr/bin/env python3
# md5_cipher.py
# 
# A simple script for cybersecurity beginners to demonstrate MD5 hashing in Python.
# It encrypts a user-provided password using MD5 and displays the hash.

import hashlib  # Standard library for hashing algorithms
import sys      # Provides access to system-specific parameters and functions


def encrypt_md5(password):
    """
    Encrypts a plain-text password using MD5 and returns the hexadecimal digest.
    :param password: The input password string
    :return: MD5 hash as a hex string
    """
    # Encode the password to bytes, then compute MD5
    md5_obj = hashlib.md5(password.encode())
    return md5_obj.hexdigest()


def main():
    """
    Main function: prompts the user for a password and displays its MD5 hash.
    """
    try:
        pwd = input("Enter password to encrypt: ")
        if not pwd:
            print("[!] No password entered. Exiting.")
            sys.exit(1)
        hashed = encrypt_md5(pwd)
        print(f"MD5 hash: {hashed}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)


if __name__ == '__main__':
    main()
