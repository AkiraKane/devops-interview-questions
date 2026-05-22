#!/usr/bin/env python3
"""
Solution for: StorageClass and PVC Expansion

Company: Datadog | Difficulty: Medium

Scenario:
Create a StorageClass fast-sc with volume expansion enabled, a PVC expand-pvc
(initially 1Gi), and a pod in namespace storage.

Task:
Expand the PVC from 1Gi to 2Gi dynamically.

Solution Approach:
- Create StorageClass with allowVolumeExpansion: true
- Create PVC and pod
- Patch PVC to request 2Gi
"""

import subprocess
import json


STORAGE_CLASS = {
    "apiVersion": "storage.k8s.io/v1",
    "kind": "StorageClass",
    "metadata": {"name": "fast-sc"},
    "provisioner": "kubernetes.io/no-provisioner",
    "allowVolumeExpansion": True
}

PVC = {
    "apiVersion": "v1",
    "kind": "PersistentVolumeClaim",
    "metadata": {"name": "expand-pvc", "namespace": "storage"},
    "spec": {
        "accessModes": ["ReadWriteOnce"],
        "storageClassName": "fast-sc",
        "resources": {"requests": {"storage": "1Gi"}}
    }
}

POD = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {"name": "storage-pod", "namespace": "storage"},
    "spec": {
        "containers": [{
            "name": "app",
            "image": "nginx:latest",
            "volumeMounts": [{"name": "data", "mountPath": "/data"}]
        }],
        "volumes": [{
            "name": "data",
            "persistentVolumeClaim": {"claimName": "expand-pvc"}
        }]
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


def expand_pvc():
    patch = {"spec": {"resources": {"requests": {"storage": "2Gi"}}}}
    result = subprocess.run(
        ['kubectl', 'patch', 'pvc', 'expand-pvc', '-n', 'storage',
         '--type=strategic', '-p', json.dumps(patch)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Expanded: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")


def verify():
    result = subprocess.run(
        ['kubectl', 'get', 'sc', 'fast-sc',
         '-o', 'jsonpath={.allowVolumeExpansion}'],
        capture_output=True, text=True
    )
    print(f"\nStorageClass allowVolumeExpansion: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'pvc', 'expand-pvc', '-n', 'storage'],
        capture_output=True, text=True
    )
    print(f"PVC:\n{result.stdout}")


def main():
    print("=== StorageClass and PVC Expansion ===\n")

    subprocess.run(['kubectl', 'create', 'namespace', 'storage'],
                   capture_output=True, text=True)

    print("Step 1: Create StorageClass")
    apply_manifest(STORAGE_CLASS)

    print("\nStep 2: Create PVC (1Gi)")
    apply_manifest(PVC)

    print("\nStep 3: Create Pod")
    apply_manifest(POD)

    print("\nStep 4: Expand PVC to 2Gi")
    expand_pvc()

    print("\nStep 5: Verify")
    verify()


if __name__ == '__main__':
    main()
