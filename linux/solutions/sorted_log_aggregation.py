#!/usr/bin/env python3
"""
Solution for: Sorted Log Aggregation

Company: Airbnb | Difficulty: Easy

Scenario:
A log file has entries from multiple servers in mixed order.

Task:
Sort the log by timestamp (earliest first), then by hostname for ties,
and save the sorted output to a new file.

Solution Approach:
- Read the log file and parse each line to extract timestamp and hostname
- Sort by (timestamp, hostname) using the `sort` command or Python
- Save the sorted output to a new file
"""

import subprocess
import os


def sort_log(input_file, output_file):
    """
    Sort a log file by timestamp (column 1) then hostname (column 2).

    Assumes log format: <timestamp> <hostname> <message...>
    Uses the system `sort` command for efficiency on large files.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist")
        return False

    # Use sort command: -k1,1 for timestamp field, -k2,2 for hostname field
    # -s for stable sort (preserves relative order of equal keys)
    result = subprocess.run(
        ['sort', '-k1,1', '-k2,2', '-o', output_file, input_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error sorting: {result.stderr}")
        return False

    print(f"Sorted log saved to {output_file}")

    # Show line count comparison
    original = subprocess.run(['wc', '-l', input_file], capture_output=True, text=True)
    sorted_out = subprocess.run(['wc', '-l', output_file], capture_output=True, text=True)
    print(f"Original: {original.stdout.strip()}")
    print(f"Sorted:   {sorted_out.stdout.strip()}")

    return True


def verify_sort(output_file):
    """Verify the output file is sorted by timestamp."""
    result = subprocess.run(
        ['sort', '-c', '-k1,1', '-k2,2', output_file],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("VERIFIED: Output is correctly sorted by timestamp and hostname")
    else:
        print(f"WARNING: Output may not be fully sorted: {result.stderr}")


def main():
    input_file = '/var/log/aggregated.log'
    output_file = '/var/log/aggregated_sorted.log'

    print("=== Sorted Log Aggregation ===\n")
    print(f"Sorting {input_file} by timestamp then hostname...")

    if sort_log(input_file, output_file):
        verify_sort(output_file)

        # Show first and last 5 lines as preview
        print("\n--- First 5 lines ---")
        head = subprocess.run(['head', '-5', output_file], capture_output=True, text=True)
        print(head.stdout)

        print("--- Last 5 lines ---")
        tail = subprocess.run(['tail', '-5', output_file], capture_output=True, text=True)
        print(tail.stdout)


if __name__ == '__main__':
    main()
