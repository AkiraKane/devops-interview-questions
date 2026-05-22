#!/usr/bin/env python3
"""
Solution for: ConfigMap Reload with Sidecar

Company: Yelp | Difficulty: Medium

Scenario:
Create a ConfigMap (app-config) with key settings.conf and a pod with two
containers (main nginx:1.24 and a busybox sidecar called config-watcher) that
both mount the ConfigMap at /etc/config.

Task:
Create a ConfigMap and a pod with a sidecar that watches for config changes
without restarting the pod.

Solution Approach:
- Create ConfigMap app-config with settings.conf key
- Create a pod with main nginx container and busybox sidecar
- Both mount the ConfigMap at /etc/config
"""

import subprocess
import json
import os


CONFIGMAP_MANIFEST = {
    "apiVersion": "v1",
    "kind": "ConfigMap",
    "metadata": {
        "name": "app-config",
        "namespace": "default"
    },
    "data": {
        "settings.conf": "server_name=localhost\nmax_connections=100\n"
    }
}

POD_MANIFEST = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "config-sidecar",
        "namespace": "default"
    },
    "spec": {
        "containers": [
            {
                "name": "app",
                "image": "nginx:1.24",
                "volumeMounts": [
                    {"name": "config-volume", "mountPath": "/etc/config"}
                ]
            },
            {
                "name": "config-watcher",
                "image": "busybox",
                "command": ["sh", "-c", "while true; do cat /etc/config/settings.conf; sleep 30; done"],
                "volumeMounts": [
                    {"name": "config-volume", "mountPath": "/etc/config"}
                ]
            }
        ],
        "volumes": [
            {
                "name": "config-volume",
                "configMap": {
                    "name": "app-config"
                }
            }
        ]
    }
}


def apply_manifest(manifest):
    """Apply a Kubernetes manifest using kubectl."""
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(manifest),
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"Applied: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify():
    """Verify the ConfigMap and pod are running."""
    # Check ConfigMap
    result = subprocess.run(
        ['kubectl', 'get', 'configmap', 'app-config', '-o', 'jsonpath={.data}'],
        capture_output=True, text=True
    )
    print(f"\nConfigMap data: {result.stdout}")

    # Check pod containers
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'config-sidecar',
         '-o', 'jsonpath={.spec.containers[*].name}'],
        capture_output=True, text=True
    )
    print(f"Pod containers: {result.stdout}")

    # Check volume mounts
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'config-sidecar',
         '-o', 'jsonpath={.spec.containers[*].volumeMounts[*].mountPath}'],
        capture_output=True, text=True
    )
    print(f"Volume mounts: {result.stdout}")


def main():
    print("=== ConfigMap Reload with Sidecar ===\n")

    print("Step 1: Create ConfigMap")
    apply_manifest(CONFIGMAP_MANIFEST)

    print("\nStep 2: Create Pod with sidecar")
    apply_manifest(POD_MANIFEST)

    print("\nStep 3: Verify")
    verify()


if __name__ == '__main__':
    main()
