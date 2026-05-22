#!/usr/bin/env python3
"""
Solution for: Update AWS Configs

Company: Stripe | Difficulty: Medium

Scenario:
Multiple environment config files under /etc/app/envs/ are set to single-AZ mode.

Task:
Find all .conf files, update multi_az from false to true and change
availability_zone to include two zones (us-east-1a,us-east-1b), doing
in-place edits while preserving all other values.

Solution Approach:
- Use `find` or `glob` to locate all .conf files under /etc/app/envs/
- Use `sed` for in-place substitution
- Preserve all other config values
"""

import subprocess
import os
import glob


def find_conf_files(directory='/etc/app/envs'):
    """Find all .conf files in the directory."""
    pattern = os.path.join(directory, '*.conf')
    files = glob.glob(pattern)
    print(f"Found {len(files)} .conf files in {directory}:")
    for f in files:
        print(f"  {f}")
    return files


def update_config_file(filepath):
    """
    Update a single config file:
    - multi_az = false  ->  multi_az = true
    - availability_zone = <anything>  ->  availability_zone = us-east-1a,us-east-1b
    """
    # Use sed for in-place editing, preserving all other values
    changes = []

    # Update multi_az
    result = subprocess.run(
        ['sed', '-i', 's/^multi_az\\s*=.*/multi_az = true/', filepath],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        changes.append('multi_az = true')
    else:
        # Try alternative pattern
        result = subprocess.run(
            ['sed', '-i', 's/multi_az=false/multi_az=true/', filepath],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            changes.append('multi_az = true')

    # Update availability_zone
    result = subprocess.run(
        ['sed', '-i',
         's/^availability_zone\\s*=.*/availability_zone = us-east-1a,us-east-1b/',
         filepath],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        changes.append('availability_zone = us-east-1a,us-east-1b')

    return changes


def verify_updates(filepath):
    """Verify the config file was updated correctly."""
    result = subprocess.run(
        ['grep', '-E', '(multi_az|availability_zone)', filepath],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def main():
    config_dir = '/etc/app/envs'

    print("=== Update AWS Configs ===\n")

    # Create test directory if it doesn't exist
    if not os.path.exists(config_dir):
        print(f"Creating {config_dir} for demonstration...")
        os.makedirs(config_dir, exist_ok=True)
        # Create sample config files
        for env in ['dev', 'staging', 'prod']:
            path = os.path.join(config_dir, f'{env}.conf')
            with open(path, 'w') as f:
                f.write(f"# {env} environment config\n")
                f.write(f"region = us-east-1\n")
                f.write(f"multi_az = false\n")
                f.write(f"availability_zone = us-east-1a\n")
                f.write(f"instance_type = t3.medium\n")

    files = find_conf_files(config_dir)

    if not files:
        print("No .conf files found")
        return

    print(f"\n=== Updating {len(files)} config files ===\n")
    for filepath in files:
        print(f"Updating {filepath}:")
        changes = update_config_file(filepath)
        for change in changes:
            print(f"  {change}")

        print("  Verification:")
        verification = verify_updates(filepath)
        for line in verification.split('\n'):
            print(f"    {line}")
        print()


if __name__ == '__main__':
    main()
