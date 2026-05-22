#!/usr/bin/env python3
"""
Network Socket Usage Analysis

Company: SAP
Difficulty: Easy

Scenario:
Network latency issues were reported due to opening too many TCP connections.

Task:
Inspect active sockets along with the processes that own them to identify which
application is responsible for the excessive connection count. Save all currently
active TCP/UDP connections (ESTABLISHED, LISTEN, TIME_WAIT, etc.) output to
/tmp/active_tcp.txt

Solution:
Use the `ss` command to display all socket statistics including process information,
then filter and format the output to show which processes have the most connections.
"""

import subprocess
import re
from collections import Counter


def get_all_connections():
    """Get all active TCP and UDP connections."""
    print("[*] Retrieving all active TCP/UDP connections...")

    # ss options:
    # -a: all sockets (including listening)
    # -t: TCP
    # -u: UDP
    # -n: numeric (don't resolve hostnames)
    # -p: show process information

    result = subprocess.run(
        ["ss", "-a", "-tunp"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  [!] ss command failed: {result.stderr}")
        return None

    return result.stdout


def parse_connection_line(line):
    """Parse a single connection line from ss output."""
    # ss output format:
    # Netid  State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
    # tcp    ESTAB   0       0       192.168.1.50:22     192.168.1.100:54321  users:(("sshd",pid=1234,fd=3))

    parts = line.split()

    if len(parts) < 5:
        return None

    try:
        netid = parts[0]
        state = parts[1]

        # Parse local address
        local = parts[4]

        # Parse peer address
        peer = parts[5] if len(parts) > 5 else "*:*"

        # Extract process info if present
        pid_info = None
        if len(parts) > 6:
            pid_info = " ".join(parts[6:])

        return {
            'netid': netid,
            'state': state,
            'local': local,
            'peer': peer,
            'process': pid_info
        }
    except (ValueError, IndexError):
        return None


def analyze_connections():
    """Analyze connections to identify problematic processes."""
    print("[*] Analyzing connections...")

    connections_raw = get_all_connections()

    if not connections_raw:
        return

    lines = connections_raw.split('\n')

    # Skip header line
    data_lines = [l for l in lines[1:] if l.strip()]

    connections = []
    for line in data_lines:
        conn = parse_connection_line(line)
        if conn:
            connections.append(conn)

    print(f"  Total connections parsed: {len(connections)}")

    # Count connections by process
    process_counts = Counter()

    for conn in connections:
        if conn['process']:
            # Extract process name and PID from process info
            # Format: users:(("name",pid=XXX,fd=YYY))
            match = re.search(r'\("([^"]+)"', conn['process'])
            if match:
                process_name = match.group(1)
                process_counts[process_name] += 1

    print()
    print("[*] Top processes by connection count:")
    for process, count in process_counts.most_common(10):
        print(f"  {process}: {count} connection(s)")

    return connections


def save_connections():
    """Save all active connections to a file."""
    print("[*] Saving all connections to /tmp/active_tcp.txt...")

    result = subprocess.run(
        ["ss", "-a", "-tunp"],
        capture_output=True,
        text=True
    )

    with open("/tmp/active_tcp.txt", "w") as f:
        f.write(result.stdout)

    print(f"[+] Saved {len(result.stdout.split(chr(10)))} lines to /tmp/active_tcp.txt")

    # Display the file contents
    print()
    print("[*] Contents of /tmp/active_tcp.txt:")
    print("-" * 80)
    print(result.stdout)
    print("-" * 80)


def main():
    """Main function to analyze network socket usage."""
    print("=" * 60)
    print("Network Socket Usage Analysis")
    print("Company: SAP | Difficulty: Easy")
    print("=" * 60)
    print()

    # Step 1: Get all connections
    print("[*] Displaying all active connections:")
    print()

    result = subprocess.run(
        ["ss", "-a", "-tunp"],
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 2: Analyze
    print()
    analyze_connections()

    # Step 3: Save to file
    print()
    save_connections()

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  # Show all TCP/UDP sockets with process info")
    print("  ss -a -tunp")
    print()
    print("  # Show only ESTABLISHED connections")
    print("  ss -tun state established")
    print()
    print("  # Filter by state")
    print("  ss -tun state time-wait")
    print()


if __name__ == "__main__":
    main()