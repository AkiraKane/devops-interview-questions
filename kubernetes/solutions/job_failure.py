#!/usr/bin/env python3
"""
Solution for: Job Failure

Company: RedHat | Difficulty: Easy

Scenario:
Fix a failing Job fail-job in namespace batch.

Task:
Change the command to 'echo Success; exit 0' and ensure backoffLimit is 1.

Solution Approach:
- Delete the existing failing job
- Apply a corrected manifest with the fixed command
"""

import subprocess
import json


FIXED_JOB = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": "fail-job",
        "namespace": "batch"
    },
    "spec": {
        "backoffLimit": 1,
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "fail-job",
                        "image": "busybox",
                        "command": ["sh", "-c", "echo 'Success'; exit 0"]
                    }
                ],
                "restartPolicy": "Never"
            }
        }
    }
}


def fix_job():
    """Delete and recreate the job with the correct command."""
    # Delete existing job
    result = subprocess.run(
        ['kubectl', 'delete', 'job', 'fail-job', '-n', 'batch'],
        capture_output=True, text=True
    )
    print(f"Deleted old job: {result.stdout.strip()}")

    # Apply fixed job
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(FIXED_JOB),
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Applied: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify():
    """Verify the job completes successfully."""
    # Wait for job to complete
    result = subprocess.run(
        ['kubectl', 'wait', '--for=condition=complete', 'job/fail-job',
         '-n', 'batch', '--timeout=60s'],
        capture_output=True, text=True
    )
    print(f"Job wait: {result.stdout.strip()}")

    # Check job status
    result = subprocess.run(
        ['kubectl', 'get', 'job', 'fail-job', '-n', 'batch',
         '-o', 'jsonpath={.status.conditions[*].type}'],
        capture_output=True, text=True
    )
    print(f"Job status: {result.stdout}")

    # Check pod logs
    result = subprocess.run(
        ['kubectl', 'logs', '-n', 'batch', '-l', 'job-name=fail-job'],
        capture_output=True, text=True
    )
    print(f"Pod logs: {result.stdout.strip()}")


def main():
    print("=== Job Failure Fix ===\n")

    print("Step 1: Fix job command and backoffLimit")
    fix_job()

    print("\nStep 2: Verify job completes")
    verify()


if __name__ == '__main__':
    main()
