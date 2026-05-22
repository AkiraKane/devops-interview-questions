#!/usr/bin/env python3
"""
Solution for CPU Resource Management Priority

Company: RedHat
Difficulty: Easy

Scenario:
During peak traffic hours, a background `data-processing` job that is started by
user `devops` is consuming too much CPU and slowing down user-facing services.
Stopping it isn't an option because it would interrupt ongoing workflows, but you
need to limit its CPU usage temporarily.

Task:
Reduce the process's priority to 10 while keeping it running.

Solution Approach:
- Find the data-processing process running as devops user
- Use `renice` to adjust the process priority (lower nice value = higher priority)
- To reduce priority/limit CPU, we use a higher nice value (10)

Note: Nice values range from -20 (highest priority) to 19 (lowest priority).
To reduce a process's CPU share, we increase its nice value.
"""

import subprocess
import re


def find_data_processing_pid():
    """Find the PID of the data-processing job running as devops user."""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.split('\n'):
            if 'data-processing' in line or 'data-processor' in line or 'data_processing' in line:
                # Skip the header and grep itself
                if 'devops' in line and 'ps aux' not in line:
                    parts = line.split()
                    # Format: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
                    pid = parts[1]
                    return pid, line.strip()

        return None, None
    except subprocess.CalledProcessError as e:
        print(f"Error finding process: {e.stderr}")
        return None, None


def renice_process(pid, priority):
    """
    Change the priority of a process using renice.

    Args:
        pid: Process ID
        priority: New nice value (10 to reduce priority, lower values increase priority)
    """
    try:
        result = subprocess.run(
            ['renice', str(priority), '-p', pid],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Successfully adjusted priority of PID {pid} to nice value {priority}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adjusting priority: {e.stderr}")
        return False


def get_process_nice(pid):
    """Get the current nice value of a process."""
    try:
        result = subprocess.run(
            ['ps', '-o', 'nice=', '-p', pid],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def main():
    """Main function to reduce process priority to 10."""
    target_priority = 10

    print(f"Looking for data-processing job running as devops user...")

    pid, process_info = find_data_processing_pid()

    if not pid:
        print("No data-processing job found running as devops user")
        print("Searching for any data-processing related processes...")

        # List all data-processing related processes for debugging
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.split('\n'):
                if 'data' in line.lower() and 'devops' in line:
                    print(f"  Found: {line}")
        except:
            pass

        print("\nNote: In a real scenario, this would find the actual process.")
        print(f"To manually renice a process, use: renice {target_priority} -p <PID>")
        return

    print(f"Found process:\n  {process_info}")

    current_nice = get_process_nice(pid)
    print(f"Current nice value: {current_nice}")

    print(f"\nAdjusting priority to {target_priority}...")
    renice_process(pid, target_priority)

    new_nice = get_process_nice(pid)
    print(f"New nice value: {new_nice}")


if __name__ == '__main__':
    main()