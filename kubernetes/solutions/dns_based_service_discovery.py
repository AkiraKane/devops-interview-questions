#!/usr/bin/env python3
"""
Solution for: DNS-Based Service Discovery

Company: Netflix | Difficulty: Medium

Scenario:
Fix the service discovery-svc in namespace disco so that DNS resolution returns
individual pod IPs instead of a single service ClusterIP.

Task:
Convert the service to headless by setting clusterIP: None.

Solution Approach:
- Patch the service to set clusterIP: None
- This makes DNS return individual pod A records instead of a single service IP
"""

import subprocess
import json


def fix_service():
    """Patch the service to be headless."""
    patch = {
        "spec": {
            "clusterIP": "None"
        }
    }

    result = subprocess.run(
        ['kubectl', 'patch', 'service', 'discovery-svc', '-n', 'disco',
         '--type=strategic', '-p', json.dumps(patch)],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"Patched: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify():
    """Verify the service is now headless."""
    # Check service type
    result = subprocess.run(
        ['kubectl', 'get', 'service', 'discovery-svc', '-n', 'disco',
         '-o', 'jsonpath={.spec.clusterIP}'],
        capture_output=True, text=True
    )
    print(f"ClusterIP: {result.stdout}")

    # Get endpoints
    result = subprocess.run(
        ['kubectl', 'get', 'endpoints', 'discovery-svc', '-n', 'disco'],
        capture_output=True, text=True
    )
    print(f"Endpoints:\n{result.stdout}")

    # DNS lookup from a pod
    result = subprocess.run(
        ['kubectl', 'run', 'dns-test', '-n', 'disco', '--image=busybox',
         '--rm', '-i', '--restart=Never',
         '--command', '--', 'nslookup', 'discovery-svc'],
        capture_output=True, text=True
    )
    print(f"DNS resolution:\n{result.stdout}")


def main():
    print("=== DNS-Based Service Discovery Fix ===\n")

    print("Step 1: Patch service to headless (clusterIP: None)")
    fix_service()

    print("\nStep 2: Verify")
    verify()

    print("\nKey: Headless services return individual pod IPs for DNS queries,")
    print("enabling clients to discover all backing pods directly.")


if __name__ == '__main__':
    main()
