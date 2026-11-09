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