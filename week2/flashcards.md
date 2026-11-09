## Week 2 Day 1: Networking

**Q:** OSI layers 1-7?
**A:** Physical, Data Link, Network, Transport, Session, Presentation, Application ("Please Do Not Throw Sausage Pizza Away")

**Q:** TCP/IP model layers?
**A:** Link, Internet, Transport, Application

**Q:** TCP 3-way handshake?
**A:** SYN → SYN-ACK → ACK

**Q:** TCP vs UDP?
**A:** TCP: connection-oriented, reliable, ordered (web, SSH, email). UDP: connectionless, fast, no delivery guarantee (DNS, streaming, VoIP).

**Q:** Which layer does a switch work at? A router?
**A:** Switch: Layer 2 (MAC addresses). Router: Layer 3 (IP addresses).

**Q:** What does ARP do?
**A:** Maps an IP address to a MAC address on a local network.

**Q:** Why is ARP spoofing possible?
**A:** ARP has no authentication. Any host can send fake replies and poison other hosts' caches (a man-in-the-middle setup).

**Q:** Data unit names by layer?
**A:** L4 segment (TCP) / datagram (UDP), L3 packet, L2 frame, L1 bits

**Q:** Common ports?
**A:** 21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 445 SMB, 3389 RDP

**Q:** Usable hosts in a /24? /26? /30?
**A:** 254 / 62 / 2 (formula: 2^(32 - prefix) - 2)

**Q:** What is a /26 subnet mask?
**A:** 255.255.255.192

**Q:** Private IPv4 ranges (RFC 1918)?
**A:** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

**Q:** What does NAT do?
**A:** Translates private IPs to a public IP so many devices can share one address.

**Q:** TCP flags to know?
**A:** SYN, ACK, FIN, RST, PSH, URG

**Q:** What does an open, closed and filtered port look like to a scanner?
**A:** Open: SYN-ACK. Closed: RST. Filtered: no response (a firewall is dropping packets).

**Q:** How does your port checker know a port is open?
**A:** connect_ex() returns 0, meaning the full TCP handshake completed.

## Week 2 Day 2: DNS, DHCP, Subnetting

**Q:** DNS resolution order?
**A:** Browser cache → OS cache → recursive resolver → root server → TLD server → authoritative server

**Q:** A vs AAAA vs CNAME vs MX vs TXT vs NS vs PTR?
**A:** A: name → IPv4. AAAA: name → IPv6. CNAME: alias to another name. MX: mail server. TXT: arbitrary text (SPF, DKIM, verification). NS: authoritative nameserver. PTR: IP → name (reverse lookup).

**Q:** What is a DNS zone transfer (AXFR) and why is it dangerous?
**A:** It copies the full zone's records from a nameserver. If it's open to anyone, attackers get a complete map of hosts and subdomains.

**Q:** DHCP DORA?
**A:** Discover → Offer → Request → Acknowledge

**Q:** dig command for MX records?
**A:** dig MX example.com (add +short for a compact answer)

**Q:** Reverse DNS lookup command?
**A:** dig -x 8.8.8.8

**Q:** Default DNS port and protocols?
**A:** 53, UDP for normal queries, TCP for large responses and zone transfers

**Q:** Subnet math: 192.168.1.0/26, what are the network, broadcast and usable range?
**A:** Network .0, broadcast .63, usable .1 to .62

**Q:** Block size for /27? /28?
**A:** 32 / 16 (256 minus the last octet of the mask)

**Q:** What's passive vs active recon?
**A:** Passive: no direct contact with the target (whois, DNS lookups, search engines). Active: sends traffic to the target (port scans, banner grabs).

**Q:** What does set -euo pipefail do in Bash?
**A:** Exit on errors (-e), treat unset variables as errors (-u), fail a pipeline if any command in it fails (pipefail)

## Week 2 Day 3: Wireshark + Packet Analysis

**Q:** Capture filter vs display filter?
**A:** Capture filters (BPF syntax) limit what gets recorded. Display filters (Wireshark syntax) hide packets after capture.

**Q:** Display filter for traffic to or from an IP?
**A:** ip.addr == 10.0.0.5 (use ip.src or ip.dst for one direction)

**Q:** Display filters for DNS, HTTP, a TCP port?
**A:** dns, http, tcp.port == 443

**Q:** Display filter for SYN-only packets (scan indicator)?
**A:** tcp.flags.syn == 1 && tcp.flags.ack == 0

**Q:** Capture filter for port 80 only?
**A:** port 80

**Q:** How do you rebuild a full conversation?
**A:** Right-click a packet → Follow → TCP Stream (or Ctrl+Alt+Shift+T)

**Q:** How do you find cleartext credentials in a capture?
**A:** Filter http.request.method == "POST" or ftp, then Follow Stream. Telnet, FTP and HTTP send credentials unencrypted.

**Q:** What does a port scan look like in a capture?
**A:** One source sending SYNs to many ports. Closed ports reply RST, open ones reply SYN-ACK.

**Q:** Wireshark Statistics menu items to know?
**A:** Conversations, Endpoints, Protocol Hierarchy, I/O Graph

**Q:** tcpdump command to save traffic on eth0 to a file?
**A:** sudo tcpdump -i eth0 -w capture.pcap

**Q:** tcpdump command to read a saved capture?
**A:** tcpdump -r capture.pcap

**Q:** Sign of ARP spoofing in a capture?
**A:** Multiple IPs claiming the same MAC, or repeated unsolicited ARP replies

**Q:** Why can't you read HTTPS payloads in Wireshark?
**A:** TLS encrypts them. You'd need the session keys (SSLKEYLOGFILE) to decrypt.

## Week 2 Day 4: Nmap

**Q:** Host discovery only, no port scan?
**A:** nmap -sn <target> (ping scan)

**Q:** -sS vs -sT?
**A:** -sS: SYN (half-open/stealth) scan, needs root, never completes the handshake. -sT: full TCP connect scan, works without root, noisier.

**Q:** UDP scan flag and why it's slow?
**A:** -sU. Open UDP ports often don't respond, so nmap has to wait and retransmit.

**Q:** Service/version detection? OS detection? Aggressive?
**A:** -sV / -O / -A (-A = -sV + -O + default scripts + traceroute)

**Q:** Scan all 65535 ports?
**A:** -p- (or -p 1-65535)

**Q:** Scan specific ports?
**A:** -p 22,80,443 or -p 1-1000

**Q:** Nmap's six port states?
**A:** open, closed, filtered, unfiltered, open|filtered, closed|filtered

**Q:** What does "filtered" mean?
**A:** Nmap can't tell if the port is open because a firewall or filter is dropping the probes.

**Q:** Skip host discovery (treat all hosts as up)?
**A:** -Pn (useful when the target blocks ping)

**Q:** Timing templates?
**A:** -T0 paranoid, -T1 sneaky, -T2 polite, -T3 normal (default), -T4 aggressive, -T5 insane

**Q:** Output formats and the flag that saves all of them?
**A:** -oN normal, -oX XML, -oG grepable, -oA all three

**Q:** Run default scripts? A specific script category?
**A:** -sC / --script vuln (or --script <name>)

**Q:** Read targets from a file?
**A:** -iL targets.txt

**Q:** Increase verbosity during a scan?
**A:** -v or -vv (press Enter mid-scan for status)

**Q:** Why scan with -sV after finding open ports?
**A:** Port numbers can lie. Services run on non-standard ports, and version info points to known vulnerabilities.

## Week 2 Day 5: Protocols and Banner Grabbing

**Q:** Default ports: FTP, SSH, Telnet, SMTP, HTTP?
**A:** 21, 22, 23, 25, 80

**Q:** Default ports: POP3, IMAP, and their encrypted versions?
**A:** POP3 110 (995 with TLS), IMAP 143 (993 with TLS)

**Q:** Encrypted replacements for HTTP, FTP, Telnet, SMTP?
**A:** HTTPS (443), SFTP or FTPS, SSH, SMTPS/STARTTLS (465/587)

**Q:** Why are Telnet, FTP and HTTP insecure?
**A:** They send data and credentials in cleartext, so anyone sniffing the network (Wireshark) can read them.

**Q:** What is a service banner?
**A:** The text a service sends on connect, often with software name and version (e.g. SSH-2.0-OpenSSH_8.2p1).

**Q:** Why do attackers grab banners?
**A:** The version points to known vulnerabilities (CVEs). Defenders can hide or change banners, but that isn't real security.

**Q:** Netcat command to connect to a port?
**A:** nc -nv <ip> <port> (-n skip DNS, -v verbose)

**Q:** Netcat command to listen on a port?
**A:** nc -lvnp 4444

**Q:** HTTP methods and what HEAD does?
**A:** GET, POST, PUT, DELETE, HEAD, OPTIONS. HEAD returns only the headers, no body.

**Q:** Common HTTP status code groups?
**A:** 2xx success, 3xx redirect, 4xx client error (403 forbidden, 404 not found), 5xx server error

**Q:** Manual SMTP commands in order?
**A:** HELO/EHLO, MAIL FROM, RCPT TO, DATA, QUIT

**Q:** FTP anonymous login?
**A:** Username "anonymous" with any password. A common misconfiguration worth checking in every scan.

**Q:** Why does python socket.create_connection raise on closed ports?
**A:** The TCP connect fails (connection refused or timeout), so the code treats that as closed or filtered.

**Q:** Difference between active banner grabbing and passive?
**A:** Active: connect and read the banner (nc, nmap -sV). Passive: observe traffic without contacting the target (packet captures).

## Week 2, Day 6

**Q:** `nmap -sS` vs `-sT`: what's the difference?
**A:** `-sS` (SYN) sends SYN, gets SYN/ACK, then sends RST without finishing the handshake. Needs root. `-sT` (connect) completes the full handshake. No root needed, but it is logged more.

**Q:** What are the three main Nmap port states?
**A:** Open (service accepting connections), closed (reachable, nothing listening, replies RST), filtered (no reply or ICMP error, a firewall is probably dropping packets).

**Q:** Why are UDP scans (`-sU`) slow?
**A:** Open UDP ports often send no reply, and closed ports send ICMP unreachable that is rate-limited. Nmap has to wait and retry.

**Q:** What do `-sV`, `-O` and `-A` do?
**A:** `-sV` detects service versions, `-O` detects the OS, `-A` = `-sV` + `-O` + default scripts + traceroute.

**Q:** How do you scan all 65535 ports quickly?
**A:** `nmap -p- -T4 <host>`

**Q:** Nmap output formats?
**A:** `-oN` normal, `-oG` greppable, `-oX` XML, `-oA name` all three.

**Q:** In Python, how does `sock.connect_ex((host, port))` signal an open port?
**A:** It returns 0 on success instead of raising an exception. Any non-zero value is an error code (closed, timed out, unreachable).

**Q:** Why use threads (`ThreadPoolExecutor`) in a port scanner?
**A:** Scanning is I/O-bound: most time is spent waiting on timeouts. Threads let many connections wait in parallel, so the scan takes seconds instead of minutes.

**Q:** What is banner grabbing?
**A:** Connecting to a service and reading what it sends (e.g. `SSH-2.0-OpenSSH_8.2p1`) to identify the product and version. Some services speak first (SSH, FTP, SMTP); HTTP needs a request such as `HEAD /`.

**Q:** Why can a banner-based version be wrong?
**A:** Admins can hide or spoof banners, and distros backport security fixes without changing the version string. Always verify before calling something vulnerable.

**Q:** What are CVE, CVSS and NVD?
**A:** CVE = unique ID for a public vulnerability. CVSS = 0-10 severity score (9.0+ is critical). NVD = NIST's database that enriches CVEs with scores and affected products.

**Q:** What is a CPE?
**A:** A standard name for a product and version, e.g. `cpe:2.3:a:apache:http_server:2.4.49`. Querying by CPE is more accurate than keyword search.

**Q:** What does KEV mean?
**A:** CISA's Known Exploited Vulnerabilities catalog: CVEs confirmed exploited in the wild. Patch these first.

**Q:** Which command finds SUID files, and why does it matter?
**A:** `find / -perm -4000 2>/dev/null`. SUID binaries run as their owner (often root), so they are a privilege-escalation lead.

**Q:** What does `ss -tulpn` show?
**A:** Listening TCP/UDP sockets with numeric ports and the owning process (`-p` needs root for other users' processes).

**Q:** What does `chmod 754 file` mean?
**A:** Owner rwx (7), group r-x (5), others r-- (4). Values: r=4, w=2, x=1.

**Q:** What does `2>/dev/null` do?
**A:** Redirects stderr (file descriptor 2) to the null device, discarding error messages such as "Permission denied" from `find`.

**Q:** Which command lists what you can run as root?
**A:** `sudo -l`