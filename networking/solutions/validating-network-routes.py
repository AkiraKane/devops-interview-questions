#!/usr/bin/env python3
"""
Validating Network Routes

Company: Google
Difficulty: Medium

Scenario:
Your server uses multiple network interfaces and may have incorrect routing for a
specific subnet. You need to verify and fix it to ensure proper traffic flow.

Task:
Display the current routing table to identify existing routes, check if a route for
the 10.10.0.0/16 subnet exists and which interface and gateway it uses. If the route
goes through eth0, delete the existing route and add a new route for 10.10.0.0/16
via gateway 192.168.100.1 using interface eth1.

Solution:
Use `ip route` commands to display, check, delete, and add routes for specific subnets.
"""

import subprocess
import re


def display_routing_table():
    """Display the current routing table."""
    print("[*] Displaying current routing table:")

    result = subprocess.run(
        ["ip", "route", "show"],
        capture_output=True,
        text=True
    )

    print(result.stdout if result.stdout else result.stderr)
    return result.stdout


def find_route_for_subnet(subnet="10.10.0.0/16"):
    """Find the existing route for a specific subnet."""
    print(f"[*] Checking if route for {subnet} exists...")

    result = subprocess.run(
        ["ip", "route", "show", subnet],
        capture_output=True,
        text=True
    )

    if result.returncode != 0 or not result.stdout.strip():
        print(f"[!] No route found for {subnet}")
        return None

    route_info = result.stdout.strip()
    print(f"  Found: {route_info}")

    # Parse route information
    # Examples:
    # 10.10.0.0/16 via 192.168.50.1 dev eth0
    # 10.10.0.0/16 dev eth0 proto static

    route_details = {
        'subnet': subnet,
        'gateway': None,
        'interface': None,
        'via': 'direct'
    }

    # Extract gateway
    gateway_match = re.search(r'via (\S+)', route_info)
    if gateway_match:
        route_details['gateway'] = gateway_match.group(1)
        route_details['via'] = 'via'

    # Extract interface
    dev_match = re.search(r'dev (\S+)', route_info)
    if dev_match:
        route_details['interface'] = dev_match.group(1)

    return route_details


def delete_route(subnet="10.10.0.0/16"):
    """Delete the existing route for a subnet."""
    print(f"[*] Deleting route for {subnet}...")

    result = subprocess.run(
        ["ip", "route", "del", subnet],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  [!] Error deleting route: {result.stderr}")
        return False
    else:
        print(f"[+] Route deleted successfully")
        return True


def add_route(subnet="10.10.0.0/16", gateway="192.168.100.1", interface="eth1"):
    """Add a new route for a subnet through a specific gateway and interface."""
    print(f"[*] Adding route for {subnet} via {gateway} dev {interface}...")

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


def verify_route(subnet="10.10.0.0/16", expected_gateway="192.168.100.1",
                 expected_interface="eth1"):
    """Verify the route is correctly configured."""
    print(f"[*] Verifying route for {subnet}...")

    result = subprocess.run(
        ["ip", "route", "show", subnet],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and result.stdout:
        route_info = result.stdout.strip()
        print(f"  Current: {route_info}")

        # Check if route uses correct interface
        if expected_interface in route_info:
            print(f"[+] Route correctly uses interface {expected_interface}")
        else:
            print(f"  [!] Route does NOT use expected interface {expected_interface}")

        # Check if route uses correct gateway
        if expected_gateway in route_info:
            print(f"[+] Route correctly uses gateway {expected_gateway}")
        else:
            print(f"  [!] Route does NOT use expected gateway {expected_gateway}")

        return True
    else:
        print(f"  [!] Route verification failed")
        return False


def main():
    """Main function to validate and fix network routes."""
    print("=" * 60)
    print("Validating Network Routes")
    print("Company: Google | Difficulty: Medium")
    print("=" * 60)
    print()

    subnet = "10.10.0.0/16"
    correct_gateway = "192.168.100.1"
    correct_interface = "eth1"

    # Step 1: Display routing table
    display_routing_table()
    print()

    # Step 2: Find existing route for subnet
    route_details = find_route_for_subnet(subnet)

    if route_details and route_details['interface'] == "eth0":
        print(f"  [!] Route goes through eth0 (incorrect)")
        print(f"      Gateway: {route_details.get('gateway', 'N/A')}")
        print()

        # Step 3: Delete incorrect route
        delete_route(subnet)
        print()

        # Step 4: Add correct route
        add_route(subnet, correct_gateway, correct_interface)
        print()

        # Step 5: Verify new route
        verify_route(subnet, correct_gateway, correct_interface)
    elif route_details and route_details['interface'] == correct_interface:
        print(f"  [+] Route already uses correct interface {correct_interface}")
    else:
        print(f"  [*] No route for {subnet} exists, adding correct route...")
        add_route(subnet, correct_gateway, correct_interface)

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  # Display routing table")
    print("  ip route show")
    print()
    print("  # Check route for specific subnet")
    print("  ip route show 10.10.0.0/16")
    print()
    print("  # Delete route")
    print("  ip route del 10.10.0.0/16")
    print()
    print("  # Add new route")
    print("  ip route add 10.10.0.0/16 via 192.168.100.1 dev eth1")


if __name__ == "__main__":
    main()