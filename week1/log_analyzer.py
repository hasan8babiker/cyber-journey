import re
import sys
from collections import Counter

PATTERN = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)")

def analyze(path):
    ips, users = Counter(), Counter()
    with open(path, errors="ignore") as f:
        for line in f:
            m = PATTERN.search(line)
            if m:
                users[m.group(1)] += 1
                ips[m.group(2)] += 1
    return ips, users

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python log_analyzer.py <auth.log>")
    ips, users = analyze(sys.argv[1])
    print("Top attacking IPs:")
    for ip, n in ips.most_common(5):
        print(f"  {ip:<16} {n} failures")
    print("Most targeted usernames:")
    for user, n in users.most_common(5):
        print(f"  {user:<16} {n} attempts")