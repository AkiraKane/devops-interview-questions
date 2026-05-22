#!/usr/bin/env python3
"""
Solution for: Fix Job with ServiceAccount and RBAC Permission Issues

Company: SAP | Difficulty: Medium

Scenario:
A Job data-loader in namespace ops fails with permission denied when calling
the Kubernetes API.

Task:
Create a ServiceAccount with RBAC Role and RoleBinding granting get/list on
pods, and update the Job to use that ServiceAccount.

Solution Approach:
- Create ServiceAccount data-loader-sa
- Create Role with get/list on pods
- Create RoleBinding
- Patch the Job to use the ServiceAccount
"""

import subprocess
import json


SERVICEACCOUNT = {
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "name": "data-loader-sa",
        "namespace": "ops"
    }
}

ROLE = {
    "apiVersion": "rbac.authorization.k8s.io/v1",
    "kind": "Role",
    "metadata": {
        "name": "data-loader-role",
        "namespace": "ops"
    },
    "rules": [
        {
            "apiGroups": [""],
            "resources": ["pods"],
            "verbs": ["get", "list"]
        }
    ]
}

ROLE_BINDING = {
    "apiVersion": "rbac.authorization.k8s.io/v1",
    "kind": "RoleBinding",
    "metadata": {
        "name": "data-loader-binding",
        "namespace": "ops"
    },
    "subjects": [
        {
            "kind": "ServiceAccount",
            "name": "data-loader-sa",
            "namespace": "ops"
        }
    ],
    "roleRef": {
        "kind": "Role",
        "name": "data-loader-role",
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


def patch_job():
    """Patch the data-loader Job to use the ServiceAccount."""
    # Delete existing job first (jobs are mostly immutable)
    subprocess.run(
        ['kubectl', 'delete', 'job', 'data-loader', '-n', 'ops'],
        capture_output=True, text=True
    )

    # Get existing job and modify serviceAccountName
    result = subprocess.run(
        ['kubectl', 'get', 'job', 'data-loader', '-n', 'ops', '-o', 'json'],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        job = json.loads(result.stdout)
        job['spec']['template']['spec']['serviceAccountName'] = 'data-loader-sa'
        # Remove resourceVersion etc for clean apply
        for key in ['resourceVersion', 'uid', 'creationTimestamp']:
            job['metadata'].pop(key, None)

        apply_manifest(job)
    else:
        # Create a simple job if original doesn't exist
        job = {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": "data-loader",
                "namespace": "ops"
            },
            "spec": {
                "template": {
                    "spec": {
                        "serviceAccountName": "data-loader-sa",
                        "containers": [
                            {
                                "name": "loader",
                                "image": "bitnami/kubectl:latest",
                                "command": ["kubectl", "get", "pods"]
                            }
                        ],
                        "restartPolicy": "Never"
                    }
                },
                "backoffLimit": 1
            }
        }
        apply_manifest(job)


def verify():
    """Verify the Job uses the correct ServiceAccount."""
    result = subprocess.run(
        ['kubectl', 'get', 'job', 'data-loader', '-n', 'ops',
         '-o', 'jsonpath={.spec.template.spec.serviceAccountName}'],
        capture_output=True, text=True
    )
    print(f"\nJob ServiceAccount: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'sa,role,rolebinding', '-n', 'ops'],
        capture_output=True, text=True
    )
    print(f"RBAC resources:\n{result.stdout}")


def main():
    print("=== Fix Job with ServiceAccount and RBAC ===\n")

    print("Step 1: Create ServiceAccount")
    apply_manifest(SERVICEACCOUNT)

    print("\nStep 2: Create Role (get/list pods)")
    apply_manifest(ROLE)

    print("\nStep 3: Create RoleBinding")
    apply_manifest(ROLE_BINDING)

    print("\nStep 4: Patch Job to use ServiceAccount")
    patch_job()

    print("\nStep 5: Verify")
    verify()


if __name__ == '__main__':
    main()
