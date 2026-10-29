"""http_inspect.py - print status code, headers, and cookies for a URL.

Usage:
	python http_inspect.py http://example.com
	python http_inscpet.py example.com --no-redirects
	"""


import argparse
import sys
import requests

def main():
	parser = argparse.ArgumentParser(description="Inspect an HTTP response.")
	parser.add_argument("url", help="Target URL (https:// is added if misssing)")
	parser.add_argument("--no-redirects", action="store_true", help="Do not follow redirects")
	parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds (default: 10)")
	args = parser.parse_args()



	url = args.url
	if not url.startswith(("http://", "https://")):
		url = "https://" + url


	try:
		resp = requests.get(url, timeout=args.timeout, allow_redirects=not args.no_redirects)

	except requests.exceptions.RequestException as e:
		print(f"[!] Request Failed: {e}")
		sys.exit(1)


	print(f"[+] URL:	{resp.url}")
	print(f"[+] Status: {resp.status_code} {resp.reason}")


	if resp.history:
		print("\nRedirect chain:")
		for r in resp.history:
			print(f"{r.status_code} -> {r.headers.get('Location')}")



	print("\n Response headers:")
	for name, value in resp.headers.items():
		print(f"{name}: {value}")


	print("\n Cookies set:")
	if resp.cookies:
		for c in resp.cookies:
			print(f"{c.name}={c.value}")
			print(f"domain={c.domain} path={c.path}")
			print(f"secure={c.secure}")
			print(f"httponly={c.has_nonstandard_attr('HttpOnly')}")
	else:
		print("(none)")




if __name__ == "__main__":
	main()
