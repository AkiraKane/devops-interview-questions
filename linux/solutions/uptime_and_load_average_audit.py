#!/usr/bin/env python3
"""
Solution for: Uptime and Load Average Audit

Company: Microsoft | Difficulty: Easy

Scenario:
A Linux server is under stability review.

Task:
Use the uptime command to extract the server uptime and the 15-minute load average,
saving each to separate files (uptime.txt and loadavg.txt).

Solution Approach:
- Run `uptime` and parse the output
- Extract uptime duration and save to uptime.txt
- Extract 15-minute load average and save to loadavg.txt
"""

import subprocess
import re
import os


def get_uptime_info():
    """
    Get system uptime and load averages.

    Parses `uptime` output which looks like:
    14:30:00 up 45 days, 3:22, 2 users, load average: 0.15, 0.25, 0.30
    """
    result = subprocess.run(['uptime'], capture_output=True, text=True)
    return result.stdout.strip()


def parse_uptime(uptime_output):
    """Parse uptime output into uptime string and load averages."""
    # Extract uptime portion (between "up" and "load average" or ",  X user")
    uptime_match = re.search(r'up\s+(.+?),\s+\d+\s+user', uptime_output)
    uptime_str = uptime_match.group(1).strip() if uptime_match else 'unknown'

    # Extract load averages
    load_match = re.search(r'load average:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)', uptime_output)
    if load_match:
        load_1 = load_match.group(1)
        load_5 = load_match.group(2)
        load_15 = load_match.group(3)
    else:
        load_1 = load_5 = load_15 = 'unknown'

    return uptime_str, load_1, load_5, load_15


def save_results(uptime_str, load_15, output_dir='/home/devops'):
    """Save uptime and load average to separate files."""
    os.makedirs(output_dir, exist_ok=True)

    uptime_file = os.path.join(output_dir, 'uptime.txt')
    loadavg_file = os.path.join(output_dir, 'loadavg.txt')

    with open(uptime_file, 'w') as f:
        f.write(f"Server uptime: {uptime_str}\n")
    print(f"Saved uptime to {uptime_file}")

    with open(loadavg_file, 'w') as f:
        f.write(f"15-minute load average: {load_15}\n")
    print(f"Saved load average to {loadavg_file}")


def main():
    output_dir = '/home/devops'

    print("=== Uptime and Load Average Audit ===\n")

    uptime_output = get_uptime_info()
    print(f"Raw uptime output: {uptime_output}")

    uptime_str, load_1, load_5, load_15 = parse_uptime(uptime_output)

    print(f"\nParsed values:")
    print(f"  Uptime: {uptime_str}")
    print(f"  Load averages: 1min={load_1}, 5min={load_5}, 15min={load_15}")

    save_results(uptime_str, load_15, output_dir)

    # Verify files
    for fname in ['uptime.txt', 'loadavg.txt']:
        path = os.path.join(output_dir, fname)
        with open(path) as f:
            print(f"  {fname}: {f.read().strip()}")


if __name__ == '__main__':
    main()
