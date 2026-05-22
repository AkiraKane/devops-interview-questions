#!/usr/bin/env python3
"""
Solution for: Implement StatefulSet with Stable DNS

Company: Okta | Difficulty: Medium

Scenario:
Create a Headless Service named dns-app and a StatefulSet with 3 replicas
(image nginx:alpine) in namespace dev.

Task:
Ensure each pod gets a stable DNS name like dns-app-0.dns-app.

Solution Approach:
- Create a Headless Service (clusterIP: None) named dns-app
- Create a StatefulSet with serviceName: dns-app and 3 replicas
- K8s automatically creates DNS entries: <pod-name>.<service-name>
"""

import subprocess
import json


HEADLESS_SERVICE = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": "dns-app",
        "namespace": "dev"
    },
    "spec": {
        "clusterIP": "None",
        "selector": {
            "app": "dns-app"
        },
        "ports": [
            {"port": 80, "targetPort": 80}
        ]
    }
}

STATEFULSET = {
    "apiVersion": "apps/v1",
    "kind": "StatefulSet",
    "metadata": {
        "name": "dns-app",
        "namespace": "dev"
    },
    "spec": {
        "serviceName": "dns-app",
        "replicas": 3,
        "selector": {
            "matchLabels": {
                "app": "dns-app"
            }
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "dns-app"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:alpine",
                        "ports": [
                            {"containerPort": 80}
                        ]
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
    """Verify StatefulSet pods have stable DNS names."""
    # Check pods
    result = subprocess.run(
        ['kubectl', 'get', 'pods', '-n', 'dev', '-l', 'app=dns-app',
         '-o', 'custom-columns=NAME:.metadata.name,IP:.status.podIP'],
        capture_output=True, text=True
    )
    print(f"\nPods:\n{result.stdout}")

    # Check headless service endpoints
    result = subprocess.run(
        ['kubectl', 'get', 'endpoints', 'dns-app', '-n', 'dev'],
        capture_output=True, text=True
    )
    print(f"Endpoints:\n{result.stdout}")

    # DNS lookup from a pod
    result = subprocess.run(
        ['kubectl', 'run', 'dns-check', '-n', 'dev', '--image=busybox',
         '--rm', '-i', '--restart=Never',
         '--command', '--', 'nslookup', 'dns-app-0.dns-app'],
        capture_output=True, text=True
    )
    print(f"DNS lookup for dns-app-0.dns-app:\n{result.stdout}")


def main():
    print("=== StatefulSet with Stable DNS ===\n")

    subprocess.run(['kubectl', 'create', 'namespace', 'dev'],
                   capture_output=True, text=True)

    print("Step 1: Create Headless Service")
    apply_manifest(HEADLESS_SERVICE)

    print("\nStep 2: Create StatefulSet")
    apply_manifest(STATEFULSET)

    print("\nStep 3: Verify stable DNS names")
    verify()

    print("\nKey: StatefulSet pods get DNS: <pod-name>.<service-name>.<ns>.svc.cluster.local")


if __name__ == '__main__':
    main()
