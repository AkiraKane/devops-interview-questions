#!/usr/bin/env python3
"""
Solution for: Trace Process Service Ownership

Company: NVIDIA | Difficulty: Hard

Scenario:
A process is consuming excessive resources but its origin is unclear.

Task:
Write a bash script (/home/devops/trace_service.sh) that takes a PID, identifies
the managing systemd service, prints its full status, and shows the last 20
journal log entries.

Solution Approach:
- Read /proc/<pid>/cgroup to find the systemd service unit
- Use systemctl status to show service details
- Use journalctl -u to show recent log entries
"""

import subprocess
import os
import sys


def get_service_from_pid(pid):
    """
    Identify the systemd service that owns a given PID.

    Reads /proc/<pid>/cgroup to find the service unit name.
    """
    try:
        with open(f'/proc/{pid}/cgroup', 'r') as f:
            for line in f:
                # Look for systemd service slice
                if '.service' in line:
                    # Extract service name from cgroup path
                    # Format: <id>:<controller>:<path>
                    parts = line.strip().split(':')
                    if len(parts) >= 3:
                        path = parts[2]
                        # Extract service name from path
                        for segment in path.split('/'):
                            if segment.endswith('.service'):
                                return segment

        # Fallback: check if process has a systemd unit via systemctl
        result = subprocess.run(
            ['systemctl', 'list-units', '--type=service', '--all'],
            capture_output=True, text=True
        )
        # This is a less precise fallback
        return None

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error reading cgroup: {e}")
        return None


def get_service_status(service_name):
    """Get full systemctl status for a service."""
    result = subprocess.run(
        ['systemctl', 'status', service_name],
        capture_output=True, text=True
    )
    return result.stdout


def get_journal_logs(service_name, lines=20):
    """Get last N journal log entries for a service."""
    result = subprocess.run(
        ['journalctl', '-u', service_name, '-n', str(lines), '--no-pager'],
        capture_output=True, text=True
    )
    return result.stdout


def write_trace_script(script_path):
    """Write the trace_service.sh bash script."""
    script_content = '''#!/bin/bash
# trace_service.sh — Identify the systemd service managing a PID
# Usage: ./trace_service.sh <PID>

PID=$1

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

if [ ! -d "/proc/$PID" ]; then
    echo "Error: Process $PID does not exist"
    exit 1
fi

echo "=== Tracing service ownership for PID $PID ==="
echo ""

# Get process info
echo "--- Process Info ---"
ps -p "$PID" -o pid,ppid,user,comm,args --no-headers
echo ""

# Find service from cgroup
SERVICE=$(grep -oP '[^/]+\\.service' /proc/$PID/cgroup 2>/dev/null | head -1)

if [ -z "$SERVICE" ]; then
    echo "No systemd service found for PID $PID"
    echo "This process may be a standalone process or in a different cgroup."
    exit 0
fi

echo "Managing service: $SERVICE"
echo ""

# Show service status
echo "--- Service Status ---"
systemctl status "$SERVICE" --no-pager
echo ""

# Show last 20 journal entries
echo "--- Last 20 Journal Entries ---"
journalctl -u "$SERVICE" -n 20 --no-pager
'''

    os.makedirs(os.path.dirname(script_path), exist_ok=True)
    with open(script_path, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    print(f"Written script to {script_path}")


def main():
    script_path = '/home/devops/trace_service.sh'

    # Write the bash script
    write_trace_script(script_path)

    # If a PID argument is provided, also run the trace
    if len(sys.argv) > 1:
        pid = sys.argv[1]
        print(f"\n=== Running trace for PID {pid} ===\n")

        service = get_service_from_pid(pid)
        if service:
            print(f"Service: {service}")
            print("\n--- Service Status ---")
            print(get_service_status(service))
            print("\n--- Last 20 Journal Entries ---")
            print(get_journal_logs(service))
        else:
            print(f"No systemd service found for PID {pid}")
    else:
        print("\nScript created. Usage: /home/devops/trace_service.sh <PID>")
        print("\nOr run this script with a PID argument to trace directly.")


if __name__ == '__main__':
    main()
