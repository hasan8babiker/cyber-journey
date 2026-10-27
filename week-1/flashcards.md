# Week 1 Flashcards

Click a question to reveal the answer.

## Day 1: Ports and Networking

<details><summary>Port 22?</summary>SSH: encrypted remote login. (Telnet is 23, FTP is 21, SMTP is 25.)</details>

<details><summary>Port 53?</summary>DNS: UDP for normal queries, TCP for large responses and zone transfers.</details>

<details><summary>Ports 80 and 443?</summary>80 = HTTP (unencrypted), 443 = HTTPS (HTTP over TLS).</details>

<details><summary>Port 445?</summary>SMB: Windows file sharing. Frequent attack target (e.g. EternalBlue).</details>

<details><summary>Port 3389?</summary>RDP: Windows remote desktop. Exposed RDP is a common ransomware entry point.</details>

<details><summary>TCP 3-way handshake order?</summary>SYN, then SYN-ACK, then ACK.</details>

<details><summary>What does DNS do?</summary>Translates domain names into IP addresses. (DHCP assigns IPs; routers route.)</details>

<details><summary>OSI layers, 7 to 1?</summary>Application, Presentation, Session, Transport, Network, Data Link, Physical. Trick: All People Seem To Need Data Processing.</details>

<details><summary>Which OSI layer are TCP and UDP?</summary>Layer 4 (Transport). IP is Layer 3, Ethernet/MAC is Layer 2, HTTP/DNS are Layer 7.</details>

<details><summary>TCP vs UDP?</summary>TCP: reliable, connection-based, ordered (web, SSH). UDP: connectionless, faster, no delivery guarantee (DNS queries, streaming, VoIP).</details>

## Day 2: Linux Fundamentals

<details><summary>List all files incl. hidden, with details?</summary><code>ls -la</code>: -l long format, -a includes dotfiles.</details>

<details><summary>Read -rwxr-xr--</summary>First char = file type. Owner rwx, group r-x, others r--.</details>

<details><summary>What does chmod 640 set?</summary>Owner rw-, group r--, others ---. (read=4, write=2, execute=1)</details>

<details><summary>Search inside files recursively?</summary><code>grep -r "pattern" .</code> (find searches by name/type/size, not content.)</details>

<details><summary>Find flag.txt anywhere on the system?</summary><code>find / -name flag.txt 2>/dev/null</code>: the redirect hides Permission denied noise.</details>

<details><summary>What is in /etc/passwd?</summary>User account info (users, UIDs, home dirs, shells). World-readable. Hashes are in /etc/shadow (root only).</details>

<details><summary>Where are logs stored?</summary><code>/var/log</code> (e.g. auth.log for logins, syslog).</details>

<details><summary>List processes / stop one?</summary><code>ps aux</code> (or <code>top</code> live) / <code>kill PID</code>. <code>kill -9 PID</code> force-kills.</details>

<details><summary>What does sudo do?</summary>Runs one command as root if allowed in /etc/sudoers. <code>sudo -l</code> shows what you may run (privilege-escalation check).</details>

<details><summary>What does the pipe | do?</summary>Sends one command's output into the next: <code>cat log.txt | grep Failed</code>. Also: <code>&gt;</code> overwrite, <code>&gt;&gt;</code> append.</details>

<details><summary>Remote login / copy a file remotely?</summary><code>ssh user@host</code> / <code>scp file user@host:/path</code> (encrypted, port 22).</details>

<details><summary>cat, head, tail?</summary>Whole file, first 10 lines, last 10 lines. <code>tail -f</code> follows a log live.</details>
