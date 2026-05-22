#!/usr/bin/env python3
"""
Solution for Analyzing Log Partition Usage

Company: RedHat
Difficulty: Medium

Scenario:
Log rotation has stopped working correctly, and you suspect that `/var/log` might be
mounted on a different filesystem with limited space or incorrect mount options.

Task:
Determine which filesystem or device `/var/log` is mounted on, including device name,
mount point, filesystem type, size, and usage. Save the findings to
`/home/devops/varlog_filesystem_info.txt`. Optionally identify if this filesystem
differs from `/` which could provide additional info on causes of log rotation or space issues.

Solution Approach:
- Use `df -h /var/log` to get filesystem info for /var/log
- Use `mount | grep /var/log` to get detailed mount information
- Compare with `/` filesystem to identify differences
"""

import subprocess
import os


def get_filesystem_info(path):
    """Get filesystem information for a given path."""
    try:
        # Get df output for the path
        df_result = subprocess.run(
            ['df', '-h', path],
            capture_output=True,
            text=True,
            check=True
        )
        return df_result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running df: {e.stderr}"


def get_mount_details(path):
    """Get detailed mount information for a given path."""
    try:
        # Get mount info using findmnt
        findmnt_result = subprocess.run(
            ['findmnt', '-J', path],
            capture_output=True,
            text=True,
            check=False
        )
        if findmnt_result.returncode == 0:
            return findmnt_result.stdout

        # Fallback to mount | grep
        mount_result = subprocess.run(
            ['mount'],
            capture_output=True,
            text=True,
            check=True
        )
        lines = [line for line in mount_result.stdout.split('\n') if path in line]
        return '\n'.join(lines) if lines else "No mount info found"
    except subprocess.CalledProcessError as e:
        return f"Error getting mount details: {e.stderr}"


def get_root_filesystem_info():
    """Get filesystem information for root filesystem."""
    return get_filesystem_info('/')


def main():
    """Main function to analyze /var/log filesystem and save results."""
    output_file = '/home/devops/varlog_filesystem_info.txt'

    varlog_info = get_filesystem_info('/var/log')
    varlog_mount = get_mount_details('/var/log')
    root_info = get_root_filesystem_info()

    content = f"""=== Filesystem Analysis for /var/log ===

=== Disk Usage for /var/log ===
{varlog_info}

=== Mount Details for /var/log ===
{varlog_mount}

=== Root Filesystem (/) for comparison ===
{root_info}

=== Analysis ===
"""

    # Detect if /var/log is on a different filesystem
    if '/var/log' not in varlog_mount:
        content += "\n/var/log appears to be on the same filesystem as /\n"
    else:
        content += "\n/var/log is on a DIFFERENT filesystem from /\n"
        content += "This could cause log rotation issues if that partition is full.\n"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(content)

    print(f"Filesystem info saved to {output_file}")
    print("\nFilesystem Analysis:")
    print(varlog_info)


if __name__ == '__main__':
    main()