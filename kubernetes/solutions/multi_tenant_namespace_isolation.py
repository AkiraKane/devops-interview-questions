#!/usr/bin/env python3
"""
Solution for: Multi-Tenant Namespace Isolation

Company: Palantir | Difficulty: Medium

Scenario:
Set up network isolation for namespaces team-a and team-b.

Task:
Create default-deny NetworkPolicies, then allow team-a pods to reach team-b
pods labeled app=api on port 8080 only. Also create LimitRanges capping
CPU at 1 and memory at 512Mi per container in both namespaces.

Solution Approach:
- Create default-deny ingress/egress NetworkPolicies in both namespaces
- Create an allow policy in team-a for egress to team-b app=api:8080
- Create a corresponding ingress allow in team-b from team-a
- Create LimitRange in both namespaces
"""

import subprocess
import json


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


def create_namespaces():
    """Create the two tenant namespaces."""
    for ns in ['team-a', 'team-b']:
        subprocess.run(
            ['kubectl', 'create', 'namespace', ns],
            capture_output=True, text=True
        )
        print(f"Namespace {ns} ready")


def create_default_deny(ns):
    """Create default-deny NetworkPolicy for a namespace."""
    policy = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {
            "name": "default-deny-all",
            "namespace": ns
        },
        "spec": {
            "podSelector": {},
            "policyTypes": ["Ingress", "Egress"]
        }
    }
    return apply_manifest(policy)


def create_egress_allow():
    """Allow team-a pods to reach team-b app=api on port 8080."""
    policy = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {
            "name": "allow-egress-to-team-b-api",
            "namespace": "team-a"
        },
        "spec": {
            "podSelector": {},
            "policyTypes": ["Egress"],
            "egress": [
                {
                    "to": [
                        {
                            "namespaceSelector": {
                                "matchLabels": {
                                    "kubernetes.io/metadata.name": "team-b"
                                }
                            },
                            "podSelector": {
                                "matchLabels": {
                                    "app": "api"
                                }
                            }
                        }
                    ],
                    "ports": [
                        {
                            "protocol": "TCP",
                            "port": 8080
                        }
                    ]
                }
            ]
        }
    }
    return apply_manifest(policy)


def create_ingress_allow():
    """Allow team-b to receive traffic from team-a on port 8080."""
    policy = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {
            "name": "allow-ingress-from-team-a",
            "namespace": "team-b"
        },
        "spec": {
            "podSelector": {
                "matchLabels": {
                    "app": "api"
                }
            },
            "policyTypes": ["Ingress"],
            "ingress": [
                {
                    "from": [
                        {
                            "namespaceSelector": {
                                "matchLabels": {
                                    "kubernetes.io/metadata.name": "team-a"
                                }
                            }
                        }
                    ],
                    "ports": [
                        {
                            "protocol": "TCP",
                            "port": 8080
                        }
                    ]
                }
            ]
        }
    }
    return apply_manifest(policy)


def create_limit_range(ns):
    """Create a LimitRange capping CPU and memory per container."""
    limit_range = {
        "apiVersion": "v1",
        "kind": "LimitRange",
        "metadata": {
            "name": "container-limits",
            "namespace": ns
        },
        "spec": {
            "limits": [
                {
                    "type": "Container",
                    "default": {
                        "cpu": "1",
                        "memory": "512Mi"
                    },
                    "defaultRequest": {
                        "cpu": "100m",
                        "memory": "64Mi"
                    }
                }
            ]
        }
    }
    return apply_manifest(limit_range)


def verify():
    """Verify all resources are in place."""
    for ns in ['team-a', 'team-b']:
        print(f"\n--- {ns} ---")
        result = subprocess.run(
            ['kubectl', 'get', 'networkpolicy,limitrange', '-n', ns],
            capture_output=True, text=True
        )
        print(result.stdout)


def main():
    print("=== Multi-Tenant Namespace Isolation ===\n")

    print("Step 1: Create namespaces")
    create_namespaces()

    print("\nStep 2: Default-deny NetworkPolicies")
    create_default_deny('team-a')
    create_default_deny('team-b')

    print("\nStep 3: Allow team-a -> team-b api:8080")
    create_egress_allow()
    create_ingress_allow()

    print("\nStep 4: LimitRanges in both namespaces")
    create_limit_range('team-a')
    create_limit_range('team-b')

    print("\nStep 5: Verify")
    verify()


if __name__ == '__main__':
    main()
