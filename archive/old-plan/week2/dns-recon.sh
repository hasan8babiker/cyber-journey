#!/usr/bin/env bash
# dnsrecon.sh - basic DNS enumeration
# Usage: ./dnsrecon.sh example.com

set -euo pipefail

[[ $# -ne 1 ]] && { echo "Usage: $0 <domain>"; exit 1; }
domain="$1"
out="recon_${domain}_$(date +%F).txt"

{
  echo "=== DNS recon for $domain ($(date)) ==="
  for type in A AAAA MX NS TXT SOA CNAME; do
    echo -e "\n--- $type ---"
    dig +short "$domain" "$type" || true
  done

  echo -e "\n--- Zone transfer attempts ---"
  for ns in $(dig +short NS "$domain"); do
    echo "[*] AXFR against $ns"
    dig AXFR "$domain" @"$ns" +time=3 +tries=1 | head -20 || true
  done

  echo -e "\n--- Whois (summary) ---"
  whois "$domain" | grep -Ei 'registrar:|creation|expir|name server' | head -10 || true
} | tee "$out"

echo -e "\n[+] Saved to $out"
