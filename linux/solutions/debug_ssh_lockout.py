#!/usr/bin/env python3
"""
Solution for Debug SSH Lockout

Company: TCS
Difficulty: Medium

Scenario:
The developer account dev has been locked out of the server. Security logs indicate
the SSH daemon's authentication failure limit was triggered.

Task:
Check the logs to count exactly how many times the user failed `today`. Update the
SSH configuration to increase the allowed login attempts above that number.

Solution Approach:
- Parse /var/log/auth.log (or /var/log/secure) to count failed SSH attempts for user 'dev'
- Identify today's failed attempts
- Update SSH config to increase MaxAuthTries above the count
"""

import subprocess
import os
from datetime import datetime


def count_failed_auth_today(username='dev'):
    """
    Count failed authentication attempts for a user from today's logs.

    Args:
        username: The username to search for (default: 'dev')

    Returns:
        int: Number of failed attempts today
    """
    # Determine log file location (varies by distro)
    log_files = ['/var/log/auth.log', '/var/log/secure', '/var/log/auth.log.1']

    log_content = ''
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    log_content += f.read()
            except PermissionError:
                # Try using sudo
                try:
                    result = subprocess.run(
                        ['sudo', 'cat', log_file],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        log_content += result.stdout
                except:
                    pass

    if not log_content:
        print(f"Could not read any log files. Tried: {log_files}")
        return 0

    # Get today's date in various formats
    today = datetime.now().date()
    today_str = today.strftime('%b %d')  # e.g., "May 22"

    failed_count = 0

    for line in log_content.split('\n'):
        # Look for SSH failed password attempts for the user
        if 'sshd' in line and 'Failed password' in line and username in line:
            # Check if it's today
            if today_str in line:
                failed_count += 1

    return failed_count


def get_current_max_auth_tries():
    """Get the current MaxAuthTries value from SSH config."""
    config_files = ['/etc/ssh/sshd_config', '/etc/ssh/sshd_config.d/*.conf']

    try:
        for config_file in ['/etc/ssh/sshd_config']:
            if os.path.exists(config_file):
                result = subprocess.run(
                    ['grep', '-E', '^MaxAuthTries', config_file],
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    value = result.stdout.split()[1]
                    return int(value)
    except Exception as e:
        print(f"Error reading SSH config: {e}")

    # Default if not specified
    return 6


def update_ssh_max_auth_tries(new_value):
    """
    Update the MaxAuthTries setting in SSH config.

    This uses sed to update the value, or adds it if not present.
    """
    config_file = '/etc/ssh/sshd_config'

    # First check if MaxAuthTries exists
    try:
        result = subprocess.run(
            ['grep', '-E', '^MaxAuthTries', config_file],
            capture_output=True,
            text=True
        )

        if result.stdout:
            # Update existing value
            subprocess.run(
                ['sudo', 'sed', '-i', f's/^MaxAuthTries.*/MaxAuthTries {new_value}/', config_file],
                check=True
            )
        else:
            # Add new value at the end
            with open(config_file, 'a') as f:
                f.write(f'\nMaxAuthTries {new_value}\n')

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error updating SSH config: {e}")
        return False


def main():
    """Main function to debug SSH lockout and fix it."""
    username = 'dev'

    print(f"Analyzing failed SSH login attempts for user '{username}'...")

    failed_count = count_failed_auth_today(username)
    print(f"Failed authentication attempts today: {failed_count}")

    current_max = get_current_max_auth_tries()
    print(f"Current MaxAuthTries: {current_max}")

    # Set new value above failed count
    new_max = max(failed_count + 1, current_max + 1)

    # Ensure it's at least a reasonable minimum
    new_max = max(new_max, 10)

    print(f"\nUpdating MaxAuthTries to {new_max} (above {failed_count} failures)...")

    if update_ssh_max_auth_tries(new_max):
        print(f"Successfully updated MaxAuthTries to {new_max}")

        # Reload SSH configuration
        print("Reloading SSH configuration...")
        subprocess.run(['sudo', 'systemctl', 'reload', 'sshd'], check=False)
    else:
        print("Could not update SSH config automatically (may need sudo)")

    print(f"\nNote: User '{username}' should now be able to log in.")
    print(f"MaxAuthTries is now set to {new_max}, which is above the {failed_count} failed attempts.")


if __name__ == '__main__':
    main()