#!/usr/bin/env python3
"""
Solution for: Multi-Key ConfigMap

Company: Snap | Difficulty: Easy

Scenario:
Create a ConfigMap settings with two keys (MODE=dev and VERSION=1.0).

Task:
Create a pod config-pod (busybox) that mounts the ConfigMap at /etc/config
so both keys appear as files.

Solution Approach:
- Create ConfigMap with two data keys
- Create pod mounting the ConfigMap as a volume
- Each key becomes a file at the mount path
"""

import subprocess
import json


CONFIGMAP = {
    "apiVersion": "v1",
    "kind": "ConfigMap",
    "metadata": {
        "name": "settings",
        "namespace": "default"
    },
    "data": {
        "MODE": "dev",
        "VERSION": "1.0"
    }
}

POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "config-pod",
        "namespace": "default"
    },
    "spec": {
        "containers": [
            {
                "name": "busybox",
                "image": "busybox",
                "command": ["sh", "-c", "cat /etc/config/MODE /etc/config/VERSION; sleep 3600"],
                "volumeMounts": [
                    {"name": "config", "mountPath": "/etc/config"}
                ]
            }
        ],
        "volumes": [
            {
                "name": "config",
                "configMap": {
                    "name": "settings"
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
    """Verify the ConfigMap keys appear as files in the pod."""
    result = subprocess.run(
        ['kubectl', 'exec', 'config-pod', '--', 'ls', '-la', '/etc/config/'],
        capture_output=True, text=True
    )
    print(f"\nFiles at /etc/config:\n{result.stdout}")

    result = subprocess.run(
        ['kubectl', 'exec', 'config-pod', '--', 'cat', '/etc/config/MODE'],
        capture_output=True, text=True
    )
    print(f"MODE = {result.stdout.strip()}")

    result = subprocess.run(
        ['kubectl', 'exec', 'config-pod', '--', 'cat', '/etc/config/VERSION'],
        capture_output=True, text=True
    )
    print(f"VERSION = {result.stdout.strip()}")


def main():
    print("=== Multi-Key ConfigMap ===\n")

    print("Step 1: Create ConfigMap with MODE and VERSION")
    apply_manifest(CONFIGMAP)

    print("\nStep 2: Create pod mounting ConfigMap")
    apply_manifest(POD)

    print("\nStep 3: Verify keys appear as files")
    verify()


if __name__ == '__main__':
    main()
