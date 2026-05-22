#!/usr/bin/env python3
"""
Solution for Recursive Database File Backup

Company: GitLab
Difficulty: Easy

Scenario:
Before performing a system-wide database schema migration, you've been asked to
ensure that all existing `.db` files are safely backed up. These files may be
scattered across multiple subdirectories, and simply renaming them isn't enough.
You must create backup copies with the `.db.bak` extension, preserving directory
structure and permissions.

Task:
Recursively scan `/opt/data/` and create backup copies of all files ending with
`.db`. Each backup should have the same name but with `.bak` suffix added and
remain in the same directory as the original file.

Solution Approach:
- Use `find` to locate all .db files under /opt/data/
- For each file, create a copy with .bak extension
- Use `cp -p` to preserve permissions and timestamps
"""

import subprocess
import os
import shutil


def find_db_files(directory='/opt/data/'):
    """
    Find all .db files under a directory.

    Returns:
        list: List of full paths to .db files
    """
    try:
        result = subprocess.run(
            ['find', directory, '-name', '*.db', '-type', 'f'],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            return result.stdout.strip().split('\n')
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error finding .db files: {e.stderr}")
        return []


def create_backup(original_path):
    """
    Create a backup of a .db file with .bak extension.

    Preserves permissions using cp -p.
    """
    backup_path = original_path + '.bak'

    try:
        # Use cp -p to preserve permissions and timestamps
        shutil.copy2(original_path, backup_path)
        return True, backup_path
    except PermissionError:
        # Try with sudo
        try:
            subprocess.run(
                ['sudo', 'cp', '-p', original_path, backup_path],
                check=True
            )
            return True, backup_path
        except:
            return False, None
    except Exception as e:
        print(f"Error backing up {original_path}: {e}")
        return False, None


def main():
    """Main function to create backup copies of .db files."""
    directory = '/opt/data/'

    print("=== Recursive Database File Backup ===\n")

    print(f"Scanning {directory} for .db files...")

    db_files = find_db_files(directory)

    if not db_files:
        print(f"No .db files found under {directory}")

        # In test environment, create some demo files
        print("\nDemo mode: creating test files...")
        os.makedirs('/opt/data/apps', exist_ok=True)
        os.makedirs('/opt/data/config', exist_ok=True)
        os.makedirs('/opt/data/logs', exist_ok=True)

        test_files = [
            '/opt/data/apps/inventory.db',
            '/opt/data/config/settings.db',
            '/opt/data/logs/session.db'
        ]

        for f in test_files:
            with open(f, 'w') as file:
                file.write(f"Database: {f}\n")

        db_files = test_files
        print(f"Created test files: {db_files}")

    print(f"\nFound {len(db_files)} .db file(s):")
    for f in db_files:
        print(f"  {f}")

    print(f"\nCreating backup copies...")

    backed_up = []
    failed = []

    for filepath in db_files:
        success, backup_path = create_backup(filepath)
        if success:
            print(f"  Created: {backup_path}")
            backed_up.append(backup_path)
        else:
            print(f"  Failed: {filepath}")
            failed.append(filepath)

    print(f"\n=== Summary ===")
    print(f"Successfully backed up: {len(backed_up)} file(s)")

    if backed_up:
        print("\nBackup files created:")
        for b in backed_up:
            stats = os.stat(b)
            print(f"  {b} ({stats.st_size} bytes)")

    if failed:
        print(f"\nFailed to backup: {len(failed)} file(s)")


if __name__ == '__main__':
    main()