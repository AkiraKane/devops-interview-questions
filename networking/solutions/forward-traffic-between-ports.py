#!/usr/bin/env python3
"""
Forward Traffic Between Ports

Company: Meta
Difficulty: Medium

Scenario:
A service on your server is running on port 8080, but you now need it to also be
reachable on port 8081. The application cannot be restarted and its configuration
cannot be changed.

Task:
Verify the service is listening on 127.0.0.1:8080. Configure iptables to forward
all TCP traffic from port 8081 to port 8080, ensuring this works for both external
requests and local connections (localhost). Verify the forwarding works, then save
the rules to persist after a reboot.

Solution:
Use iptables PREROUTING (for external traffic) and OUTPUT (for local traffic) chains
with REDIRECT target to forward packets from port 8081 to 8080.
"""

import subprocess
import socket
import time


def verify_service_listening():
    """Verify the service is listening on 127.0.0.1:8080."""
    print("[*] Checking if service is listening on 127.0.0.1:8080...")
    result = subprocess.run(
        ["ss", "-tlnp"],
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Also use netstat as fallback
    if "8080" not in result.stdout:
        print("[*] Trying with netstat as fallback...")
        result = subprocess.run(
            ["netstat", "-tlnp"],
            capture_output=True,
            text=True
        )
        print(result.stdout)


def setup_iptables_forwarding():
    """Configure iptables to forward traffic from port 8081 to 8080."""
    print("[*] Setting up iptables port forwarding...")

    # Enable IP forwarding (required for NAT/redirection)
    print("[*] Enabling IP forwarding...")
    subprocess.run(
        ["sysctl", "-w", "net.ipv4.ip_forward=1"],
        check=True
    )

    # For external traffic - PREROUTING chain in NAT table
    print("[*] Adding PREROUTING rule for external traffic (port 8081 -> 8080)...")
    subprocess.run(
        ["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "--dport", "8081",
         "-j", "REDIRECT", "--to-port", "8080"],
        check=True
    )

    # For local traffic - OUTPUT chain in NAT table
    print("[*] Adding OUTPUT rule for local traffic (port 8081 -> 8080)...")
    subprocess.run(
        ["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "-d", "127.0.0.1",
         "--dport", "8081", "-j", "REDIRECT", "--to-port", "8080"],
        check=True
    )

    print("[+] iptables rules added successfully")


def show_iptables_rules():
    """Display the current iptables NAT table rules."""
    print("[*] Current NAT table rules:")
    result = subprocess.run(
        ["iptables", "-t", "nat", "-L", "-v", "-n"],
        capture_output=True,
        text=True
    )
    print(result.stdout)


def verify_forwarding():
    """Verify the port forwarding is working."""
    print("[*] Verifying port forwarding works...")

    # Test with curl to the redirected port
    print("[*] Testing with curl to localhost:8081...")
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:8081"],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(f"  HTTP Status via 8081: {result.stdout}")


def save_iptables_rules():
    """Save iptables rules to persist after reboot."""
    print("[*] Saving iptables rules for persistence...")

    # Save current rules to /etc/iptables/rules.v4 or fallback location
    save_paths = ["/etc/iptables/rules.v4", "/etc/sysconfig/iptables",
                  "/etc/iptables.rules"]

    saved = False
    for path in save_paths:
        try:
            with open(path, "w") as f:
                result = subprocess.run(
                    ["iptables-save"],
                    capture_output=True,
                    text=True
                )
                f.write(result.stdout)
            print(f"[+] Rules saved to {path}")
            saved = True
            break
        except (PermissionError, FileNotFoundError):
            continue

    if not saved:
        # Fallback: save to home directory
        home = subprocess.run(["echo", "$HOME"], capture_output=True, text=True).stdout.strip()
        save_path = f"{home}/iptables-rules-backup.txt"
        with open(save_path, "w") as f:
            result = subprocess.run(["iptables-save"], capture_output=True, text=True)
            f.write(result.stdout)
        print(f"[+] Rules saved to {save_path} (fallback location)")
        print("[!] Note: Restore with iptables-restore < /path/to/rules file")


def main():
    """Main function to demonstrate port forwarding setup."""
    print("=" * 60)
    print("Forward Traffic Between Ports")
    print("Company: Meta | Difficulty: Medium")
    print("=" * 60)
    print()

    # Step 1: Verify service is listening
    verify_service_listening()
    print()

    # Step 2: Setup iptables forwarding
    setup_iptables_forwarding()
    print()

    # Step 3: Show the rules
    show_iptables_rules()
    print()

    # Step 4: Verify forwarding works
    verify_forwarding()
    print()

    # Step 5: Save rules for persistence
    save_iptables_rules()

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  # Enable IP forwarding")
    print("  sysctl -w net.ipv4.ip_forward=1")
    print()
    print("  # Forward external traffic: port 8081 -> 8080")
    print("  iptables -t nat -A PREROUTING -p tcp --dport 8081 -j REDIRECT --to-port 8080")
    print()
    print("  # Forward local traffic: port 8081 -> 8080")
    print("  iptables -t nat -A OUTPUT -p tcp -d 127.0.0.1 --dport 8081 -j REDIRECT --to-port 8080")
    print()
    print("  # Save rules for persistence")
    print("  iptables-save > /etc/iptables/rules.v4")


if __name__ == "__main__":
    main()