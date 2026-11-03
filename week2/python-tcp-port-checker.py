#!/usr/bin/env python3
import socket, sys
from concurrent.futures import ThreadPoolExecutor

def check(host, port, timeout=1.0):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return port, s.connect_ex((host, port)) == 0

def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <host> [start_port] [end_port]")
    host = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        sys.exit("Could not resolve host")
    print(f"Scanning {host} ({ip}) ports {start}-{end}")
    with ThreadPoolExecutor(max_workers=100) as ex:
        for port, is_open in ex.map(lambda p: check(ip, p), range(start, end + 1)):
            if is_open:
                try:
                    svc = socket.getservbyport(port)
                except OSError:
                    svc = "unknown"
                print(f"  {port}/tcp open  {svc}")

if __name__ == "__main__":
    main()