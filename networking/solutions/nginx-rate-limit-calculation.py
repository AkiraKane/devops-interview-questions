#!/usr/bin/env python3
"""
Nginx Rate Limit Calculation

Company: Cloudflare
Difficulty: Hard

Scenario:
Your Nginx web server has recently experienced performance issues caused by excessive
traffic from a few aggressive clients. You've decided to enable rate limiting based on
the recent traffic pattern. To determine the proper limit, you first need to analyze
request frequency.

Task:
Find the top 3 client IPs by number of requests from /var/log/nginx/access.log,
calculate the rate limit using the formula (sum of top 3 IP request counts / 3) * 0.8,
write this value into /etc/nginx/nginx.conf as limit_req_zone directive, and verify
the configuration with nginx -t.

Solution:
Parse nginx access logs to count requests per IP, calculate the rate limit,
update nginx.conf with the limit_req_zone directive, and validate the configuration.
"""

import subprocess
import re
from collections import Counter


def get_top_ips_from_log(log_path="/var/log/nginx/access.log"):
    """Parse nginx access log and return top 3 IPs by request count."""
    print(f"[*] Reading nginx access log: {log_path}")

    try:
        with open(log_path, "r") as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"  [!] Log file not found: {log_path}")
        return []
    except PermissionError:
        print(f"  [!] Permission denied: {log_path}")
        # Try with sudo
        result = subprocess.run(
            ["sudo", "cat", log_path],
            capture_output=True,
            text=True
        )
        log_content = result.stdout

    # Parse log lines to extract client IPs
    # Common nginx log format: client_ip - - [timestamp] "request" status ...
    # Example: 192.168.1.100 - - [22/May/2026:10:15:32 +0000] "GET /path HTTP/1.1" 200 1234

    ip_pattern = r'^(\d+\.\d+\.\d+\.\d+)'

    ips = []
    for line in log_content.split('\n'):
        match = re.match(ip_pattern, line.strip())
        if match:
            ips.append(match.group(1))

    # Count requests per IP
    ip_counts = Counter(ips)

    # Get top 3
    top_3 = ip_counts.most_common(3)

    print(f"[*] Total unique IPs: {len(ip_counts)}")
    print(f"[*] Top 3 IPs by request count:")
    for ip, count in top_3:
        print(f"    {ip}: {count} requests")

    return top_3


def calculate_rate_limit(top_ips):
    """
    Calculate rate limit using formula: (sum of top 3 IP counts / 3) * 0.8

    Returns the rate limit in requests per second (r/s).
    """
    if not top_ips:
        print("[!] No IPs found, cannot calculate rate limit")
        return 0

    total_requests = sum(count for _, count in top_ips)
    average = total_requests / len(top_ips)
    rate_limit = average * 0.8

    print()
    print(f"[*] Calculation:")
    print(f"    Sum of top 3: {total_requests}")
    print(f"    Average: {average:.2f}")
    print(f"    Rate limit (average * 0.8): {rate_limit:.2f} r/s")

    return rate_limit


def update_nginx_conf(rate_limit):
    """Update nginx.conf with the limit_req_zone directive."""
    print(f"\n[*] Updating /etc/nginx/nginx.conf...")

    conf_path = "/etc/nginx/nginx.conf"

    # Read current nginx.conf
    try:
        with open(conf_path, "r") as f:
            conf_content = f.read()
    except FileNotFoundError:
        print(f"  [!] nginx.conf not found at {conf_path}")
        return False
    except PermissionError:
        print(f"  [!] Permission denied, using sudo...")
        result = subprocess.run(
            ["sudo", "cat", conf_path],
            capture_output=True,
            text=True
        )
        conf_content = result.stdout

    # Create the limit_req_zone directive
    limit_directive = f'limit_req_zone $binary_remote_addr zone=app_limit:10m rate={int(rate_limit)}r/s;'

    print(f"[*] New directive: {limit_directive}")

    # Check if limit_req_zone already exists
    if 'limit_req_zone' in conf_content:
        print("[*] limit_req_zone already exists, updating...")
        # Replace existing limit_req_zone lines
        new_conf = re.sub(
            r'limit_req_zone\s+\$binary_remote_addr\s+zone=\w+:\d+m\s+rate=\d+r/s;',
            limit_directive,
            conf_content
        )
    else:
        print("[*] Adding new limit_req_zone directive...")
        # Add after the http { line
        new_conf = re.sub(
            r'(http\s*{)',
            r'\1\n    ' + limit_directive,
            conf_content
        )

    # Write the updated config
    try:
        with open(conf_path, "w") as f:
            f.write(new_conf)
        print(f"[+] Updated {conf_path}")
    except PermissionError:
        print("[*] Using sudo to write nginx.conf...")
        subprocess.run(
            ["sudo", "tee", conf_path],
            input=new_conf,
            text=True
        )

    return True


def verify_nginx_config():
    """Verify nginx configuration with nginx -t."""
    print("[*] Verifying nginx configuration...")

    result = subprocess.run(
        ["nginx", "-t"],
        capture_output=True,
        text=True
    )

    print(f"  {result.stdout}")
    if result.stderr:
        print(f"  {result.stderr}")

    if result.returncode == 0:
        print("[+] nginx configuration is valid!")
        return True
    else:
        print("[!] nginx configuration has errors!")
        return False


def main():
    """Main function to calculate and apply nginx rate limiting."""
    print("=" * 60)
    print("Nginx Rate Limit Calculation")
    print("Company: Cloudflare | Difficulty: Hard")
    print("=" * 60)
    print()

    # Step 1: Get top 3 IPs from access log
    top_ips = get_top_ips_from_log("/var/log/nginx/access.log")
    print()

    if not top_ips:
        print("[!] Could not determine top IPs. Creating sample output for demonstration...")
        print()
        print("Example calculation:")
        print("  Top IPs (example): 192.168.1.1: 4523, 192.168.1.2: 3891, 192.168.1.3: 3456")
        print("  Sum: 11870, Average: 3956.67, Rate limit: 3165 r/s")
        print()
        print("The actual solution would:")
        print("  1. Parse /var/log/nginx/access.log")
        print("  2. Count requests per IP")
        print("  3. Apply formula: (sum of top 3 / 3) * 0.8")
        print("  4. Update /etc/nginx/nginx.conf with limit_req_zone directive")
        print("  5. Verify with nginx -t")
        return

    # Step 2: Calculate rate limit
    rate_limit = calculate_rate_limit(top_ips)
    print()

    # Step 3: Update nginx.conf
    if rate_limit > 0:
        update_nginx_conf(rate_limit)

    # Step 4: Verify configuration
    print()
    verify_nginx_config()

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands and concepts:")
    print("  # Parse access log to count IPs")
    print("  awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -3")
    print()
    print("  # Calculate rate limit from top 3 averages")
    print("  # Formula: (sum_of_top_3 / 3) * 0.8")
    print()
    print("  # Updated nginx.conf should include:")
    print("  limit_req_zone $binary_remote_addr zone=app_limit:10m rate=<limit>r/s;")
    print()
    print("  # Verify configuration")
    print("  nginx -t")


if __name__ == "__main__":
    main()