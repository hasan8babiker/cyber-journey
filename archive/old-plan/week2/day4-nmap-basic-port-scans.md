# TryHackMe: Nmap Basic Port Scans — Writeup

**Room:** Nmap Basic Port Scans (Network Security module)
**Date:** 2026-11-07 | **Roadmap:** Week 2, Day 4
**Tools:** Nmap, Wireshark (AttackBox)
**Skills practiced:** TCP/UDP fundamentals, port states, scan types, scan tuning

---

## Summary

This room covers how Nmap discovers open ports: the TCP connect scan, the SYN scan, the UDP scan, and options for controlling scan scope and speed. I ran each scan against the target machine and used Wireshark to confirm what actually happens on the wire.

---

## 1. TCP and UDP Basics

| Question | Answer | Notes |
|---|---|---|
| Service on UDP port 53 | **DNS** | DNS uses UDP 53 for normal queries and TCP 53 for large responses and zone transfers |
| Service on TCP port 22 | **SSH** | Encrypted remote login |
| Number of port states Nmap considers | **6** | See below |
| Most interesting state for a pentester | **open** | An open port means a service is listening and can be probed |

**Nmap's six port states**

| State | Meaning |
|---|---|
| open | A service is accepting connections |
| closed | The port is reachable, but no service is listening |
| filtered | Nmap can't tell if it's open; a firewall is dropping or blocking probes |
| unfiltered | Reachable, but Nmap can't tell if it's open or closed (seen with ACK scans) |
| open\|filtered | Nmap can't decide between open and filtered (common with UDP) |
| closed\|filtered | Nmap can't decide between closed and filtered (seen with idle scans) |

---

## 2. TCP Flags

| Question | Answer | Notes |
|---|---|---|
| Flag that resets a connection | **RST** | Sent to tear down a connection, or in reply to traffic aimed at a port with no listening service |
| Flag set on the first packet of the handshake | **SYN** | Starts the 3-way handshake and synchronizes sequence numbers |

The handshake is SYN, then SYN-ACK, then ACK.

---

## 3. TCP Connect Scan (`-sT`)

```bash
nmap -sT -sV -F <target>
```

| Option | What it does |
|---|---|
| `-sT` | Full TCP connect scan. Completes the whole 3-way handshake. Needs no root, but is noisier and gets logged by the target |
| `-sV` | Detects service names and versions |
| `-F` | Fast mode. Scans the top 100 ports instead of the default 1000 |

**Results**
- FTP on port 21: **open**
- Nmap's guess for the service on port 53: **domain** (DNS)

---

## 4. TCP SYN Scan (`-sS`)

```bash
sudo nmap -sS <target>
```

A SYN scan sends a SYN and waits for a reply. An open port answers with SYN-ACK, and Nmap then sends RST instead of ACK, so the handshake is never completed (this is why it's called "half-open"). That makes it faster than `-sT` and less likely to show up in application logs. It needs root because it crafts raw packets.

**Verification in Wireshark:** I captured the scan and counted **4 SYN-ACK** packets, matching the **4 open ports** Nmap reported. Every open port produces one SYN-ACK, so the capture and the scan output agree.

Useful Wireshark filter for this: `tcp.flags.syn == 1 && tcp.flags.ack == 1`

---

## 5. UDP Scan (`-sU`)

```bash
sudo nmap -sU --top-ports 20 <target>
```

UDP has no handshake, which makes scanning it harder:
- **Closed port:** the target replies with an ICMP "port unreachable" message.
- **Open port:** often sends no reply at all, so Nmap reports `open|filtered`.

Because Nmap has to wait and retransmit when there's no answer, UDP scans are much slower than TCP scans.

**Result:** UDP port 161 (SNMP) was **closed** on the target.

---

## 6. Scope and Performance Tuning

| Goal | Option | Notes |
|---|---|---|
| Scan TCP ports 5000-5500 | `-p5000-5500` | Limits the scan to a range |
| Run at least 64 probes in parallel | `--min-parallelism=64` | Speeds up large scans |
| Very slow, paranoid scan | `-T0` | Timing template 0. Used to evade IDS, but extremely slow |

Timing templates run from `-T0` (paranoid) to `-T5` (insane). The default is `-T3`.

---

## Key Takeaways

- `-sT` and `-sS` find the same open ports but behave differently on the network. `-sS` is stealthier, while `-sT` works without root.
- Wireshark confirmed the theory: the SYN-ACK count matched the open-port count.
- UDP scanning is slow and ambiguous because silence can mean open or filtered.
- Scan options trade speed against stealth and accuracy. Choosing them deliberately matters more than memorizing flags.

## Next Steps

Nmap does much more than a basic port scanner: service and version detection, OS detection and scripts. My own Python port checker only does TCP connect checks. To approach Nmap's features I plan to add banner grabbing, a SYN-style scan with Scapy, and UDP support.

---

*By @hasan8babiker | Happy Hunting*
