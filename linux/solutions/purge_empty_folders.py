#!/usr/bin/env python3
"""
Solution for Purge Empty Folders

Company: CrowdStrike
Difficulty: Easy

Scenario:
The `/tmp` directory has accumulated numerous leftover folders from previous
application runs and temporary scripts. Many of these directories are now empty
and can be safely removed.

Task:
Find all empty directories under /tmp recursively and delete them without
affecting directories that contain files or subdirectories.

Solution Approach:
- Use `find /tmp -type d -empty` to find empty directories
- Use `rmdir` or `rm -rf` (with empty check) to remove them
- The find command with -empty flag identifies truly empty directories
"""

import subprocess
import os


def find_empty_directories(path='/tmp'):
    """
    Find all empty directories under a path.

    Returns:
        list: List of empty directory paths
    """
    try:
        result = subprocess.run(
            ['find', path, '-type', 'd', '-empty'],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            return result.stdout.strip().split('\n')
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error finding empty directories: {e.stderr}")
        return []


def remove_empty_directory(dir_path):
    """Remove an empty directory."""
    try:
        # Use rmdir which only removes empty directories (safer)
        subprocess.run(['rmdir', dir_path], check=True)
        return True
    except subprocess.CalledProcessError:
        # Fallback to rmdir with sudo
        try:
            subprocess.run(['sudo', 'rmdir', dir_path], check=True)
            return True
        except:
            return False


def main():
    """Main function to purge empty folders."""
    print("=== Purge Empty Folders ===\n")

    print("Searching for empty directories under /tmp...")

    empty_dirs = find_empty_directories('/tmp')

    if not empty_dirs:
        print("No empty directories found")
        return

    print(f"Found {len(empty_dirs)} empty directory(s):")
    for d in empty_dirs:
        print(f"  {d}")

    print(f"\nRemoving {len(empty_dirs)} empty directory(s)...")

    removed = 0
    failed = []

    for dir_path in empty_dirs:
        if remove_empty_directory(dir_path):
            print(f"  Removed: {dir_path}")
            removed += 1
        else:
            failed.append(dir_path)

    print(f"\nRemoved {removed} empty directories")

    if failed:
        print(f"Could not remove {len(failed)} directory(s):")
        for d in failed:
            print(f"  {d}")

    # Verify
    print("\n=== Verification ===")
    remaining = find_empty_directories('/tmp')

    if remaining:
        print(f"{len(remaining)} empty directory(s) remain:")
        for d in remaining:
            print(f"  {d}")
    else:
        print("No empty directories remaining in /tmp")


if __name__ == '__main__':
    main()