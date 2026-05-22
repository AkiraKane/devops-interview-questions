#!/usr/bin/env python3
"""
Solution for Managing Process Overload

Company: Booking.com
Difficulty: Medium

Scenario:
The process count on a production server keeps increasing even though no new
workloads were deployed. Zombie processes are accumulating in the system.

Task:
Find all zombie processes, kill their parent processes to remove the zombies,
and confirm they are gone from the system.

Solution Approach:
- Use `ps` to identify zombie processes (state = Z)
- Find parent PIDs of zombies
- Kill the parent processes to reap the zombies
- Verify zombies are gone
"""

import subprocess


def find_zombie_processes():
    """
    Find all zombie processes.

    Returns:
        list: List of (pid, ppid, stat, command) tuples
    """
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True,
            check=True
        )

        zombies = []
        for line in result.stdout.split('\n'):
            # Zombie processes show as 'Z' or 'Z+' in STAT column
            if ' Z ' in line or line.strip().startswith('Z'):
                parts = line.split()
                if len(parts) >= 11:
                    pid = parts[1]
                    ppid = parts[2]
                    stat = parts[7]
                    cmd = ' '.join(parts[10:])
                    zombies.append({
                        'pid': pid,
                        'ppid': ppid,
                        'stat': stat,
                        'cmd': cmd
                    })

        return zombies
    except subprocess.CalledProcessError as e:
        print(f"Error finding zombies: {e.stderr}")
        return []


def kill_parent_process(ppid):
    """Kill a parent process to reap its zombie child."""
    try:
        # First try to gracefully terminate
        result = subprocess.run(
            ['kill', ppid],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            print(f"  Sent SIGTERM to parent PID {ppid}")
            return True

        # If that fails, try sudo
        result = subprocess.run(
            ['sudo', 'kill', ppid],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode == 0:
            print(f"  Sent SIGTERM to parent PID {ppid} (sudo)")
            return True

        return False
    except Exception as e:
        print(f"  Error killing parent {ppid}: {e}")
        return False


def force_kill_parent(ppid):
    """Force kill a stubborn parent process."""
    try:
        subprocess.run(['sudo', 'kill', '-9', ppid], check=False)
        print(f"  Sent SIGKILL to parent PID {ppid}")
        return True
    except:
        return False


def main():
    """Main function to manage process overload by removing zombies."""
    print("=== Managing Process Overload (Zombie Cleanup) ===\n")

    # Find zombie processes
    print("Scanning for zombie processes...")
    zombies = find_zombie_processes()

    if not zombies:
        print("No zombie processes found")
        return

    print(f"Found {len(zombies)} zombie process(es):")
    for z in zombies:
        print(f"  PID={z['pid']} PPID={z['ppid']} STAT={z['stat']} CMD={z['cmd'][:50]}")

    # Find unique parent PIDs
    parent_pids = set(z['ppid'] for z in zombies)
    print(f"\n{len(parent_pids)} unique parent process(es) to address: {parent_pids}")

    # Kill parent processes to reap zombies
    print("\n=== Killing Parent Processes ===")

    for ppid in parent_pids:
        print(f"Killing parent PID {ppid}...")

        # Get process info
        try:
            result = subprocess.run(
                ['ps', '-p', ppid, '-o', 'pid,ppid,stat,comm'],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  Parent info: {result.stdout.strip()}")
        except:
            print(f"  Parent {ppid} may have already exited")

        if not kill_parent_process(ppid):
            force_kill_parent(ppid)

    # Verify zombies are gone
    print("\n=== Verification ===")
    remaining = find_zombie_processes()

    if remaining:
        print(f"WARNING: {len(remaining)} zombie(s) still remain:")
        for z in remaining:
            print(f"  PID={z['pid']} CMD={z['cmd'][:50]}")
    else:
        print("SUCCESS: No zombie processes remaining")


if __name__ == '__main__':
    main()