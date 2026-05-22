#!/usr/bin/env python3
"""
Solution for: Upload-Safe File Partitioning

Company: GoDaddy | Difficulty: Medium

Scenario:
Application files in /tmp/app/ exceed the 1 MB upload limit.

Task:
Find all files larger than 1 MB, split each into 1 MB chunks (with .part_aa,
.part_ab naming pattern) in the same directory, keep the originals intact,
and verify the chunks were created.

Solution Approach:
- Use `find` to locate files larger than 1M
- Use `split` to create 1M chunks with a naming prefix
- Verify chunks exist and are within size limits
"""

import subprocess
import os


def find_large_files(directory='/tmp/app', size_mb=1):
    """Find files larger than the given size in MB."""
    result = subprocess.run(
        ['find', directory, '-type', 'f', '-size', f'+{size_mb}M'],
        capture_output=True, text=True
    )
    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    return files


def split_file(filepath, chunk_size='1m'):
    """
    Split a file into 1 MB chunks.

    Uses `split` with numeric suffixes for .part_aa, .part_ab pattern.
    Chunks are placed in the same directory as the original.
    """
    directory = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    prefix = os.path.join(directory, f'{basename}.part_')

    result = subprocess.run(
        ['split', '-b', chunk_size, '--numeric-suffixes', '--suffix-length=2',
         filepath, prefix],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"  Error splitting {filepath}: {result.stderr}")
        return []

    # List created chunks
    chunks = sorted([
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.startswith(f'{basename}.part_')
    ])

    return chunks


def verify_chunks(chunks, max_bytes=1048576):
    """Verify all chunks are within the size limit."""
    all_valid = True
    for chunk in chunks:
        size = os.path.getsize(chunk)
        status = "OK" if size <= max_bytes else "OVER LIMIT"
        if status != "OK":
            all_valid = False
        print(f"    {os.path.basename(chunk)}: {size} bytes [{status}]")
    return all_valid


def main():
    app_dir = '/tmp/app'
    output = '/home/devops/upload_partition_report.txt'

    print("=== Upload-Safe File Partitioning ===\n")

    # Create test directory if needed
    if not os.path.exists(app_dir):
        print(f"Creating {app_dir} with sample files...")
        os.makedirs(app_dir, exist_ok=True)
        # Create files of various sizes
        for name, size_mb in [('small.txt', 0.5), ('large1.dat', 2), ('large2.dat', 3)]:
            path = os.path.join(app_dir, name)
            with open(path, 'wb') as f:
                f.write(b'x' * int(size_mb * 1024 * 1024))

    print(f"Finding files larger than 1 MB in {app_dir}...")
    large_files = find_large_files(app_dir)

    if not large_files:
        print("No files larger than 1 MB found")
        return

    print(f"Found {len(large_files)} large file(s):\n")

    report_lines = ["=== Upload-Safe File Partitioning Report ===\n"]

    for filepath in large_files:
        size = os.path.getsize(filepath)
        size_mb = size / (1024 * 1024)
        print(f"  {filepath} ({size_mb:.1f} MB)")

        print(f"  Splitting into 1 MB chunks...")
        chunks = split_file(filepath)

        if chunks:
            print(f"  Created {len(chunks)} chunks:")
            verify_chunks(chunks)

            report_lines.append(f"\nOriginal: {filepath} ({size_mb:.1f} MB)")
            report_lines.append(f"Chunks ({len(chunks)}):")
            for c in chunks:
                report_lines.append(f"  {os.path.basename(c)}: {os.path.getsize(c)} bytes")

    # Save report
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.write('\n'.join(report_lines))
    print(f"\nReport saved to {output}")


if __name__ == '__main__':
    main()
