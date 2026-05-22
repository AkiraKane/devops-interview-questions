#!/usr/bin/env python3
"""
Solution for: Pod with Readiness Probe

Company: Zscaler | Difficulty: Easy

Scenario:
Create a pod web-ready using nginx:latest with an HTTP GET readiness probe.

Task:
Configure an HTTP readiness probe on port 80 at path / so the pod only
receives traffic once ready.

Solution Approach:
- Create pod with readinessProbe using httpGet
- Port 80, path /
"""

import subprocess
import json


POD_MANIFEST = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "web-ready",
        "labels": {
            "app": "web-ready"
        }
    },
    "spec": {
        "containers": [
            {
                "name": "nginx",
                "image": "nginx:latest",
                "ports": [
                    {"containerPort": 80}
                ],
                "readinessProbe": {
                    "httpGet": {
                        "path": "/",
                        "port": 80
                    },
                    "initialDelaySeconds": 5,
                    "periodSeconds": 10
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
    """Verify pod is ready."""
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'web-ready',
         '-o', 'jsonpath={.status.conditions[?(@.type=="Ready")].status}'],
        capture_output=True, text=True
    )
    print(f"Ready condition: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'web-ready'],
        capture_output=True, text=True
    )
    print(result.stdout)


def main():
    print("=== Pod with Readiness Probe ===\n")

    print("Creating pod with HTTP readiness probe...")
    apply_manifest(POD_MANIFEST)

    print("\nVerifying...")
    verify()


if __name__ == '__main__':
    main()
