#!/usr/bin/env bash
# scanwrap.sh - host discovery, then service scan of live hosts
# Usage: ./scanwrap.sh <target|CIDR>
# Only scan systems you own or are authorized to test (THM, scanme.nmap.org, your lab).

set -euo pipefail

command -v nmap >/dev/null || { echo "nmap not installed"; exit 1; }
[[ $# -ne 1 ]] && { echo "Usage: $0 <target|CIDR>"; exit 1; }

target="$1"
dir="scan_$(date +%F_%H%M)"
mkdir -p "$dir"

echo "[*] Host discovery on $target"
nmap -sn "$target" -oG - | awk '/Up$/{print $2}' > "$dir/live_hosts.txt"

n=$(wc -l < "$dir/live_hosts.txt")
echo "[+] $n live host(s)"
[[ $n -eq 0 ]] && exit 0

echo "[*] Service scan (top 1000 ports)"
nmap -sV -T4 --top-ports 1000 -iL "$dir/live_hosts.txt" -oA "$dir/services" >/dev/null

# One open port per line: HOST  PORT/PROTO  SERVICE  VERSION
awk '
  /^Nmap scan report for/ { host=$NF; gsub(/[()]/, "", host) }
  /^[0-9]+\/(tcp|udp)[ ]+open/ {
    ver=""
    for (i=4; i<=NF; i++) ver = ver " " $i
    printf "%-16s %-10s %-12s%s\n", host, $1, $3, ver
  }
' "$dir/services.nmap" | tee "$dir/open_ports.txt"

echo
echo "[+] Full results in $dir/ (open_ports.txt, services.nmap/.xml/.gnmap)"