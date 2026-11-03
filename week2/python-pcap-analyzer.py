#!/usr/bin/env python3
"""pcap_analyzer.py - summarize a pcap: top talkers, protocols, DNS queries, scan detection."""
import sys
from collections import Counter, defaultdict
from scapy.all import rdpcap, IP, TCP, UDP, DNS, DNSQR

SCAN_THRESHOLD = 20  # distinct ports hit by one source with bare SYNs

def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <file.pcap>")

    pkts = rdpcap(sys.argv[1])
    talkers, protos, dns_q = Counter(), Counter(), Counter()
    syn_ports = defaultdict(set)

    for p in pkts:
        if IP not in p:
            continue
        talkers[p[IP].src] += 1
        if TCP in p:
            protos["TCP"] += 1
            flags = int(p[TCP].flags)
            if flags & 0x12 == 0x02:  # SYN set, ACK not set
                syn_ports[p[IP].src].add(p[TCP].dport)
        elif UDP in p:
            protos["UDP"] += 1
        else:
            protos["Other"] += 1
        if p.haslayer(DNS) and p.haslayer(DNSQR) and p[DNS].qr == 0:
            dns_q[p[DNSQR].qname.decode(errors="ignore")] += 1

    print(f"Total packets: {len(pkts)}\n")
    print("Protocols:", dict(protos), "\n")
    print("Top talkers:")
    for ip, n in talkers.most_common(5):
        print(f"  {ip:<16} {n}")
    print("\nTop DNS queries:")
    for q, n in dns_q.most_common(10):
        print(f"  {q:<40} {n}")
    print("\nPossible port scanners:")
    found = False
    for ip, ports in syn_ports.items():
        if len(ports) >= SCAN_THRESHOLD:
            found = True
            print(f"  {ip} sent SYNs to {len(ports)} distinct ports")
    if not found:
        print("  none detected")

if __name__ == "__main__":
    main()