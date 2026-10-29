import socket


def check_port(host, port, timeout=1.0):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.settimeout(timeout)
		return s.connect_ex((host, port)) == 0

if __name__ == "__main__":
  host = input("Enter url example scanme.nmap.org: ")
  if host != '':
  	for port in (22, 80, 443):
  		print(f"{host}:{port} ->", "open" if check_port(host, port) else "closed/filterd")

  else:
  	print("Please Enter a Valid url")
