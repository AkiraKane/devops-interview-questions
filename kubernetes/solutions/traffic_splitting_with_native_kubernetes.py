#!/usr/bin/env python3
"""
Solution for: Traffic Splitting with Native Kubernetes

Company: Palantir | Difficulty: Medium

Scenario:
Implement canary traffic splitting in namespace canary.

Task:
2/3 of traffic goes to app-v1 and 1/3 goes to app-v2 (nginx:1.25) using
only native Kubernetes resources (weighted replica counts).

Solution Approach:
- Create app-v1 Deployment with 2 replicas
- Create app-v2 Deployment with 1 replica
- Create a single Service selecting both via a shared label
- Traffic is distributed across pods, so 2:1 replicas = 2/3:1/3 split
"""

import subprocess
import json


APP_V1 = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "app-v1", "namespace": "canary"},
    "spec": {
        "replicas": 2,
        "selector": {"matchLabels": {"app": "myapp", "version": "v1"}},
        "template": {
            "metadata": {"labels": {"app": "myapp", "version": "v1"}},
            "spec": {
                "containers": [{
                    "name": "nginx",
                    "image": "nginx:1.24",
                    "ports": [{"containerPort": 80}]
                }]
            }
        }
    }
}

APP_V2 = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "app-v2", "namespace": "canary"},
    "spec": {
        "replicas": 1,
        "selector": {"matchLabels": {"app": "myapp", "version": "v2"}},
        "template": {
            "metadata": {"labels": {"app": "myapp", "version": "v2"}},
            "spec": {
                "containers": [{
                    "name": "nginx",
                    "image": "nginx:1.25",
                    "ports": [{"containerPort": 80}]
                }]
            }
        }
    }
}

SERVICE = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {"name": "app-svc", "namespace": "canary"},
    "spec": {
        "selector": {"app": "myapp"},
        "ports": [{"port": 80, "targetPort": 80}]
    }
}


def apply_manifest(manifest):
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
    result = subprocess.run(
        ['kubectl', 'get', 'pods', '-n', 'canary', '-l', 'app=myapp',
         '-o', 'custom-columns=NAME:.metadata.name,VERSION:.metadata.labels.version,IP:.status.podIP'],
        capture_output=True, text=True
    )
    print(f"\nPods:\n{result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'endpoints', 'app-svc', '-n', 'canary'],
        capture_output=True, text=True
    )
    print(f"Service endpoints:\n{result.stdout}")

    print("Traffic distribution: 2 pods v1 (2/3) + 1 pod v2 (1/3)")


def main():
    print("=== Traffic Splitting with Native Kubernetes ===\n")

    subprocess.run(['kubectl', 'create', 'namespace', 'canary'],
                   capture_output=True, text=True)

    print("Step 1: Create app-v1 (2 replicas)")
    apply_manifest(APP_V1)

    print("\nStep 2: Create app-v2 (1 replica)")
    apply_manifest(APP_V2)

    print("\nStep 3: Create Service (selects both via app=myapp)")
    apply_manifest(SERVICE)

    print("\nStep 4: Verify")
    verify()

    print("\nKey: Native canary uses replica count ratio (2:1) for traffic splitting")


if __name__ == '__main__':
    main()
