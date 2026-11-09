# Week 1: Foundations (2026-10-24 to 2026-10-29)

**Focus:** networking, Linux, Windows, web basics, and first Python/PowerShell tools.

## What I covered
- Networking: OSI model, TCP/IP, encapsulation, DNS, TCP handshake, ports, HTTP
- Linux fundamentals and OverTheWire Bandit (up to level 12)
- Windows fundamentals and failed-logon event analysis
- picoGym General Skills challenges

## What I built
| File | What it does |
|---|---|
| `decoder.py` | Detects and decodes common CTF encodings (hex, decimal, octal, binary, base64, base32, URL, Morse) and Caesar shifts; highlights flags |
| `log_analyzer.py` | Counts failed SSH logins by IP and username from `auth.log` |
| `failed_logons.ps1` | Lists the top source IPs of failed Windows logons (Event ID 4625) |
| `http_inspect.py` | Prints status, headers, redirect chain, and cookies for a URL |
| `port_checker.py` | Checks whether common ports (22, 80, 443) are open on a host |

Notes: `networking-notes.md` | Study cards: `flashcards.md` | Writeups: `writeups/`

## Key lesson
Identify what you are looking at before you act on it (file type, encoding, protocol). Most early challenges are solved by the same loop: identify, decode, repeat.

## Next week
Nmap, Wireshark, and a Python port scanner (Month 2 start).

## Ethics
All testing is done only on systems I own, on intentionally vulnerable lab platforms, or on hosts that explicitly allow it (for example, scanme.nmap.org).