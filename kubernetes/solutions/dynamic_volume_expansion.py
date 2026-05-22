#!/usr/bin/env python3
"""
Solution for: Dynamic Volume Expansion

Company: EPAM | Difficulty: Easy

Scenario:
Create a StorageClass (expandable-sc), PVC (data-pvc starting at 1Gi),
and pod in namespace storage, then expand the PVC to 5Gi without restarting.

Task:
Enable volume expansion on the StorageClass and expand the PVC dynamically.

Solution Approach:
- Create StorageClass with allowVolumeExpansion: true
- Create PVC and pod
- Patch PVC to request larger size
"""

import subprocess
import json


STORAGE_CLASS = {
    "apiVersion": "storage.k8s.io/v1",
    "kind": "StorageClass",
    "metadata": {
        "name": "expandable-sc"
    },
    "provisioner": "kubernetes.io/no-provisioner",
    "allowVolumeExpansion": True
}

PVC_MANIFEST = {
    "apiVersion": "v1",
    "kind": "PersistentVolumeClaim",
    "metadata": {
        "name": "data-pvc",
        "namespace": "storage"
    },
    "spec": {
        "accessModes": ["ReadWriteOnce"],
        "storageClassName": "expandable-sc",
        "resources": {
            "requests": {
                "storage": "1Gi"
            }
        }
    }
}

POD_MANIFEST = {
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "data-pod",
        "namespace": "storage"
    },
    "spec": {
        "containers": [
            {
                "name": "app",
                "image": "nginx:latest",
                "volumeMounts": [
                    {"name": "data", "mountPath": "/data"}
                ]
            }
        ],
        "volumes": [
            {
                "name": "data",
                "persistentVolumeClaim": {
                    "claimName": "data-pvc"
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


def expand_pvc(new_size='5Gi'):
    """Expand the PVC to the new size."""
    patch = {
        "spec": {
            "resources": {
                "requests": {
                    "storage": new_size
                }
            }
        }
    }

    result = subprocess.run(
        ['kubectl', 'patch', 'pvc', 'data-pvc', '-n', 'storage',
         '--type=strategic', '-p', json.dumps(patch)],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"Expanded PVC: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")


def verify():
    """Verify PVC size and pod status."""
    result = subprocess.run(
        ['kubectl', 'get', 'pvc', 'data-pvc', '-n', 'storage'],
        capture_output=True, text=True
    )
    print(f"\nPVC status:\n{result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'data-pod', '-n', 'storage'],
        capture_output=True, text=True
    )
    print(f"Pod status:\n{result.stdout}")


def main():
    print("=== Dynamic Volume Expansion ===\n")

    subprocess.run(['kubectl', 'create', 'namespace', 'storage'],
                   capture_output=True, text=True)

    print("Step 1: Create StorageClass with allowVolumeExpansion")
    apply_manifest(STORAGE_CLASS)

    print("\nStep 2: Create PVC (1Gi)")
    apply_manifest(PVC_MANIFEST)

    print("\nStep 3: Create Pod")
    apply_manifest(POD_MANIFEST)

    print("\nStep 4: Expand PVC to 5Gi")
    expand_pvc('5Gi')

    print("\nStep 5: Verify")
    verify()


if __name__ == '__main__':
    main()
