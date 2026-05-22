#!/usr/bin/env python3
"""
Solution for Handling Large Log Archives

Company: Amazon
Difficulty: Easy

Scenario:
During an incident investigation, you pulled a massive log export from
`/var/log/app/access.log` that's several gigabytes in size. Your analysis tools
and editors can't handle the entire file at once.

Task:
Split the log file into smaller chunks of 100 lines each, with sequential naming,
save to /tmp/log_parts/, and keep original file intact.

Solution Approach:
- Create the output directory /tmp/log_parts/
- Use `split` command to split by lines (100 lines per file)
- Use sequential naming with 'access_part_' prefix
"""

import subprocess
import os


def split_log_file(input_file, output_dir, lines_per_file=100, prefix='access_part_'):
    """
    Split a log file into smaller chunks.

    Args:
        input_file: Path to the large log file
        output_dir: Directory for output files
        lines_per_file: Number of lines per output file
        prefix: Prefix for output filenames

    Returns:
        bool: True if successful
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Warning: {input_file} does not exist. This is expected in test environment.")
        print("The solution would use: split -l 100 /var/log/app/access.log /tmp/log_parts/access_part_")
        return False

    # Split command: split -l <lines> <input> <output_prefix>
    # This creates files named access_part_aa, access_part_ab, etc.
    try:
        result = subprocess.run(
            ['split', '-l', str(lines_per_file), input_file, os.path.join(output_dir, prefix)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Successfully split {input_file}")
        print(f"Output directory: {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error splitting file: {e.stderr}")
        return False


def verify_split_files(output_dir, prefix):
    """Verify the split files were created correctly."""
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist")
        return

    files = sorted([f for f in os.listdir(output_dir) if f.startswith(prefix)])

    if not files:
        print("No split files found")
        return

    print(f"\nSplit files created ({len(files)} files):")
    total_lines = 0

    for f in files:
        filepath = os.path.join(output_dir, f)
        with open(filepath, 'r') as file:
            line_count = sum(1 for _ in file)
        total_lines += line_count
        print(f"  {f}: {line_count} lines")

    print(f"\nTotal: {total_lines} lines across {len(files)} files")

    # Verify original is intact
    original = '/var/log/app/access.log'
    if os.path.exists(original):
        with open(original, 'r') as f:
            original_lines = sum(1 for _ in f)
        print(f"\nOriginal file intact: {original} ({original_lines} lines)")


def main():
    """Main function to split large log file."""
    input_file = '/var/log/app/access.log'
    output_dir = '/tmp/log_parts/'
    lines_per_file = 100
    prefix = 'access_part_'

    print("=== Handling Large Log Archives ===\n")
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Lines per chunk: {lines_per_file}\n")

    success = split_log_file(input_file, output_dir, lines_per_file, prefix)

    if success:
        verify_split_files(output_dir, prefix)
    else:
        print("\nNote: In a real environment with the actual log file, this would:")
        print(f"  1. Create directory: {output_dir}")
        print(f"  2. Split the file with: split -l {lines_per_file} {input_file} {output_dir}{prefix}")
        print(f"  3. This creates sequential files: {prefix}aa, {prefix}ab, {prefix}ac, etc.")


if __name__ == '__main__':
    main()