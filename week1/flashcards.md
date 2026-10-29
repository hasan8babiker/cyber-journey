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

## Day 3: Windows Fundamentals

<details><summary>See which groups a user belongs to?</summary><code>net user USERNAME</code> and read Local Group Memberships. GUI: <code>lusrmgr.msc</code>, Users, double-click the user, Member Of tab.</details>

<details><summary>List members of a group?</summary><code>net localgroup Administrators</code> (swap in any group name).</details>

<details><summary>Open the Local Users and Groups tool?</summary>Win+R, then <code>lusrmgr.msc</code>. (Not on Windows Home; use <code>net user</code> instead.)</details>

<details><summary>Add a user to a group / create a user?</summary><code>net localgroup GROUP USER /add</code> / <code>net user USER PASSWORD /add</code>.</details>

<details><summary>What does "Change account type" do?</summary>Only toggles Standard user vs Administrator. It does not show other group memberships.</details>

<details><summary>Standard user vs Administrator?</summary>Administrators can change system-wide settings, install software, and manage other accounts. Standard users are limited and need admin approval for system changes.</details>

<details><summary>What is UAC?</summary>User Account Control: prompts for approval before an action runs with admin rights, limiting what malware can do silently.</details>

<details><summary>What is the SAM database?</summary>Security Account Manager: stores local account password hashes (C:\Windows\System32\config\SAM). Attackers dump it to crack passwords.</details>

<details><summary>What is a SID?</summary>Security Identifier: the unique ID Windows uses for a user or group. Admin account RID ends in -500.</details>

<details><summary>What is the Windows Registry?</summary>Hierarchical database of system and app settings. Edit with <code>regedit</code>. Main hives: HKLM (machine) and HKCU (current user).</details>

<details><summary>What is NTFS?</summary>The default Windows file system. Supports file permissions (ACLs), encryption (EFS), and journaling.</details>

<details><summary>Where are the Windows system files?</summary><code>C:\Windows\System32</code>. User data is in <code>C:\Users</code>.</details>

<details><summary>Which tool shows logs on Windows?</summary>Event Viewer (<code>eventvwr</code>): Security log for logons, System log for services and drivers, Application log for apps.</details>

<details><summary>Event ID 4624 and 4625?</summary>4624 = successful logon, 4625 = failed logon. Many 4625s in a row suggest brute force.</details>

<details><summary>List processes / stop one from the command line?</summary><code>tasklist</code> / <code>taskkill /PID 1234 /F</code>.</details>

<details><summary>What are Windows services?</summary>Background programs that start without a user logged in. Manage with <code>services.msc</code> or <code>sc query</code>.</details>

<details><summary>Show current user and their privileges?</summary><code>whoami</code>, <code>whoami /groups</code>, <code>whoami /priv</code>.</details>

<details><summary>Show network config on Windows?</summary><code>ipconfig /all</code> (like ip a). <code>netstat -ano</code> lists connections and the owning PID.</details>

<details><summary>CMD vs PowerShell?</summary>CMD is the legacy shell. PowerShell is object-based, scriptable, and the main admin and attacker tool on modern Windows.</details>

<details><summary>Built-in antivirus and firewall?</summary>Windows Defender (Security) and Windows Defender Firewall. Check status in Windows Security.</details>

## Day 4: Web Fundamentals

<details><summary>What happens when you type a URL in a browser?</summary>DNS lookup (domain to IP), TCP handshake, TLS handshake (if HTTPS), browser sends the HTTP request, server sends the response, browser renders it.</details>

<details><summary>Main HTTP methods?</summary>GET = retrieve, POST = send/create data, PUT = replace/update, DELETE = remove, HEAD = headers only, OPTIONS = list allowed methods.</details>

<details><summary>GET vs POST?</summary>GET puts data in the URL (visible, logged, cached). POST puts data in the request body (not shown in the URL).</details>

<details><summary>Status code ranges?</summary>1xx info, 2xx success, 3xx redirect, 4xx client error, 5xx server error.</details>

<details><summary>200, 301, 302, 404, 500?</summary>200 OK, 301 permanent redirect, 302 temporary redirect, 404 not found, 500 server error.</details>

<details><summary>401 vs 403?</summary>401 = you haven't proven who you are. 403 = the server knows who you are and still refuses.</details>

<details><summary>Structure of an HTTP request?</summary>Request line (method, path, version), headers, blank line, optional body.</details>

<details><summary>Structure of an HTTP response?</summary>Status line (version, code, reason), headers, blank line, body.</details>

<details><summary>Host header?</summary>Tells the server which domain you want, so one IP can host many sites.</details>

<details><summary>User-Agent header?</summary>Identifies the client (browser or tool). Easily spoofed.</details>

<details><summary>Content-Type header?</summary>Describes the body format (e.g. text/html, application/json, application/x-www-form-urlencoded).</details>

<details><summary>What is a cookie?</summary>Small data the server sets with the Set-Cookie header; the browser sends it back with the Cookie header on later requests. Used for sessions and tracking.</details>

<details><summary>Cookie flags: HttpOnly, Secure, SameSite?</summary>HttpOnly = JavaScript can't read it (helps against XSS theft). Secure = sent only over HTTPS. SameSite = limits cross-site sending (helps against CSRF).</details>

<details><summary>What is a session?</summary>Server-side state tied to a user, usually identified by a session ID stored in a cookie.</details>

<details><summary>Key security headers?</summary>Content-Security-Policy, Strict-Transport-Security (HSTS), X-Frame-Options, X-Content-Type-Options.</details>

<details><summary>HTTP vs HTTPS?</summary>HTTPS is HTTP over TLS: encrypted, integrity-protected, and authenticates the server.</details>

<details><summary>What is Burp Proxy used for?</summary>It sits between browser and server so you can intercept, inspect, modify, and forward requests and responses.</details>

<details><summary>Burp Repeater vs Intruder?</summary>Repeater = manually resend and tweak one request. Intruder = automate many requests with changing payloads (fuzzing, brute force).</details>

<details><summary>What does http_inspect.py show?</summary>Status code, redirect chain, response headers, and cookies (with domain, path, Secure, HttpOnly).</details>

## Day 5: Bandit and CTF Basics

<details><summary>Connect to a Bandit level?</summary><code>ssh bandit0@bandit.labs.overthewire.org -p 2220</code>. Bandit uses port 2220, not 22.</details>

<details><summary>Read a file named "-" or with spaces?</summary><code>cat ./-</code> for a dash file. <code>cat "my file"</code> or <code>cat my\ file</code> for spaces.</details>

<details><summary>Find a file by size, owner, and group?</summary><code>find / -user bandit7 -group bandit6 -size 33c 2>/dev/null</code> (c = bytes).</details>

<details><summary>Find the one unique line in a file?</summary><code>sort file | uniq -u</code>. uniq only compares adjacent lines, so sort first.</details>

<details><summary>Extract readable text from a binary file?</summary><code>strings file</code>. Combine with grep: <code>strings file | grep "="</code>.</details>

<details><summary>Decode base64?</summary><code>echo "TEXT" | base64 -d</code> (or <code>base64 -d file</code>).</details>

<details><summary>Decode ROT13?</summary><code>echo "TEXT" | tr 'A-Za-z' 'N-ZA-Mn-za-m'</code>.</details>

<details><summary>Convert a hex dump back to a file?</summary><code>xxd -r hexdump.txt output</code>. Check the type with <code>file output</code>.</details>

<details><summary>What does the file command do?</summary>Identifies a file's real type from its contents (gzip, bzip2, tar, ASCII text), ignoring the extension.</details>

<details><summary>Extract gzip, bzip2, and tar files?</summary><code>gzip -d</code> (or <code>gunzip</code>), <code>bzip2 -d</code>, <code>tar xf file.tar</code>. Rename with the right extension first when needed.</details>

<details><summary>Work in a writable directory on Bandit?</summary><code>mktemp -d</code> creates a private folder in /tmp. Work there, since your home may be read-only.</details>

<details><summary>Log in to the next level with a private key?</summary><code>chmod 600 key.private</code> then <code>ssh -i key.private user@host -p 2220</code>. ssh rejects keys with loose permissions.</details>

<details><summary>Send data to a port / test a service?</summary><code>nc localhost PORT</code> or <code>echo "pass" | nc localhost PORT</code>. Add <code>ncat --ssl</code> or <code>openssl s_client -connect host:port</code> for TLS.</details>

<details><summary>Scan a range of ports?</summary><code>nmap -p 31000-32000 localhost</code>. Add <code>-sV</code> to detect service versions.</details>

<details><summary>Typical CTF flag format?</summary>picoCTF uses <code>picoCTF{...}</code>. Always copy the full string with braces.</details>

<details><summary>What does 2>/dev/null do?</summary>Sends error messages (stderr) to nowhere, hiding Permission denied noise from find.</details>

<details><summary>What does decoder.py do?</summary>Decodes base64, hex, and ROT13 from text or a file, so you can quickly identify and decode CTF encodings.</details>
