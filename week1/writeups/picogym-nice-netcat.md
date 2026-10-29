# picoGym (General Skills): Nice netcat...


**Platform:** picoCTF / picoGym | **Category:** General Skills | **Difficulty:** Easy | **Date:** 2026-10-28
**Skills:** netcat, ASCII encoding, decoding numbers to text, scripting a decoder

## Goal
Connect to a remote service with `nc`. It prints a list of numbers instead of text. Convert them to readable characters to reveal the flag.

## Tools used
`nc` (netcat), Python, my own `decoder.py`

## Walkthrough

### Step 1: Connect
```bash
nc <host> <port>      # host and port come from the challenge page
```
`nc` opens a raw TCP connection, so I see exactly what the server sends. The output was a series of decimal numbers separated by spaces, with no readable text.

### Step 2: Recognize the encoding
Every number was between roughly 32 and 126. That is the **printable ASCII range**, so each number is one character's decimal code (for example, 65 = `A`, 123 = `{`).

### Step 3: Decode
Quick way in Python:
```python
nums = "<paste the numbers here>"
print("".join(chr(int(n)) for n in nums.split()))
```
`chr()` converts a code to its character. I also confirmed the result with my own tool:
```bash
python decoder.py <paste the numbers here>
```
`decoder.py` auto-detects decimal ASCII and highlights anything shaped like `picoCTF{...}`.

### Step 4: Submit the flag
The decoded text had the `picoCTF{...}` format. *(Flag not shown on purpose.)*

## What I learned
- Numbers in the 32-126 range are a strong hint for ASCII; hex pairs (`70 69 63 6f`) and binary are the same idea in other bases.
- Building the tool first paid off: the same decoder now solves a whole class of challenges.

## How to defend against it / real-world relevance
Encoding is not encryption. Anyone who sees the numbers can reverse them in seconds. Never "protect" credentials or tokens by only encoding them (base64, hex, ASCII codes); use proper encryption or hashing.
