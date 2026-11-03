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