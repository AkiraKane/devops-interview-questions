#!/usr/bin/env python3
"""
Validating DNS Consistency

Company: SAP
Difficulty: Easy

Scenario:
Your monitoring alerts indicate that DNS resolution might be inconsistent across
servers, and you need to confirm both IPv4 and IPv6 records for a given domain.

Task:
Add IPv4 and IPv6 address entries for the domain example.local to /etc/hosts using
the format <ip_address> <hostname> with each record on a separate line.

Solution:
Edit /etc/hosts to add static DNS entries for the domain. The /etc/hosts file
takes precedence over DNS for name resolution.
"""

import subprocess
import os


def preview_etc_hosts():
    """Preview current /etc/hosts content."""
    print("[*] Current /etc/hosts entries:")

    try:
        with open("/etc/hosts", "r") as f:
            content = f.read()
            print("-" * 40)
            print(content)
            print("-" * 40)
    except PermissionError:
        print("[*] Permission denied, using sudo...")
        result = subprocess.run(
            ["sudo", "cat", "/etc/hosts"],
            capture_output=True,
            text=True
        )
        print(result.stdout)


def add_dns_entries(ipv4="198.51.100.42", ipv6="2001:db8:85a3::8a2e:370:7334",
                     hostname="example.local"):
    """Add DNS entries to /etc/hosts."""
    print(f"[*] Adding DNS entries for '{hostname}' to /etc/hosts...")
    print(f"    IPv4: {ipv4} {hostname}")
    print(f"    IPv6: {ipv6} {hostname}")

    entries = f"{ipv4} {hostname}\n{ipv6} {hostname}\n"

    # Read current content
    try:
        with open("/etc/hosts", "r") as f:
            current_content = f.read()
    except PermissionError:
        print("[*] Permission denied, using sudo to read...")
        result = subprocess.run(
            ["sudo", "cat", "/etc/hosts"],
            capture_output=True,
            text=True
        )
        current_content = result.stdout
    except FileNotFoundError:
        current_content = ""

    # Check if entries already exist
    if hostname in current_content:
        print(f"[!] Entries for '{hostname}' already exist in /etc/hosts")
        print("[*] Updating existing entries...")

        # Remove old entries for this hostname
        lines = current_content.split('\n')
        new_lines = []
        skip_next = False

        for line in lines:
            if hostname in line and not line.strip().startswith('#'):
                continue  # Skip lines with this hostname (non-comment)
            new_lines.append(line)

        new_content = '\n'.join(new_lines)
    else:
        new_content = current_content.rstrip('\n')

    # Append new entries
    new_content += '\n' + entries

    # Write updated content
    try:
        with open("/etc/hosts", "w") as f:
            f.write(new_content)
        print("[+] DNS entries added successfully")
    except PermissionError:
        print("[*] Permission denied, using sudo...")
        subprocess.run(
            ["sudo", "tee", "/etc/hosts"],
            input=new_content,
            text=True
        )
        print("[+] DNS entries added successfully")


def verify_dns_entries(hostname="example.local"):
    """Verify DNS entries are correctly configured."""
    print(f"[*] Verifying DNS resolution for '{hostname}'...")

    # Check with getent
    print("[*] Using getent to check hosts database:")
    result = subprocess.run(
        ["getent", "hosts", hostname],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  {result.stdout}")
    else:
        print(f"  getent returned: {result.returncode}")

    # Try to ping (just check if hostname resolves, don't expect replies)
    print("[*] Checking /etc/hosts content:")
    try:
        with open("/etc/hosts", "r") as f:
            for line in f:
                if hostname in line:
                    print(f"  {line.strip()}")
    except PermissionError:
        result = subprocess.run(
            ["grep", hostname, "/etc/hosts"],
            capture_output=True,
            text=True
        )
        print(f"  {result.stdout}")


def main():
    """Main function to add DNS entries."""
    print("=" * 60)
    print("Validating DNS Consistency")
    print("Company: SAP | Difficulty: Easy")
    print("=" * 60)
    print()

    hostname = "example.local"
    ipv4 = "198.51.100.42"
    ipv6 = "2001:db8:85a3::8a2e:370:7334"

    # Step 1: Preview current /etc/hosts
    preview_etc_hosts()
    print()

    # Step 2: Add DNS entries
    add_dns_entries(ipv4, ipv6, hostname)
    print()

    # Step 3: Verify entries
    verify_dns_entries(hostname)

    print()
    print("[+] Solution complete!")
    print()
    print("Key information:")
    print("  /etc/hosts format: <ip_address> <hostname>")
    print()
    print("  Added entries:")
    print(f"    {ipv4} {hostname}")
    print(f"    {ipv6} {hostname}")
    print()
    print("Note: /etc/hosts entries take precedence over DNS")
    print("      Changes take effect immediately (no service restart needed)")


if __name__ == "__main__":
    main()