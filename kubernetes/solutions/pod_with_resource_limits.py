#!/usr/bin/env python3
"""
Solution for: Pod with Resource Limits

Company: PWC | Difficulty: Easy

Scenario:
Create a pod resource-pod using nginx:latest with resource constraints.

Task:
Set CPU request 100m / limit 200m and memory request 64Mi / limit 128Mi.

Solution Approach:
- Create pod with resources.requests and resources.limits
"""

import subprocess
import json


POD_MANIFEST = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "resource-pod"
    },
    "spec": {
        "containers": [
            {
                "name": "nginx",
                "image": "nginx:latest",
                "resources": {
                    "requests": {
                        "cpu": "100m",
                        "memory": "64Mi"
                    },
                    "limits": {
                        "cpu": "200m",
                        "memory": "128Mi"
                    }
                }
            }
        ]
    }
}


def apply_manifest(manifest):
    """Apply a Kubernetes manifest."""
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(manifest),
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Applied: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify():
    """Verify pod resource configuration."""
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'resource-pod',
         '-o', 'jsonpath={.spec.containers[0].resources}'],
        capture_output=True, text=True
    )
    print(f"Resources: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'describe', 'pod', 'resource-pod'],
        capture_output=True, text=True
    )
    # Extract resource lines
    for line in result.stdout.split('\n'):
        if 'cpu' in line.lower() or 'memory' in line.lower():
            print(f"  {line.strip()}")


def main():
    print("=== Pod with Resource Limits ===\n")

    print("Creating pod with CPU and memory limits...")
    apply_manifest(POD_MANIFEST)

    print("\nVerifying...")
    verify()


if __name__ == '__main__':
    main()
