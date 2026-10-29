# OverTheWire Bandit: Level 12 → 13
## Challenge link
[Nice netcat... on picoGym](https://overthewire.org/wargames/bandit/bandit13.html)
**Platform:** OverTheWire Bandit | **Difficulty:** Easy-Medium | **Date:** 2026-10-28
**Skills:** hex dumps, file-type identification, compression formats, working in `/tmp`

## Goal
`data.txt` is a hexdump of a file that was compressed over and over. Reverse the hexdump, then unpack every layer until readable text (the next password) appears.

## Tools used
`mktemp`, `cp`, `xxd`, `file`, `mv`, `gzip`, `bzip2`, `tar`, `cat`

## Walkthrough

### Step 1: Work in a private temp directory
The home directory is read-only, so I need a place to write files.
```bash
mkdir $(mktemp -d)        # or: tmp=$(mktemp -d); cd $tmp
cp ~/data.txt .
```
`mktemp -d` gives a random directory name, so other players on the shared server can't collide with or read my work.

### Step 2: Reverse the hexdump
```bash
xxd -r data.txt > data
file data
```
`xxd -r` converts the hex text back into the original binary. `file` reads the first bytes ("magic numbers") and tells me the format. I never trust the filename; the file type decides the next tool.

### Step 3: Peel layers in a loop
Each layer is one of three formats. I repeat `file` → rename → extract until `file` says `ASCII text`.

| `file` says | Do this |
|---|---|
| gzip compressed data | `mv data data.gz && gzip -d data.gz` |
| bzip2 compressed data | `mv data data.bz2 && bzip2 -d data.bz2` |
| POSIX tar archive | `mv data data.tar && tar xf data.tar` (new file appears inside) |

`gzip` and `bzip2` refuse files without the right extension, which is why the rename is needed. After a `tar xf`, a new file appears, so I run `file` on that one next.

### Step 4: Automate the loop
Repeating the same three commands by hand is slow and error-prone, so I wrote `unpack.sh`. It runs `file`, picks the right tool, and repeats until the result is plain text.
```bash
#!/bin/bash
# unpack.sh - peel nested gzip/bzip2/tar layers until plain text appears.
# Usage: run in a /tmp working directory that contains the file "data".
f=data
while true; do
  t=$(file -b "$f")
  case "$t" in
    gzip*)  mv "$f" "$f.gz";  gzip -d "$f.gz" ;;
    bzip2*) mv "$f" "$f.bz2"; bzip2 -d "$f.bz2" ;;
    POSIX\ tar*) mv "$f" "$f.tar"; n=$(tar tf "$f.tar" | head -1); tar xf "$f.tar"; f="$n" ;;
    ASCII*) cat "$f"; break ;;
    *) echo "Unknown type: $t"; break ;;
  esac
done
```
How it works: `file -b` prints the type without the filename, and `case` matches that against each known format. After a `tar` layer it follows the new filename from `tar tf`. Any unexpected type stops the loop with a message instead of failing silently.

### Step 5: Read the result
When `file` reports `ASCII text`, the script prints it, and that is the password for level 13.
*(Password not shown on purpose; see the note below.)*

## What I learned
- **Automate repetitive steps.** If I do the same thing three times, I script it. That is how `unpack.sh` came about.
- **Identify before acting.** `file` tells me the real format; the extension can lie.
- **Layered or nested encoding is common in CTFs.** The method is always: identify, decode, repeat. I turned this idea into `decoder.py`.
- The first few layers were fine by hand, but by the fourth it was repetitive and easy to mistype. That’s why I wrote unpack.sh.

“I didn’t expect the file to be compressed so many times.” Use it only if it’s real.

## How to defend against it / real-world relevance
Attackers and malware authors nest compression and encoding to evade simple signature scanning. Security tools unpack archives recursively and inspect each layer, with depth limits to stop "zip bombs."

## Note on spoilers
OverTheWire asks players not to publish passwords. This writeup explains the method only.