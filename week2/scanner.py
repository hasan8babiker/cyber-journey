#!/usr/bin/env python3
"""TCP connect port scanner (v1).

Only scan hosts you own or have explicit permission to test
(localhost, your own VMs, scanme.nmap.org, TryHackMe/lab machines).

Usage:
    python3 scanner.py 127.0.0.1
    python3 scanner.py scanme.nmap.org -p 1-1024 -t 0.5 -w 200
    python3 scanner.py 10.10.10.10 -p 22,80,443,8000-8100 -o results.txt
"""
import argparse
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def parse_ports(spec: str) -> list[int]:
    """Turn '22,80,100-200' into a sorted list of unique ports."""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            lo, hi = int(lo), int(hi)
            if lo > hi:
                lo, hi = hi, lo
            ports.update(range(lo, hi + 1))
        else:
            ports.add(int(part))
    bad = [p for p in ports if not 1 <= p <= 65535]
    if bad:
        raise ValueError(f"ports out of range 1-65535: {bad[:5]}")
    return sorted(ports)


def scan_port(host: str, port: int, timeout: float) -> bool:
    """Return True if a full TCP connection to host:port succeeds."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except OSError:
        return False


def service_name(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description="TCP connect port scanner")
    ap.add_argument("host", help="target hostname or IPv4 address")
    ap.add_argument("-p", "--ports", default="1-1024",
                    help="ports, e.g. 22,80,443 or 1-1024 (default 1-1024)")
    ap.add_argument("-t", "--timeout", type=float, default=1.0,
                    help="seconds to wait per port (default 1.0)")
    ap.add_argument("-w", "--workers", type=int, default=100,
                    help="concurrent connections (default 100)")
    ap.add_argument("-o", "--output", help="also write results to this file")
    args = ap.parse_args()

    try:
        ports = parse_ports(args.ports)
        ip = socket.gethostbyname(args.host)
    except (ValueError, socket.gaierror) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    print(f"Scanning {args.host} ({ip}), {len(ports)} ports, "
          f"timeout {args.timeout}s, {args.workers} workers")
    start = time.time()

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = pool.map(lambda p: (p, scan_port(ip, p, args.timeout)), ports)
            open_ports = [p for p, is_open in results if is_open]
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130

    elapsed = time.time() - start
    lines = [f"{'PORT':<11}{'STATE':<7}SERVICE"]
    lines += [f"{f'{p}/tcp':<11}{'open':<7}{service_name(p)}" for p in open_ports]
    lines.append(f"\n{len(open_ports)} open / {len(ports)} scanned in {elapsed:.2f}s")
    report = "\n".join(lines)
    print(report)

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"Target: {args.host} ({ip})\n{report}\n")
        print(f"Saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
