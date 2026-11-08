#!/usr/bin/env python3
"""banner-grabbing.py - connect to ports and print each service banner on it's own line.
Usage: ./banner-grabbing.py <host> <ports>   e.g ./banner-grabbing 10.10.10.5 21,22,80 or 1-1024
Only scan systems you own or are authorized to test.
"""

import socket, sys
from concurrent.futures import ThreadPoolExecutor

HTTP_PORTS = {80, 8000, 8080, 8888}


def parse_ports(spec):
	ports = set()
	for part in spec.split(","):
		if "-" in part:
			a, b = part.split("-")
			ports.update(range(int(a), int(b) + 1))
		else:
			ports.add(int(part))
	return sorted(ports)


def grab(host, port, timeout=2.0):
	"Return (port, None) if closed/filtered, (port, banner) if open."

	try:
		with socket.create_connection((host, port), timeout=timeout) as s:
			s.settimeout(timeout)
			if port in HTTP_PORTS:
				s.sendall(f"HEAD/ HTTP/1,.0\r\n\r\n".encode())
			try:
				data = s.recv(1024)
			except socket.timeout:
				return port, "(open, no banner)"
			text = data.decode(errors="replace").strip()
			return port, text.splitlines()[0] if text else "(open, no banner)"
	except OSError:
		return port, None


def main():
	if len(sys.argv) != 3:
		sys.exit(f"Usage: {sys.argv[0]} <host> <ports>")
	host = sys.argv[1]
	try:
		ip = socket.gethostbyname(host)
	except socket.gaierror:
		sys.exit("Could not resolve host")
	ports = parse_ports(sys.argv[2])
	print(f"Grabbing banner from {host} ({ip})\n")
	with ThreadPoolExecutor(max_workers=50) as ex:
		for port, banner in ex.map(lambda p: grab(ip, p), ports):
			if banner is not None:
				try:
					svc = socket.getservbyport(port)
				except OSError:
					svc = "unknown"
				print(f"{port}/tcp {svc:<10} {banner}")



if __name__ == "__main__":
	main()

