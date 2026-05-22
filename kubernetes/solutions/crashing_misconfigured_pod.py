#!/usr/bin/env python3
"""
Solution for: Crashing Misconfigured Pod

Company: Reddit | Difficulty: Medium

Scenario:
A deployment webapp in namespace prod is in CrashLoopBackOff. The container
image already has a config directory, so the fix must inject ConfigMap data
without overwriting that existing directory.

Task:
Fix by mounting individual ConfigMap keys as files rather than replacing the
whole directory.

Solution Approach:
- Create a ConfigMap with the needed config keys
- Use items in volumeMount to mount specific keys as individual files
- This avoids replacing the existing /etc/config directory contents
"""

import subprocess
import json


CONFIGMAP_MANIFEST = {
    "apiVersion": "v1",
    "kind": "ConfigMap",
    "metadata": {
        "name": "webapp-config",
        "namespace": "prod"
    },
    "data": {
        "app.conf": "debug=false\nlog_level=info\n"
    }
}

PATCHED_DEPLOYMENT = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "webapp",
        "namespace": "prod"
    },
    "spec": {
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "webapp",
                        "image": "nginx:latest",
                        "volumeMounts": [
                            {
                                "name": "config-volume",
                                "mountPath": "/etc/config/app.conf",
                                "subPath": "app.conf"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "config-volume",
                        "configMap": {
                            "name": "webapp-config"
                        }
                    }
                ]
            }
        }
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
    """Verify the deployment is running without crashes."""
    result = subprocess.run(
        ['kubectl', 'get', 'deployment', 'webapp', '-n', 'prod',
         '-o', 'jsonpath={.status.readyReplicas}'],
        capture_output=True, text=True
    )
    print(f"Ready replicas: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'pods', '-n', 'prod', '-l', 'app=webapp'],
        capture_output=True, text=True
    )
    print(f"Pod status:\n{result.stdout}")


def main():
    print("=== Crashing Misconfigured Pod Fix ===\n")

    print("Step 1: Create ConfigMap with app config")
    apply_manifest(CONFIGMAP_MANIFEST)

    print("\nStep 2: Patch deployment to mount individual key (subPath)")
    apply_manifest(PATCHED_DEPLOYMENT)

    print("\nStep 3: Verify pods are running")
    verify()

    print("\nKey fix: Using subPath mounts individual files without replacing the directory")


if __name__ == '__main__':
    main()
