#!/usr/bin/env python3
"""decoder.py - detect and decode common CTF encodings.

Usage:
    python decoder.py -v cipher.txt             # -v shows what it's doing
    python decoder.py cipher.txt                # a file (text or binary)
    python decoder.py "70 69 63 6f 43 54 46"
    python decoder.py 97 99 97 100 101 109 121
    python decoder.py -f cipher.txt -d 6
    echo "YWNhZGVteXt0ZXN0fQ==" | python decoder.py
    python decoder.py --caesar "nxnqjrd"      # show all 25 Caesar shifts
"""
import argparse
import base64
import codecs
import os
import re
import string
import sys
import urllib.parse

FLAG_RE = re.compile(
    r"(?:academy|picoCTF|flag|CTF|THM|HTB)\{[^}\s]{1,200}\}", re.IGNORECASE
)
PRINTABLE = set(string.printable.encode())

MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7",
    "---..": "8", "----.": "9",
}


VERBOSE = False


def log(msg: str):
    """Verbose output goes to stderr so results on stdout stay clean."""
    if VERBOSE:
        print(msg, file=sys.stderr)


def preview(s: str, n: int = 70) -> str:
    s = s.replace("\n", "\\n")
    return repr(s if len(s) <= n else s[:n] + "...")


def printable_ratio(b: bytes) -> float:
    return sum(c in PRINTABLE for c in b) / len(b) if b else 0.0


# ---------- decoders: str -> bytes (raise or return None if not applicable) ----------

def d_hex(s):
    c = re.sub(r"0x|\\x|[\s,:\-]", "", s, flags=re.IGNORECASE)
    if len(c) >= 2 and len(c) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", c):
        return bytes.fromhex(c)


def d_decimal(s):
    t = [x for x in re.split(r"[\s,]+", s.strip()) if x]
    if t and all(x.isascii() and x.isdigit() for x in t):
        v = [int(x) for x in t]
        if all(0 <= n <= 255 for n in v):
            return bytes(v)


def d_octal(s):
    t = [x for x in re.split(r"[\s,]+", s.strip()) if x]
    if t and all(re.fullmatch(r"[0-7]{1,3}", x) for x in t):
        v = [int(x, 8) for x in t]
        if all(n <= 255 for n in v):
            return bytes(v)


def d_binary(s):
    c = re.sub(r"[\s,]", "", s)
    if c and len(c) % 8 == 0 and re.fullmatch(r"[01]+", c):
        return int(c, 2).to_bytes(len(c) // 8, "big")


def d_base64(s):
    c = re.sub(r"\s", "", s)
    if len(c) < 4 or not re.fullmatch(r"[A-Za-z0-9+/_\-]+={0,2}", c):
        return None
    c = c.replace("-", "+").replace("_", "/").rstrip("=")
    c += "=" * (-len(c) % 4)
    return base64.b64decode(c)


def d_base32(s):
    c = re.sub(r"\s", "", s).upper()
    if len(c) < 8 or not re.fullmatch(r"[A-Z2-7]+=*", c):
        return None
    c = c.rstrip("=")
    c += "=" * (-len(c) % 8)
    return base64.b32decode(c)


def d_url(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return urllib.parse.unquote_to_bytes(s)


def d_morse(s):
    if not re.fullmatch(r"[.\-/\s_]+", s) or not re.search(r"[.\-]", s):
        return None
    words = re.split(r"\s*/\s*|\s{3,}", s.strip())
    out = " ".join(
        "".join(MORSE[ch] for ch in w.split()) for w in words
    )
    return out.encode()


DECODERS = {
    "hex": d_hex,
    "decimal": d_decimal,
    "octal": d_octal,
    "binary": d_binary,
    "base64": d_base64,
    "base32": d_base32,
    "url": d_url,
    "morse": d_morse,
}


# ---------- ciphers: only reported when they reveal a flag (they always "look" printable) ----------

def caesar(s, n):
    def shift(ch):
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            return chr((ord(ch) - base + n) % 26 + base)
        return ch
    return "".join(shift(c) for c in s)


def atbash(s):
    def flip(ch):
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            return chr(base + 25 - (ord(ch) - base))
        return ch
    return "".join(flip(c) for c in s)


CIPHERS = {
    "rot13": lambda s: codecs.encode(s, "rot13"),
    "atbash": atbash,
    "reverse": lambda s: s[::-1],
    **{f"caesar+{n}": (lambda s, n=n: caesar(s, n)) for n in range(1, 26) if n != 13},
}


def run(data: str, depth: int):
    """Breadth-first search through decoder chains. Returns list of (chain, text)."""
    results = []
    seen = {data}
    frontier = [(data, [])]
    for level in range(1, depth + 1):
        log(f"=== layer {level}/{depth}: {len(frontier)} candidate(s) to try ===")
        nxt = []
        for text, chain in frontier:
            path = " -> ".join(chain) or "(original input)"
            log(f"[{path}] trying on: {preview(text)}")
            for name, fn in DECODERS.items():
                try:
                    out = fn(text)
                except Exception as e:
                    log(f"    {name:<8} skip: error while decoding ({type(e).__name__})")
                    continue
                if not out:
                    log(f"    {name:<8} skip: input doesn't look like {name}")
                    continue
                ratio = printable_ratio(out)
                if ratio < 0.9:
                    log(f"    {name:<8} skip: output is only {ratio:.0%} printable (junk)")
                    continue
                try:
                    t = out.decode("utf-8").strip()
                except UnicodeDecodeError:
                    log(f"    {name:<8} skip: output isn't valid UTF-8 text")
                    continue
                if not t:
                    log(f"    {name:<8} skip: output is empty")
                    continue
                if t in seen:
                    log(f"    {name:<8} skip: output already seen")
                    continue
                seen.add(t)
                results.append((chain + [name], t))
                nxt.append((t, chain + [name]))
                hit = " <-- FLAG!" if FLAG_RE.search(t) else ""
                log(f"    {name:<8} OK   -> {preview(t)}{hit}")
            if FLAG_RE.search(text):
                log("    ciphers  skipped: this text already contains a flag")
            else:
                hits = 0
                for name, fn in CIPHERS.items():
                    t = fn(text)
                    if FLAG_RE.search(t) and t not in seen:
                        seen.add(t)
                        results.append((chain + [name], t))
                        hits += 1
                        log(f"    {name:<8} OK   -> {preview(t)} <-- FLAG!")
                log(f"    ciphers  tried {len(CIPHERS)} (rot13, atbash, reverse, caesar 1-25): "
                    f"{hits} produced a flag")
        frontier = nxt
        if not frontier:
            log("no new decodings this layer, stopping early")
            break
    return results


def load_file(path: str) -> str:
    """Read a file as text. Binary files: pull out printable strings (like `strings`)."""
    with open(path, "rb") as f:
        raw = f.read()
    if b"\x00" not in raw[:4096]:
        return raw.decode("utf-8", errors="replace").strip()
    found = re.findall(rb"[\x20-\x7e]{6,}", raw)
    print(f"[info] {path} looks binary; scanning {len(found)} printable strings", file=sys.stderr)
    return "\n".join(s.decode() for s in found)


def read_input(args) -> str:
    """Input can be: a file path, plain text, -f FILE, or piped stdin."""
    if args.file:
        return load_file(args.file)
    if args.input:
        joined = " ".join(args.input)
        # a single argument that is an existing file is treated as a file
        if len(args.input) == 1 and os.path.isfile(args.input[0]):
            return load_file(args.input[0])
        return joined
    if sys.stdin.isatty():
        print("Paste input, then press Ctrl-D (Ctrl-Z + Enter on Windows):")
    return sys.stdin.read().strip()


def main():
    ap = argparse.ArgumentParser(description="Detect and decode common CTF encodings.")
    ap.add_argument("input", nargs="*", help="text to decode (or use -f / stdin)")
    ap.add_argument("-f", "--file", help="read input from a file")
    ap.add_argument("-d", "--depth", type=int, default=5, help="max chained decodes (default 5)")
    ap.add_argument("--caesar", action="store_true", help="print all 25 Caesar shifts")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="show every decoder tried and why it passed or was skipped")
    args = ap.parse_args()

    global VERBOSE
    VERBOSE = args.verbose

    data = read_input(args)
    if not data:
        sys.exit("No input.")
    log(f"input: {len(data)} chars, {len(data.splitlines())} line(s): {preview(data)}")

    if args.caesar:
        for n in range(1, 26):
            print(f"+{n:<2} {caesar(data, n)}")
        return

    if FLAG_RE.search(data):
        print(f"[FLAG] already plaintext: {FLAG_RE.search(data).group()}")

    results = run(data, args.depth)
    if not results:
        # fall back to scanning each line and each long token separately
        log("whole-input decode found nothing; scanning each line and long token separately")
        parts = [p.strip() for p in data.splitlines()]
        parts += [t for p in parts for t in p.split() if len(t) >= 8]
        seen_parts = {data}
        for part in parts:
            if part and part not in seen_parts:
                seen_parts.add(part)
                log(f"--- fragment: {preview(part)} ---")
                results += run(part, args.depth)
    if not results:
        print("No decodings found. Try --caesar, or the input may be a different encoding/cipher.")
        return

    # flags first, then shortest chain
    results.sort(key=lambda r: (not FLAG_RE.search(r[1]), len(r[0])))
    for chain, text in results:
        tag = "[FLAG] " if FLAG_RE.search(text) else ""
        shown = text if len(text) <= 300 else text[:300] + "..."
        print(f"{tag}{' -> '.join(chain)}\n    {shown}\n")


if __name__ == "__main__":
    main()
