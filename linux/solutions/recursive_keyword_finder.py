#!/usr/bin/env python3
"""
Solution for Recursive Keyword Finder

Company: X (Twitter)
Difficulty: Easy

Scenario:
Multiple applications write logs under /var/log, and you need to quickly check
if any recent errors have been recorded.

Task:
Search recursively under /var/log for all files ending with `.log`, print every
line that contains the text `ERROR`, ensure output includes filename and matching
line, and save results to /home/devops/error_logs.txt.

Solution Approach:
- Use `grep -r` or `grep -d recurse` to search recursively
- Use `grep -l` to find .log files, then grep each for ERROR
- Save results with filename prefix
"""

import subprocess
import os


def search_logs_for_errors(log_dir='/var/log', output_file='/home/devops/error_logs.txt'):
    """
    Search for ERROR in all .log files under log_dir.

    Args:
        log_dir: Directory to search
        output_file: File to save results

    Returns:
        int: Number of matches found
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Use grep to recursively search for ERROR in .log files
    # -r: recursive
    # -H: always print filename
    # --include: only .log files
    try:
        result = subprocess.run(
            ['grep', '-r', '-H', '--include=*.log', 'ERROR', log_dir],
            capture_output=True,
            text=True,
            check=False  # grep returns non-zero if no matches
        )

        matches = result.stdout if result.stdout else result.stderr

        # Save to output file
        with open(output_file, 'w') as f:
            f.write(matches)

        print(f"Search results saved to {output_file}")

        # Count matches
        match_count = len([m for m in matches.split('\n') if m])
        return match_count

    except Exception as e:
        print(f"Error searching logs: {e}")
        with open(output_file, 'w') as f:
            f.write(f"Error: {e}")
        return 0


def main():
    """Main function to find ERROR lines in log files."""
    log_dir = '/var/log'
    output_file = '/home/devops/error_logs.txt'

    print("=== Recursive Keyword Finder (ERROR search) ===\n")

    print(f"Searching for 'ERROR' in all .log files under {log_dir}...")

    match_count = search_logs_for_errors(log_dir, output_file)

    print(f"\nMatches found: {match_count}")

    if os.path.exists(output_file):
        print(f"\nResults preview:")
        with open(output_file, 'r') as f:
            lines = f.readlines()
            for line in lines[:20]:  # Show first 20 lines
                print(f"  {line.rstrip()}")

        if len(lines) > 20:
            print(f"  ... and {len(lines) - 20} more lines")


if __name__ == '__main__':
    main()