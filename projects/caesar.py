#!/usr/bin/env python3
"""Caesar cipher tool: encrypt, decrypt, or brute-force all 25 keys.

Examples:
  python caesar.py encrypt "Hello World"            # key defaults to 3
  python caesar.py encrypt "Hello World" -k 7       # specific key
  python caesar.py decrypt "Khoor Zruog"            # key defaults to 3
  python caesar.py decrypt "Khoor Zruog" -k 3
  python caesar.py decrypt "Khoor Zruog" -a         # try all keys
  python caesar.py decrypt -f cipher.txt -a         # text from a file
  echo "Khoor" | python caesar.py decrypt -a        # text from stdin
"""
import argparse
import sys

DEFAULT_KEY = 3


def shift_text(text: str, key: int) -> str:
    """Shift letters by key (positive = forward). Case and non-letters preserved."""
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + key) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + key) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


def encrypt(text: str, key: int = DEFAULT_KEY) -> str:
    return shift_text(text, key)


def decrypt(text: str, key: int = DEFAULT_KEY) -> str:
    return shift_text(text, -key)


def get_text(args) -> str:
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    if args.text is not None:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    sys.exit("error: provide text, --file, or pipe input via stdin")


def main():
    p = argparse.ArgumentParser(description="Caesar cipher encrypt/decrypt tool")
    p.add_argument("mode", choices=["encrypt", "decrypt"], help="operation to perform")
    p.add_argument("text", nargs="?", help="text to process (or use -f / stdin)")
    p.add_argument("-k", "--key", type=int, default=DEFAULT_KEY,
                   help=f"shift key (default: {DEFAULT_KEY})")
    p.add_argument("-a", "--all", action="store_true",
                   help="try all keys 1-25 (brute force)")
    p.add_argument("-f", "--file", help="read input text from a file")
    args = p.parse_args()

    text = get_text(args).rstrip("\n")
    op = encrypt if args.mode == "encrypt" else decrypt

    if args.all:
        for k in range(1, 26):
            print(f"[key {k:2d}] {op(text, k)}")
    else:
        print(op(text, args.key))


if __name__ == "__main__":
    main()