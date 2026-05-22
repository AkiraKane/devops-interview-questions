#!/usr/bin/env python3
"""
Solution for Automated Archive and Retention

Company: Microsoft
Difficulty: Hard

Scenario:
Configuration files in `/etc` are at risk of being lost due to accidental changes
or deletions, and there's currently no automated backup process in place.

Task:
Write a shell script at `/usr/local/bin/backup_etc.sh` that accepts a target backup
path (where files will be saved at) as a command-line argument, creates a compressed
archive of `/etc` with the naming format `etc-backup-YYYY-MM-DD.tar.gz`, automatically
removes backups older than 7 days, and exits with an error if no path is provided.
Make the script executable and create a cron job to run it daily at 02:00 AM,
storing backups in `/backups/etc/` using crontab command.

Solution Approach:
- Create the backup script that handles archiving and cleanup
- Set up cron job for daily execution at 02:00 AM
"""

import subprocess
import os
from datetime import datetime


def create_backup_script():
    """Create the backup script at /usr/local/bin/backup_etc.sh"""
    script_content = '''#!/bin/bash
#
# backup_etc.sh - Automated /etc backup script
# Created for Automated Archive and Retention interview question
#

# Check if backup path is provided
if [ -z "$1" ]; then
    echo "Error: Backup directory path required"
    echo "Usage: $0 <backup_directory>"
    exit 1
fi

BACKUP_DIR="$1"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate backup filename with timestamp
TIMESTAMP=$(date +%Y-%m-%d)
BACKUP_FILE="${BACKUP_DIR}/etc-backup-${TIMESTAMP}.tar.gz"

# Create compressed archive of /etc
echo "Creating backup of /etc to $BACKUP_FILE"
tar -czf "$BACKUP_FILE" /etc 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Backup created successfully: $BACKUP_FILE"
else
    echo "Error: Failed to create backup"
    exit 1
fi

# Remove backups older than 7 days
echo "Removing backups older than 7 days..."
find "$BACKUP_DIR" -name "etc-backup-*.tar.gz" -mtime +7 -delete

echo "Backup and cleanup complete"
exit 0
'''

    script_path = '/usr/local/bin/backup_etc.sh'

    with open(script_path, 'w') as f:
        f.write(script_content)

    # Make executable
    os.chmod(script_path, 0o755)

    print(f"Backup script created at {script_path}")
    return script_path


def create_cron_job():
    """Create cron job to run backup script daily at 02:00 AM."""
    cron_entry = "0 2 * * * /usr/local/bin/backup_etc.sh /backups/etc/"

    # Get current crontab
    result = subprocess.run(
        ['crontab', '-l'],
        capture_output=True,
        text=True
    )

    current_cron = result.stdout if result.returncode == 0 else ""

    # Check if our cron entry already exists
    if 'backup_etc.sh' in current_cron:
        print("Cron job already exists for backup_etc.sh")
        return

    # Add new cron entry
    new_cron = current_cron.strip() + '\n' + cron_entry + '\n'

    process = subprocess.Popen(
        ['crontab', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=new_cron)

    if process.returncode == 0:
        print(f"Cron job added: {cron_entry}")
    else:
        print(f"Error adding cron job: {stderr}")


def run_backup(backup_dir):
    """Execute the backup script with the given directory."""
    script_path = '/usr/local/bin/backup_etc.sh'

    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return False

    try:
        result = subprocess.run(
            [script_path, backup_dir],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e.stderr}")
        return False


def main():
    """Main function to set up and execute the backup solution."""
    # Ensure backups directory exists
    backup_dir = '/backups/etc/'
    os.makedirs(backup_dir, exist_ok=True)

    # Create the backup script
    create_backup_script()

    # Create cron job
    create_cron_job()

    # Run the backup
    print(f"\nExecuting backup to {backup_dir}...")
    run_backup(backup_dir)

    # List backup files
    print(f"\nBackup files in {backup_dir}:")
    if os.path.exists(backup_dir):
        for f in sorted(os.listdir(backup_dir)):
            filepath = os.path.join(backup_dir, f)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                print(f"  {f} ({size} bytes)")


if __name__ == '__main__':
    main()