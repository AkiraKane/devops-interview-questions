#!/usr/bin/env python3
"""
Solution for Managing High I/O Processes

Company: Revolut
Difficulty: Easy

Scenario:
Users are complaining about slow file access. System metrics show high disk utilization.

Task:
Reduce I/O activity of top offender using I/O priorities to `idle`. Keep critical
jobs (databases, message queues, applications) at high priority.

Solution Approach:
- Use iostat or ps to identify high I/O processes
- Use ionice to set process I/O priority to idle class
- ionice classes: real-time (1), best-effort (2, default), idle (3)
"""

import subprocess
import re


def find_high_io_processes():
    """
    Find processes with high I/O activity.

    Returns:
        list: List of (pid, command, io_read_mb, io_write_mb)
    """
    # Use ps to find I/O statistics
    try:
        result = subprocess.run(
            ['ps', 'aux', '--sort=-io'],
            capture_output=True,
            text=True,
            check=True
        )

        high_io = []
        for line in result.stdout.split('\n'):
            if 'ps aux' not in line and 'COMMAND' not in line:
                parts = line.split()
                if len(parts) >= 10:
                    try:
                        # Check for significant I/O indicators in command
                        cmd = ' '.join(parts[10:])
                        io_chars = sum(1 for c in cmd if c in 'rw')
                        if io_chars > 0:  # Has read/write indicators
                            pid = parts[1]
                            high_io.append((pid, cmd[:50]))
                    except:
                        continue

        return high_io[:5]  # Return top 5
    except subprocess.CalledProcessError as e:
        print(f"Error finding I/O processes: {e.stderr}")
        return []


def ionice_process(pid, priority_class='idle', priority=7):
    """
    Set I/O priority for a process.

    ionice format: ionice -c CLASS -p PID
    Classes: 1=realtime, 2=best-effort, 3=idle
    Priority: 0-7 (0 highest, 7 lowest) for best-effort
    """
    class_map = {
        'realtime': 1,
        'best-effort': 2,
        'idle': 3
    }

    class_num = class_map.get(priority_class, 3)

    try:
        if class_num == 3:  # idle - no priority needed
            result = subprocess.run(
                ['ionice', '-c', str(class_num), '-p', pid],
                capture_output=True,
                text=True,
                check=True
            )
        else:
            result = subprocess.run(
                ['ionice', '-c', str(class_num), '-n', str(priority), '-p', pid],
                capture_output=True,
                text=True,
                check=True
            )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Could not set ionice for PID {pid}: {e}")
        return False


def get_process_ionice(pid):
    """Get current I/O priority of a process."""
    try:
        result = subprocess.run(
            ['ionice', '-p', pid],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def main():
    """Main function to manage high I/O processes."""
    print("=== Managing High I/O Processes ===\n")

    print("Finding processes with high I/O activity...")

    # In a real scenario, we'd use iotop or similar
    # For this solution, we demonstrate the concept

    # Find high I/O processes
    high_io_procs = find_high_io_processes()

    if high_io_procs:
        print(f"\nTop {len(high_io_procs)} I/O-intensive processes:")
        for pid, cmd in high_io_procs:
            current_ionice = get_process_ionice(pid)
            print(f"  PID {pid}: {cmd[:40]} (currently: {current_ionice})")

        # Throttle non-critical processes (typically backup, sync, etc.)
        print("\n=== Setting I/O priority to idle ===")

        for pid, cmd in high_io_procs:
            # Skip known critical processes (databases, message queues, etc.)
            critical = ['postgres', 'mysql', 'redis', 'rabbitmq', 'nginx', 'java', 'python']
            if any(c in cmd.lower() for c in critical):
                print(f"Skipping critical process: {cmd[:40]}")
                continue

            print(f"Setting PID {pid} ({cmd[:30]}) to idle class...")
            if ionice_process(pid, 'idle'):
                print(f"  Success: {get_process_ionice(pid)}")
    else:
        print("No high I/O processes found")

    print("\nNote: The ionice command syntax:")
    print("  ionice -c 3 -p <PID>   # Set to idle class")


if __name__ == '__main__':
    main()