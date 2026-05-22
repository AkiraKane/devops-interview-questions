#!/usr/bin/env python3
"""
Solution for Discover Unexpected Background Jobs

Company: Plus500
Difficulty: Medium

Scenario:
You have noticed an unexpected spike in system load. You suspect a batch of
recently spawned jobs is responsible and need to isolate processes that started
within the last few minutes.

Task:
Identify all processes started within the last 10 minutes and save their PID,
User, Start Date (lstart), and Command to `/home/devops/recent_processes.txt`.
Once recent processes written to the file, Terminate the Suspicious processes
(i.e. any process that doesn't belong to the root user or systemd).

Solution Approach:
- Use ps to list processes with lstart (start time)
- Filter processes started within the last 10 minutes
- Write to file, then kill non-root/system processes
"""

import subprocess
import os
from datetime import datetime, timedelta


def get_recent_processes(minutes=10):
    """
    Get processes started within the last N minutes.

    Returns:
        list: List of process dictionaries
    """
    try:
        # ps with lstart shows full start time/date
        result = subprocess.run(
            ['ps', 'eo', 'pid,user,lstart,args', '--sort=+lstart'],
            capture_output=True,
            text=True,
            check=True
        )

        recent_processes = []
        cutoff_time = datetime.now() - timedelta(minutes=minutes)

        for line in result.stdout.split('\n'):
            if line.strip():
                # Parse: PID USER START_TIME COMMAND
                # lstart format: "Thu May 22 10:30:45 2025"
                parts = line.split(None, 3)

                if len(parts) >= 4:
                    try:
                        pid = parts[0]
                        user = parts[1]
                        # The date string is "Day Month Date Time Year"
                        date_str = parts[2] + ' ' + parts[3]

                        # Parse the lstart format
                        # Example: "Wed May 22 10:30:45 2025"
                        start_time = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")

                        if start_time >= cutoff_time:
                            recent_processes.append({
                                'pid': pid,
                                'user': user,
                                'lstart': date_str,
                                'command': parts[-1]
                            })
                    except (ValueError, IndexError):
                        continue

        return recent_processes
    except subprocess.CalledProcessError as e:
        print(f"Error getting processes: {e.stderr}")
        return []


def write_recent_processes_to_file(processes, filename):
    """Write recent processes to a file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w') as f:
        f.write(f"{'PID':<10} {'USER':<12} {'STARTED':<35} {'CMD'}\n")
        f.write("-" * 100 + "\n")

        for proc in processes:
            f.write(f"{proc['pid']:<10} {proc['user']:<12} {proc['lstart']:<35} {proc['command'][:50]}\n")

    print(f"Recent processes written to {filename}")


def kill_suspicious_processes(processes):
    """
    Kill processes that don't belong to root or systemd.
    These are considered "suspicious" for this scenario.
    """
    protected_users = ['root', 'systemd', 'root']

    killed = []
    for proc in processes:
        if proc['user'] not in protected_users:
            print(f"Killing suspicious process: PID={proc['pid']} USER={proc['user']} CMD={proc['command'][:30]}")
            try:
                subprocess.run(['kill', proc['pid']], check=True)
                killed.append(proc['pid'])
            except subprocess.CalledProcessError:
                # Try sudo if kill fails
                try:
                    subprocess.run(['sudo', 'kill', proc['pid']], check=True)
                    killed.append(proc['pid'])
                except:
                    print(f"  Could not kill PID {proc['pid']}")

    return killed


def main():
    """Main function to discover and handle recent background jobs."""
    output_file = '/home/devops/recent_processes.txt'

    print("=== Discovering Unexpected Background Jobs ===\n")
    print(f"Looking for processes started within the last 10 minutes...\n")

    processes = get_recent_processes(10)

    if not processes:
        print("No processes found started within the last 10 minutes")
        return

    print(f"Found {len(processes)} recent process(es):\n")
    for proc in processes:
        print(f"  PID={proc['pid']} USER={proc['user']} TIME={proc['lstart']} CMD={proc['command'][:40]}")

    # Write to file
    write_recent_processes_to_file(processes, output_file)

    # Kill suspicious processes (not root or systemd)
    print("\n=== Terminating Suspicious Processes ===")
    killed = kill_suspicious_processes(processes)

    print(f"\nTerminated {len(killed)} suspicious process(es)")


if __name__ == '__main__':
    main()