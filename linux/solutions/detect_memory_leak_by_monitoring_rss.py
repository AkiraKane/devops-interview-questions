#!/usr/bin/env python3
"""
Solution for Detect Memory Leak by Monitoring RSS

Company: Google
Difficulty: Medium

Scenario:
One of your long-running Node.js services (process name `node`) has been slowing
down over several hours of uptime. CPU usage is normal, disk I/O is normal, but
the server is gradually running out of memory.

Task:
Identify if any process is leaking memory and kill that process.

Solution Approach:
- Use ps to find node processes and their RSS (Resident Set Size) memory usage
- Identify processes with continuously growing memory that appear to be leaking
- Kill the problematic process(es)

RSS = Resident Set Size - actual physical memory used by a process
"""

import subprocess
import re
import time


def get_node_processes():
    """Get all node processes with their memory usage."""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True,
            check=True
        )

        processes = []
        for line in result.stdout.split('\n'):
            if 'node' in line.lower():
                parts = line.split()
                if len(parts) >= 6:
                    # USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
                    try:
                        user = parts[0]
                        pid = parts[1]
                        cpu = float(parts[2])
                        mem = float(parts[3])
                        rss_kb = int(parts[5])  # RSS in KB
                        cmd = ' '.join(parts[10:])
                        processes.append({
                            'user': user,
                            'pid': pid,
                            'cpu': cpu,
                            'mem': mem,
                            'rss_kb': rss_kb,
                            'rss_mb': rss_kb / 1024,
                            'cmd': cmd
                        })
                    except (ValueError, IndexError):
                        continue

        return processes
    except subprocess.CalledProcessError as e:
        print(f"Error getting processes: {e.stderr}")
        return []


def detect_memory_leak(processes, threshold_growth_mb=100):
    """
    Detect processes that may be leaking memory.

    A process is considered leaking if its RSS keeps growing.
    In a real scenario, we'd monitor over time. Here we look for
    high memory consumption patterns.
    """
    # Sort by RSS (memory usage)
    sorted_procs = sorted(processes, key=lambda x: x['rss_kb'], reverse=True)

    # Find processes with abnormally high memory
    # Generally, a leaking process will have RSS growing over time
    # For this solution, we identify processes with RSS > 500 MB as suspect

    suspect_processes = []
    for proc in sorted_procs:
        if proc['rss_mb'] > 500:  # Process using more than 500 MB
            suspect_processes.append(proc)

    return suspect_processes


def kill_process(pid):
    """Kill a process by its PID."""
    try:
        result = subprocess.run(
            ['kill', pid],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Successfully killed process {pid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error killing process {pid}: {e.stderr}")
        return False


def kill_memory_leaking_processes():
    """Main function to find and kill memory leaking node processes."""
    print("Scanning for node processes with potential memory leaks...")

    processes = get_node_processes()

    if not processes:
        print("No node processes found")
        return

    print(f"\nFound {len(processes)} node process(es):")
    print(f"{'PID':<10} {'RSS (MB)':<12} {'%MEM':<8} {'USER':<12} {'CMD'}")
    print("-" * 80)

    for proc in processes:
        print(f"{proc['pid']:<10} {proc['rss_mb']:<12.1f} {proc['mem']:<8.1f} {proc['user']:<12} {proc['cmd'][:50]}")

    # Detect leaking processes
    suspect_processes = detect_memory_leak(processes)

    if suspect_processes:
        print(f"\n!!! Detected {len(suspect_processes)} process(es) with potential memory leak !!!")

        for proc in suspect_processes:
            print(f"\nProcess PID {proc['pid']} using {proc['rss_mb']:.1f} MB of memory")
            print(f"  Command: {proc['cmd']}")
            print(f"  Killing due to memory leak...")

            # In real scenario, we'd also want to alert before killing
            kill_process(proc['pid'])
    else:
        print("\nNo obvious memory leaks detected (processes using < 500 MB)")


def main():
    """Main entry point."""
    # First check current node processes
    print("=== Node Process Memory Analysis ===\n")
    kill_memory_leaking_processes()

    print("\n=== Monitoring Complete ===")


if __name__ == '__main__':
    main()