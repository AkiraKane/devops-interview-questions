#!/usr/bin/env python3
"""
Fix Port Exhaustion for High Speed Scraper

Company: X
Difficulty: Medium

Scenario:
A web-scraper systemd service is running on this system, making continuous HTTP requests.
The service has started experiencing connection failures - logs show HTTP status 000 errors,
indicating connections cannot be established even though the network is functional and
remote servers are accessible.

Task:
Check the service status and logs to understand the failures, investigate the underlying cause,
identify which system resource is exhausted, and apply the appropriate kernel configuration change.

Solution:
The issue is port exhaustion - the system runs out of ephemeral ports (typically 32768-61000).
The fix is to increase the ip_local_port_range and optionally reduce TIME_WAIT duration.
"""

import subprocess
import re


def get_service_status():
    """Check the web-scraper service status and logs."""
    print("[*] Checking web-scraper service status...")
    result = subprocess.run(
        ["systemctl", "status", "web-scraper"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.stdout


def check_ephemeral_port_range():
    """Check current ephemeral port range configuration."""
    print("[*] Checking current ephemeral port range...")
    result = subprocess.run(
        ["sysctl", "net.ipv4.ip_local_port_range"],
        capture_output=True,
        text=True
    )
    print(f"  Current: {result.stdout.strip()}")
    return result.stdout


def check_socket_usage():
    """Check current socket usage statistics."""
    print("[*] Checking socket usage...")
    result = subprocess.run(
        ["ss", "-s"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    return result.stdout


def apply_kernel_fix():
    """Apply kernel configuration to fix port exhaustion."""
    print("[*] Applying kernel configuration fix...")

    # Fix 1: Increase ephemeral port range
    print("[*] Increasing ephemeral port range (net.ipv4.ip_local_port_range)...")
    subprocess.run(
        ["sysctl", "-w", "net.ipv4.ip_local_port_range=1024 65535"],
        check=True
    )

    # Fix 2: Reduce TIME_WAIT duration to reuse ports faster
    print("[*] Reducing TCP TIME_WAIT duration (net.ipv4.tcp_fin_timeout)...")
    subprocess.run(
        ["sysctl", "-w", "net.ipv4.tcp_fin_timeout=15"],
        check=True
    )

    # Make ephemeral range change persistent across reboots
    print("[*] Making configuration persistent in /etc/sysctl.conf...")
    with open("/etc/sysctl.conf", "a") as f:
        f.write("\n# Fix for port exhaustion - increased ephemeral ports\n")
        f.write("net.ipv4.ip_local_port_range = 1024 65535\n")
        f.write("net.ipv4.tcp_fin_timeout = 15\n")

    print("[+] Kernel fix applied successfully")


def verify_fix():
    """Verify the fix by checking the new port range and testing connectivity."""
    print("\n[*] Verifying fix...")

    # Check new port range
    result = subprocess.run(
        ["sysctl", "net.ipv4.ip_local_port_range"],
        capture_output=True,
        text=True
    )
    print(f"  New port range: {result.stdout.strip()}")

    # Test connectivity
    print("[*] Testing HTTP connectivity...")
    test_result = subprocess.run(
        ["curl", "-o", "/dev/null", "-s", "-w", "HTTP Status: %{http_code}\n",
         "http://example.com"],
        capture_output=True,
        text=True
    )
    print(f"  {test_result.stdout}")
    if test_result.returncode != 0:
        print(f"  curl error: {test_result.stderr}")


def main():
    """Main function to demonstrate the port exhaustion fix."""
    print("=" * 60)
    print("Fix Port Exhaustion for High Speed Scraper")
    print("Company: X | Difficulty: Medium")
    print("=" * 60)
    print()

    # Step 1: Investigate the problem
    get_service_status()
    print()

    # Step 2: Check ephemeral port range (root cause)
    check_ephemeral_port_range()
    print()

    # Step 3: Check socket usage
    check_socket_usage()
    print()

    # Step 4: Apply the kernel fix
    apply_kernel_fix()
    print()

    # Step 5: Verify the fix
    verify_fix()

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  sysctl -w net.ipv4.ip_local_port_range=1024 65535")
    print("  sysctl -w net.ipv4.tcp_fin_timeout=15")
    print("  # Add to /etc/sysctl.conf for persistence:")
    print("  net.ipv4.ip_local_port_range = 1024 65535")


if __name__ == "__main__":
    main()