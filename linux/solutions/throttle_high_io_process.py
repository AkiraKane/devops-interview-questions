#!/usr/bin/env python3
"""
Solution for: Throttle High I/O Process

Company: eBay | Difficulty: Easy

Scenario:
A server has latency spikes due to a runaway disk I/O process.

Task:
Identify the high I/O process using real-time monitoring tools, then apply
I/O throttling by changing its I/O scheduling class to idle without killing it.

Solution Approach:
- Use `iotop` or `/proc/<pid>/io` to identify high I/O processes
- Use `ionice -c 3 -p <pid>` to set the process to idle I/O class
- Verify the change with `ionice -p <pid>`
"""

import subprocess
import re


def find_high_io_process():
    """
    Find the process with the highest I/O activity.

    Reads from /proc/*/io to find the top I/O consumer.
    Returns (pid, command, read_bytes, write_bytes).
    """
    try:
        # Get all PIDs
        pids_result = subprocess.run(
            ['ls', '/proc'], capture_output=True, text=True
        )
        pids = [p for p in pids_result.stdout.split() if p.isdigit()]

        io_procs = []
        for pid in pids:
            try:
                # Read I/O stats from /proc
                with open(f'/proc/{pid}/io', 'r') as f:
                    io_stats = {}
                    for line in f:
                        key, val = line.strip().split(': ')
                        io_stats[key] = int(val)

                total_io = io_stats.get('read_bytes', 0) + io_stats.get('write_bytes', 0)
                if total_io > 0:
                    # Get command name
                    with open(f'/proc/{pid}/cmdline', 'r') as f:
                        cmd = f.read().replace('\x00', ' ').strip()
                    if not cmd:
                        with open(f'/proc/{pid}/comm', 'r') as f:
                            cmd = f.read().strip()

                    io_procs.append((pid, cmd, total_io))
            except (FileNotFoundError, PermissionError, ValueError):
                continue

        # Sort by total I/O descending
        io_procs.sort(key=lambda x: x[2], reverse=True)
        return io_procs[:5]

    except Exception as e:
        print(f"Error finding I/O processes: {e}")
        return []


def throttle_io(pid):
    """
    Set I/O scheduling class to idle (class 3) for a process.

    ionice classes: 1=realtime, 2=best-effort, 3=idle
    Idle class means the process only gets disk time when no other process needs it.
    """
    try:
        # Set to idle class
        result = subprocess.run(
            ['ionice', '-c', '3', '-p', str(pid)],
            capture_output=True, text=True, check=True
        )
        print(f"  Set PID {pid} to idle I/O class")

        # Verify
        verify = subprocess.run(
            ['ionice', '-p', str(pid)],
            capture_output=True, text=True
        )
        print(f"  Verified: {verify.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Failed to set ionice for PID {pid}: {e.stderr}")
        return False


def main():
    print("=== Throttle High I/O Process ===\n")

    print("Identifying high I/O processes...")
    top_procs = find_high_io_process()

    if not top_procs:
        print("No high I/O processes found (or insufficient permissions)")
        return

    print(f"\nTop I/O consumers:")
    for pid, cmd, total in top_procs:
        mb = total / (1024 * 1024)
        print(f"  PID {pid}: {cmd[:60]} ({mb:.1f} MB total I/O)")

    # Throttle the top offender
    target_pid = top_procs[0][0]
    target_cmd = top_procs[0][1]
    print(f"\n=== Throttling top offender: PID {target_pid} ({target_cmd[:40]}) ===")
    throttle_io(target_pid)

    print("\nNote: ionice -c 3 -p <PID> sets idle I/O class")
    print("The process still runs but yields disk access to other processes")


if __name__ == '__main__':
    main()
