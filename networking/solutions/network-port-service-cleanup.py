#!/usr/bin/env python3
"""
Network Port Service Cleanup

Company: Apple
Difficulty: Easy

Scenario:
A security audit found several unauthorized applications listening on high ports
(range 8000-9000).

Task:
Scan the system for listening TCP/UDP ports between 8000 and 9000. Identify the
Process IDs (PIDs) bound to these ports and terminate the associated services.

Solution:
Use `ss` or `netstat` to find listening ports in the specified range, extract
PIDs and process names, then use `kill` to terminate the services.
"""

import subprocess
import re
import signal
import os


def scan_ports(start_port=8000, end_port=9000):
    """Scan for listening ports in the specified range."""
    print(f"[*] Scanning for listening ports in range {start_port}-{end_port}...")

    # Use ss to find listening ports
    # -t: TCP
    # -u: UDP
    # -lt: listening TCP
    # -lu: listening UDP
    # -n: numeric ports

    all_ports = []

    # Check TCP listening ports
    tcp_result = subprocess.run(
        ["ss", "-tlnp"],
        capture_output=True,
        text=True
    )

    for line in tcp_result.stdout.split('\n'):
        # Look for ports in range
        for port in range(start_port, end_port + 1):
            if f":{port}" in line:
                all_ports.append(("tcp", line))

    # Check UDP ports
    udp_result = subprocess.run(
        ["ss", "-ulnp"],
        capture_output=True,
        text=True
    )

    for line in udp_result.stdout.split('\n'):
        for port in range(start_port, end_port + 1):
            if f":{port}" in line:
                all_ports.append(("udp", line))

    if all_ports:
        print(f"[+] Found {len(all_ports)} listening port(s) in range {start_port}-{end_port}")
        for proto, line in all_ports:
            print(f"  [{proto.upper()}] {line}")
    else:
        print(f"[+] No listening ports found in range {start_port}-{end_port}")

    return all_ports


def extract_pid_from_ss_line(line):
    """Extract PID/Process name from ss output line."""
    # ss output format for listening ports:
    # State  Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
    # LISTEN 0        511     127.0.0.1:8080      0.0.0.0:*          users:(("process_name",pid=<PID>,fd=<FD>))

    # Look for pid=<PID> in the line
    pid_match = re.search(r'pid=(\d+)', line)

    if pid_match:
        pid = pid_match.group(1)

        # Try to extract process name
        name_match = re.search(r'\("([^"]+)"', line)
        name = name_match.group(1) if name_match else "unknown"

        return pid, name

    return None, None


def kill_service(pid, name):
    """Terminate a service by PID."""
    print(f"[*] Terminating service '{name}' (PID: {pid})...")

    try:
        # Verify PID exists
        os.kill(int(pid), 0)  # Signal 0 just checks if process exists

        # Send SIGTERM for graceful shutdown
        os.kill(int(pid), signal.SIGTERM)
        print(f"  [+] Sent SIGTERM to PID {pid}")

        # Give it a moment to terminate
        import time
        time.sleep(0.5)

        # Check if still running
        try:
            os.kill(int(pid), 0)
            # Still running, try SIGKILL
            print(f"  [!] Process still running, sending SIGKILL...")
            os.kill(int(pid), signal.SIGKILL)
            print(f"  [+] Sent SIGKILL to PID {pid}")
        except OSError:
            # Process terminated
            print(f"  [+] Process terminated successfully")

    except OSError as e:
        if e.errno == 3:  # ESRCH - no such process
            print(f"  [!] Process {pid} not found (may have already terminated)")
        else:
            print(f"  [!] Error: {e}")


def main():
    """Main function to scan and cleanup unauthorized services."""
    print("=" * 60)
    print("Network Port Service Cleanup")
    print("Company: Apple | Difficulty: Easy")
    print("=" * 60)
    print()

    # Step 1: Scan for ports in range 8000-9000
    listening = scan_ports(8000, 9000)
    print()

    if not listening:
        print("[+] No unauthorized services found to clean up")
        return

    # Step 2: Extract PIDs and terminate each service
    pids_to_kill = set()

    for proto, line in listening:
        pid, name = extract_pid_from_ss_line(line)
        if pid:
            pids_to_kill.add((pid, name))

    print(f"[*] Identified {len(pids_to_kill)} unique service(s) to terminate")
    print()

    for pid, name in pids_to_kill:
        kill_service(pid, name)
        print()

    # Step 3: Verify cleanup
    print("[*] Verifying cleanup...")
    remaining = scan_ports(8000, 9000)

    print()
    print("[+] Solution complete!")
    print()
    print("Key commands used:")
    print("  # List TCP listening sockets")
    print("  ss -tlnp | grep ':80[0-9][0-9]'")
    print()
    print("  # List UDP listening sockets")
    print("  ss -ulnp | grep ':80[0-9][0-9]'")
    print()
    print("  # Terminate process")
    print("  kill -15 <PID>  # SIGTERM")
    print("  kill -9 <PID>   # SIGKILL if needed")


if __name__ == "__main__":
    main()