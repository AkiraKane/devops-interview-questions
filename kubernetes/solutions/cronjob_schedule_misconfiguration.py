#!/usr/bin/env python3
"""
Solution for: CronJob Schedule Misconfiguration

Company: RedHat | Difficulty: Medium

Scenario:
Fix a CronJob named cleanup in namespace ops.

Task:
Change schedule to * * * * *, set timezone to Etc/UTC, and limit successful
job history retention to the most recent run only.

Solution Approach:
- Patch the CronJob schedule, timezone, and successfulJobsHistoryLimit
"""

import subprocess
import json


def fix_cronjob():
    """Patch the cleanup CronJob with correct settings."""
    patch = {
        "spec": {
            "schedule": "* * * * *",
            "timeZone": "Etc/UTC",
            "successfulJobsHistoryLimit": 1
        }
    }

    result = subprocess.run(
        ['kubectl', 'patch', 'cronjob', 'cleanup', '-n', 'ops',
         '--type=strategic', '-p', json.dumps(patch)],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"Patched: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify():
    """Verify the CronJob settings."""
    result = subprocess.run(
        ['kubectl', 'get', 'cronjob', 'cleanup', '-n', 'ops', '-o', 'yaml'],
        capture_output=True, text=True
    )

    for line in result.stdout.split('\n'):
        line = line.strip()
        if any(key in line for key in ['schedule:', 'timeZone:', 'successfulJobsHistoryLimit:']):
            print(f"  {line}")


def main():
    print("=== CronJob Schedule Misconfiguration Fix ===\n")

    print("Step 1: Patch CronJob")
    fix_cronjob()

    print("\nStep 2: Verify settings")
    verify()


if __name__ == '__main__':
    main()
