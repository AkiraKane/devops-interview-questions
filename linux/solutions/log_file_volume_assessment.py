#!/usr/bin/env python3
"""
Solution for Log File Volume Assessment

Company: JPMorgan
Difficulty: Easy

Scenario:
The `/var` directory contains logs from multiple applications, and cleanup
planning is needed. Some applications create their own subdirectories with
nested log files.

Task:
Find and count all files ending with `.log` under `/var`, save count to
`/home/devops/log_count.txt`, and find `.log` files larger than 512 KB,
saving that count to `/home/devops/large_log_count.txt`.

Solution Approach:
- Use `find` to locate all .log files under /var
- Count total files and save to log_count.txt
- Use find with -size to find files larger than 512K
- Count and save to large_log_count.txt
"""

import subprocess
import os


def find_log_files(directory='/var'):
    """
    Find all .log files under a directory.

    Returns:
        list: List of full paths to .log files
    """
    try:
        result = subprocess.run(
            ['find', directory, '-name', '*.log', '-type', 'f'],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return result.stdout.strip().split('\n')
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error finding log files: {e.stderr}")
        return []


def find_large_log_files(directory='/var', min_size='512k'):
    """
    Find all .log files larger than specified size.

    Args:
        directory: Directory to search
        min_size: Minimum file size (e.g., '512k', '1M')

    Returns:
        list: List of paths to large log files
    """
    try:
        result = subprocess.run(
            ['find', directory, '-name', '*.log', '-size', f'+{min_size}', '-type', 'f'],
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            return result.stdout.strip().split('\n')
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error finding large log files: {e.stderr}")
        return []


def save_count_to_file(count, filepath):
    """Save a count to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(str(count))

    print(f"Count saved to {filepath}")


def main():
    """Main function for log file volume assessment."""
    print("=== Log File Volume Assessment ===\n")

    # Find all .log files
    print("Searching for .log files under /var...")
    all_logs = find_log_files('/var')
    total_count = len(all_logs)

    print(f"Total .log files found: {total_count}")

    # Save total count
    save_count_to_file(total_count, '/home/devops/log_count.txt')

    # Find large .log files (>512KB)
    print("\nSearching for .log files larger than 512 KB...")
    large_logs = find_large_log_files('/var', '512k')
    large_count = len(large_logs)

    print(f"Large .log files (>512KB) found: {large_count}")

    if large_logs:
        print("\nLarge log files:")
        for log in large_logs[:10]:  # Show first 10
            try:
                size = os.path.getsize(log)
                size_mb = size / (1024 * 1024)
                print(f"  {log} ({size_mb:.1f} MB)")
            except:
                print(f"  {log}")

    # Save large file count
    save_count_to_file(large_count, '/home/devops/large_log_count.txt')

    print("\n=== Summary ===")
    print(f"Total .log files: {total_count}")
    print(f"Large .log files (>512KB): {large_count}")


if __name__ == '__main__':
    main()