#!/usr/bin/env python3
"""
Solution for: Pod Viewer Access

Company: Reddit | Difficulty: Easy

Scenario:
Create RBAC resources for read-only pod access.

Task:
Create ServiceAccount reader-sa, Role pod-reader (get/list/watch on pods),
and RoleBinding pod-reader-binding in namespace demo.

Solution Approach:
- Create ServiceAccount
- Create Role with pod read permissions
- Create RoleBinding to tie them together
"""

import subprocess
import json


SERVICEACCOUNT = {
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "name": "reader-sa",
        "namespace": "demo"
    }
}

ROLE = {
    "apiVersion": "rbac.authorization.k8s.io/v1",
    "kind": "Role",
    "metadata": {
        "name": "pod-reader",
        "namespace": "demo"
    },
    "rules": [
        {
            "apiGroups": [""],
            "resources": ["pods"],
            "verbs": ["get", "list", "watch"]
        }
    ]
}

ROLE_BINDING = {
    "apiVersion": "rbac.authorization.k8s.io/v1",
    "kind": "RoleBinding",
    "metadata": {
        "name": "pod-reader-binding",
        "namespace": "demo"
    },
    "subjects": [
        {
            "kind": "ServiceAccount",
            "name": "reader-sa",
            "namespace": "demo"
        }
    ],
    "roleRef": {
        "kind": "Role",
        "name": "pod-reader",
        "apiGroup": "rbac.authorization.k8s.io"
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
    """Verify RBAC is correctly configured."""
    result = subprocess.run(
        ['kubectl', 'auth', 'can-i', 'list', 'pods',
         '-n', 'demo', '--as=system:serviceaccount:demo:reader-sa'],
        capture_output=True, text=True
    )
    print(f"\nCan list pods: {result.stdout.strip()}")

    result = subprocess.run(
        ['kubectl', 'auth', 'can-i', 'delete', 'pods',
         '-n', 'demo', '--as=system:serviceaccount:demo:reader-sa'],
        capture_output=True, text=True
    )
    print(f"Can delete pods: {result.stdout.strip()}")


def main():
    print("=== Pod Viewer Access ===\n")

    subprocess.run(['kubectl', 'create', 'namespace', 'demo'],
                   capture_output=True, text=True)

    print("Step 1: Create ServiceAccount")
    apply_manifest(SERVICEACCOUNT)

    print("\nStep 2: Create Role (get/list/watch pods)")
    apply_manifest(ROLE)

    print("\nStep 3: Create RoleBinding")
    apply_manifest(ROLE_BINDING)

    print("\nStep 4: Verify")
    verify()


if __name__ == '__main__':
    main()
