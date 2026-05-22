#!/usr/bin/env python3
"""
Temporary Route Configuration

Company: Spotify
Difficulty: Easy

Scenario:
You need to reach a remote subnet that isn't covered by the default route, but you
don't want to make any permanent configuration changes.

Task:
Check the current routing table to confirm the 10.20.0.0/16 subnet is not present,
add a temporary static route for the 10.20.0.0/16 subnet via gateway 192.168.1.1
using interface veth0.

Solution:
Use `ip route` to check and manipulate the routing table. Routes added with `ip route add`
are temporary and will be lost after reboot.
"""

import subprocess
import re


def check_routing_table():
    """Check current routing table for the target subnet."""
    print("[*] Checking current routing table...")

    result = subprocess.run(
        ["ip", "route", "show"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    # Check if 10.20.0.0/16 route exists
    if "10.20.0.0/16" in result.stdout:
        print("[!] Route to 10.20.0.0/16 already exists")
        return True
    else:
        print("[*] Route to 10.20.0.0/16 NOT found (as expected)")
        return False


def add_temporary_route(subnet="10.20.0.0/16", gateway="192.168.1.1", interface="veth0"):
    """Add a temporary static route."""
    print(f"[*] Adding temporary route for {subnet} via {gateway} dev {interface}...")

    # Add route using ip route
    result = subprocess.run(
        ["ip", "route", "add", subnet, "via", gateway, "dev", interface],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  [!] Error adding route: {result.stderr}")
        return False
    else:
        print(f"[+] Route added successfully")
        return True


def verify_route(subnet="10.20.0.0/16"):
    """Verify the route was added."""
    print("[*] Verifying route...")

    result = subprocess.run(
        ["ip", "route", "get", subnet],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"  {result.stdout}")
        print("[+] Route is working!")
        return True
    else:
        print(f"  [!] Route verification failed: {result.stderr}")
        return False


def show_route_details(subnet="10.20.0.0/16"):
    """Show detailed route information."""
    print(f"[*] Displaying route details for {subnet}...")

    result = subprocess.run(
        ["ip", "route", "show", subnet],
        capture_output=True,
        text=True
    )

    print(result.stdout if result.stdout else result.stderr)


def main():
    """Main function to demonstrate temporary route configuration."""
    print("=" * 60)
    print("Temporary Route Configuration")
    print("Company: Spotify | Difficulty: Easy")
    print("=" * 60)
    print()

    subnet = "10.20.0.0/16"
    gateway = "192.168.1.1"
    interface = "veth0"

    # Step 1: Check current routing table
    print(f"[*] Target: Add route for {subnet} via {gateway} dev {interface}")
    print()

    route_exists = check_routing_table()
    print()

    # Step 2: Add temporary route if it doesn't exist
    if not route_exists:
        if add_temporary_route(subnet, gateway, interface):
            print()
            # Step 3: Verify the route
            verify_route(subnet)
    else:
        print("[*] Route already exists, skipping addition")

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  # Show all routes")
    print("  ip route show")
    print()
    print("  # Add temporary route")
    print("  ip route add 10.20.0.0/16 via 192.168.1.1 dev veth0")
    print()
    print("  # Verify route works")
    print("  ip route get 10.20.0.0/16")
    print()
    print("  # Remove route (if needed)")
    print("  ip route del 10.20.0.0/16")
    print()
    print("Note: Routes added with 'ip route add' are NOT persistent")
    print("      They will be lost after reboot.")


if __name__ == "__main__":
    main()