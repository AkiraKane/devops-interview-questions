#!/usr/bin/env python3
"""
Network Packet Loss Diagnosis

Company: Cloudflare
Difficulty: Easy

Scenario:
Users are reporting random timeouts. You need to determine whether packet loss occurs
on the local network, upstream gateway, or public internet.

Task:
Find your default gateway IP, ping the gateway, DNS server (8.8.8.8), and google.com
(5 times each), collect packet loss and average latency from each, and write results
to /tmp/network_diagnostics.txt showing target name, IP/hostname, packet loss percentage,
and average latency.

Solution:
Use `ip route` to find the default gateway, then run `ping` commands with count=5
for each target and parse the output to extract packet loss and latency statistics.
"""

import subprocess
import re
import os


def get_default_gateway():
    """Find the default gateway IP address."""
    print("[*] Finding default gateway...")

    # Use ip route to get default gateway
    result = subprocess.run(
        ["ip", "route", "show", "default"],
        capture_output=True,
        text=True
    )

    # Parse output: default via <gateway_ip> dev <interface>
    match = re.search(r"via (\d+\.\d+\.\d+\.\d+)", result.stdout)

    if match:
        gateway = match.group(1)
        print(f"  Default gateway: {gateway}")
        return gateway
    else:
        print("  [!] Could not determine default gateway")
        return None


def ping_target(target, count=5):
    """
    Ping a target and return packet loss and average latency.

    Returns a tuple: (packet_loss_percent, avg_latency_ms)
    """
    print(f"[*] Pinging {target} ({count} times)...")

    # Run ping command
    # -c: count of pings
    # -W: timeout in seconds
    result = subprocess.run(
        ["ping", "-c", str(count), "-W", "2", target],
        capture_output=True,
        text=True,
        timeout=30
    )

    output = result.stdout + result.stderr
    print(f"  {output.strip()}")

    # Parse packet loss
    loss_match = re.search(r"(\d+)% packet loss", output)
    packet_loss = loss_match.group(1) if loss_match else "100"

    # Parse average latency
    # Look for "rtt min/avg/max/mdev = X/Y/Z/W" or "avg = X"
    latency_match = re.search(r"(?:rtt|round-trip) (?:min/)?(?:avg/)?.*?[:=]\s*([\d.]+)", output)
    if not latency_match:
        latency_match = re.search(r"(\d+\.\d+) ms", output)

    avg_latency = latency_match.group(1) if latency_match else "N/A"

    return packet_loss, avg_latency


def write_diagnostics(results):
    """Write the diagnostics results to a file."""
    print("[*] Writing diagnostics to /tmp/network_diagnostics.txt...")

    content = ""
    for name, ip, loss, latency in results:
        if latency == "N/A":
            content += f"{name} ({ip}): loss={loss}% avg={latency}\n"
        else:
            content += f"{name} ({ip}): loss={loss}% avg={latency} ms\n"
        print(f"  {name} ({ip}): loss={loss}% avg={latency} ms")

    with open("/tmp/network_diagnostics.txt", "w") as f:
        f.write(content)

    print(f"[+] Diagnostics written to /tmp/network_diagnostics.txt")


def main():
    """Main function to diagnose network packet loss."""
    print("=" * 60)
    print("Network Packet Loss Diagnosis")
    print("Company: Cloudflare | Difficulty: Easy")
    print("=" * 60)
    print()

    # Step 1: Find default gateway
    gateway = get_default_gateway()
    print()

    # Step 2: Define targets to ping
    targets = [
        ("Gateway", gateway if gateway else "192.168.1.1"),
        ("DNS", "8.8.8.8"),
        ("Internet", "google.com"),
    ]

    # Step 3: Ping each target and collect results
    results = []

    for name, ip in targets:
        try:
            loss, latency = ping_target(ip, count=5)
            results.append((name, ip, loss, latency))
        except Exception as e:
            print(f"  [!] Error pinging {name}: {e}")
            results.append((name, ip, "100", "N/A"))
        print()

    # Step 4: Write results to file
    write_diagnostics(results)

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  # Find default gateway")
    print("  ip route show default")
    print()
    print("  # Ping with statistics")
    print("  ping -c 5 -W 2 <target>")
    print()
    print("  # Results format:")
    print("  # <name> (<ip>): loss=<X>% avg=<Y> ms")


if __name__ == "__main__":
    main()