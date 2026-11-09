import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port, timeout=1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                return port
    except socket.error:
        pass
    return None

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <host> <start_port> <end_port>")
        sys.exit(1)

    host = sys.argv[1]
    start, end = int(sys.argv[2]), int(sys.argv[3])

    print(f"Scanning {host} ports {start}-{end}...")
    with ThreadPoolExecutor(max_workers=100) as pool:
        results = pool.map(lambda p: scan_port(host, p), range(start, end + 1))

    open_ports = [p for p in results if p]
    for p in open_ports:
        try:
            service = socket.getservbyport(p)
        except OSError:
            service = "unknown"
        print(f"  {p}/tcp open  {service}")
    print(f"Done. {len(open_ports)} open port(s).")

if __name__ == "__main__":
    main()