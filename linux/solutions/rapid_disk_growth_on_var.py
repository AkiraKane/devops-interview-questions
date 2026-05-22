#!/usr/bin/env python3
"""
Solution for Rapid Disk Growth on Var

Company: Google
Difficulty: Hard

Scenario:
Disk usage on the `/var` partition is at 92% and increasing rapidly. You need
to identify the largest files consuming space and determine if they're actively
used by processes or need log rotation.

Task:
Find the 10 largest files under /var and save to /home/devops/largest_var_files.txt,
check which processes are using these files and save to /home/devops/file_processes.txt,
and verify log rotation configuration for any log files found.

Solution Approach:
- Use `find` + `du` to find large files
- Use `lsof` to find processes using those files
- Check `/etc/logrotate.conf` and `/etc/logrotate.d/` for logrotate configuration
"""

import subprocess
import os
from collections import defaultdict


def find_largest_files(path='/var', limit=10):
    """
    Find the largest files under a path.

    Returns:
        list: List of (size_human, filepath) tuples
    """
    try:
        # Use find with -exec du to get sizes
        result = subprocess.run(
            ['find', path, '-type', 'f', '-exec', 'du', '-h', '{}', '+'],
            capture_output=True,
            text=True,
            check=False
        )

        files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    size = parts[0]
                    filepath = parts[1]
                    files.append((size, filepath))

        # Sort by size (need to convert for proper sorting)
        def size_to_bytes(s):
            if 'G' in s:
                return float(s.replace('G', '')) * 1024 * 1024 * 1024
            elif 'M' in s:
                return float(s.replace('M', '')) * 1024 * 1024
            elif 'K' in s:
                return float(s.replace('K', '')) * 1024
            return 0

        files.sort(key=lambda x: size_to_bytes(x[0]), reverse=True)

        return files[:limit]
    except subprocess.CalledProcessError as e:
        print(f"Error finding large files: {e.stderr}")
        return []


def find_processes_using_file(filepath):
    """Find processes that have a file open."""
    try:
        result = subprocess.run(
            ['lsof', filepath],
            capture_output=True,
            text=True,
            check=False
        )

        processes = []
        for line in result.stdout.strip().split('\n'):
            if line and 'COMMAND' not in line:
                processes.append(line)

        return processes
    except subprocess.CalledProcessError:
        return []


def check_logrotate_config():
    """Check logrotate configuration for log files."""
    configs = []

    # Check main config
    if os.path.exists('/etc/logrotate.conf'):
        configs.append(('Main config', '/etc/logrotate.conf'))

    # Check logrotate.d directory
    if os.path.isdir('/etc/logrotate.d'):
        for filename in os.listdir('/etc/logrotate.d'):
            configs.append(('Per-app config', f'/etc/logrotate.d/{filename}'))

    return configs


def main():
    """Main function to analyze rapid disk growth on /var."""
    print("=== Rapid Disk Growth on /var ===\n")

    output_largest = '/home/devops/largest_var_files.txt'
    output_processes = '/home/devops/file_processes.txt'
    output_logrotate = '/home/devops/logrotate_status.txt'

    # Ensure output directory exists
    os.makedirs('/home/devops', exist_ok=True)

    # Find largest files
    print("Finding largest files under /var...")
    largest_files = find_largest_files('/var', 10)

    # Save largest files
    print(f"Saving top 10 largest files to {output_largest}")
    with open(output_largest, 'w') as f:
        for size, filepath in largest_files:
            f.write(f"{size}\t{filepath}\n")

    # Print summary
    print("\nTop 10 largest files:")
    for size, filepath in largest_files:
        print(f"  {size}\t{filepath}")

    # Find processes using these files
    print(f"\nChecking which processes are using these files...")
    all_processes = []

    for size, filepath in largest_files:
        procs = find_processes_using_file(filepath)
        if procs:
            all_processes.extend([f"{filepath}: {p}" for p in procs])

    # Save process info
    print(f"Saving process info to {output_processes}")
    with open(output_processes, 'w') as f:
        for line in all_processes:
            f.write(f"{line}\n")

    if all_processes:
        print(f"Found {len(all_processes)} process(es) using large files")
    else:
        print("No processes found using these files (or files are not currently open)")

    # Check logrotate configuration
    print("\nChecking logrotate configuration...")
    configs = check_logrotate_config()

    with open(output_logrotate, 'w') as f:
        for config_type, config_path in configs:
            f.write(f"{config_type}: {config_path}\n")

    print(f"Saved logrotate status to {output_logrotate}")

    print("\n=== Summary ===")
    print(f"Largest file analysis saved to: {output_largest}")
    print(f"Process usage saved to: {output_processes}")
    print(f"Logrotate status saved to: {output_logrotate}")


if __name__ == '__main__':
    main()