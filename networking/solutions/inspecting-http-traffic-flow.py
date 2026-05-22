#!/usr/bin/env python3
"""
Inspecting HTTP Traffic Flow

Company: Airbnb
Difficulty: Medium

Scenario:
You suspect the web service isn't receiving HTTP requests, and you need to confirm
network traffic to port 80.

Task:
Capture network packets destined for or originating from port 80 (HTTP traffic),
limit the capture to the first 10 packets to avoid large files, save the captured
packets to /tmp/http_traffic.pcap in pcap format, read the capture file and extract
key information (source IP, destination IP with port, TCP flags), create a human-readable
summary showing packet flow and TCP handshake details, and save the summary to
/tmp/http_summary.txt in the format SOURCE_IP -> DEST_IP:PORT [FLAGS].

Solution:
Use tcpdump to capture packets and generate a pcap file, then parse the capture
with tcpdump or tshark to extract the required information.
"""

import subprocess
import re
import os


def capture_http_packets():
    """Capture HTTP traffic packets destined to or from port 80."""
    print("[*] Capturing first 10 HTTP packets (port 80)...")

    # Remove old capture file if exists
    capture_file = "/tmp/http_traffic.pcap"
    if os.path.exists(capture_file):
        os.remove(capture_file)

    # Capture packets using tcpdump
    # -i any: capture on all interfaces
    # -c 10: limit to 10 packets
    # port 80: filter for HTTP traffic
    # -w: write to pcap file
    result = subprocess.run(
        ["tcpdump", "-i", "any", "-c", "10", "port", "80", "-w", capture_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  tcpdump error: {result.stderr}")
    else:
        print(f"[+] Captured packets saved to {capture_file}")


def parse_pcap_file():
    """Parse the pcap file and extract packet information."""
    print("[*] Reading captured packets from pcap file...")

    capture_file = "/tmp/http_traffic.pcap"

    if not os.path.exists(capture_file):
        print(f"[!] Capture file {capture_file} not found")
        return None

    # Use tcpdump to read and display packet details
    # -r: read from file
    # -n: don't resolve hostnames
    # -tttt: timestamped output
    result = subprocess.run(
        ["tcpdump", "-r", capture_file, "-n", "-tttt"],
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else result.stderr)
    return result.stdout


def generate_summary():
    """Generate human-readable summary of HTTP packet flow."""
    print("[*] Generating HTTP traffic summary...")

    capture_file = "/tmp/http_traffic.pcap"
    summary_file = "/tmp/http_summary.txt"

    if not os.path.exists(capture_file):
        print(f"[!] Capture file {capture_file} not found")
        return

    # Extract source/destination IP:port and flags using tcpdump
    # Filter for IP packets with flags
    result = subprocess.run(
        ["tcpdump", "-r", capture_file, "-n", "-tttt",
         'ip and tcp'],
        capture_output=True,
        text=True
    )

    lines = result.stdout.split('\n') if result.stdout else []

    # Parse each line to extract SOURCE_IP -> DEST_IP:PORT [FLAGS] format
    summary_lines = []

    for line in lines:
        # Look for IPv4 packets (skip IPv6)
        if 'IP6' in line:
            continue

        # Extract source IP:port and destination IP:port
        # Pattern: IP source_ip.src_port > dest_ip.dest_port
        match = re.search(
            r'IP (\d+\.\d+\.\d+\.\d+)\.(\d+) > (\d+\.\d+\.\d+\.\d+)\.(\d+)',
            line
        )

        if match:
            src_ip = match.group(1)
            src_port = match.group(2)
            dst_ip = match.group(3)
            dst_port = match.group(4)

            # Extract TCP flags from the line
            flags_match = re.search(r'Flags \[([^\]]+)\]', line)
            if flags_match:
                flags = f"[{flags_match.group(1)}]"
                summary_line = f"{src_ip}:{src_port} -> {dst_ip}:{dst_port} {flags}"
            else:
                summary_line = f"{src_ip}:{src_port} -> {dst_ip}:{dst_port}"

            summary_lines.append(summary_line)
            print(f"  {summary_line}")

    # Write summary to file
    with open(summary_file, "w") as f:
        for line in summary_lines:
            f.write(line + "\n")

    print(f"[+] Summary saved to {summary_file}")


def demonstrate_tcpdump_usage():
    """Demonstrate common tcpdump commands for troubleshooting."""
    print()
    print("[*] Demonstrating tcpdump usage for HTTP traffic inspection:")
    print()
    print("  # Capture HTTP packets on all interfaces (first 10 packets)")
    print("  tcpdump -i any -c 10 port 80 -w /tmp/http_traffic.pcap")
    print()
    print("  # Read and display pcap file")
    print("  tcpdump -r /tmp/http_traffic.pcap -n")
    print()
    print("  # Show only SYN packets (connection establishment)")
    print("  tcpdump -r /tmp/http_traffic.pcap 'tcp[tcpflags] == tcp-syn'")
    print()
    print("  # Show only packets with ACK flag")
    print("  tcpdump -r /tmp/http_traffic.pcap 'tcp[13] & 16 != 0'")


def main():
    """Main function to demonstrate HTTP traffic inspection."""
    print("=" * 60)
    print("Inspecting HTTP Traffic Flow")
    print("Company: Airbnb | Difficulty: Medium")
    print("=" * 60)
    print()

    # Step 1: Capture HTTP packets
    capture_http_packets()
    print()

    # Step 2: Parse the pcap file
    parse_pcap_file()
    print()

    # Step 3: Generate human-readable summary
    generate_summary()
    print()

    # Additional: Demonstrate tcpdump usage
    demonstrate_tcpdump_usage()

    print()
    print("[+] Solution complete!")


if __name__ == "__main__":
    main()