#!/usr/bin/env python3
"""
Solution for: Custom Resource Definition Setup

Company: ActivisionBlizzard | Difficulty: Medium

Scenario:
Create a CRD widgets.mycompany.io (group mycompany.io, kind Widget, short
name wd, namespaced scope, version v1 with served:true and storage:true).

Task:
Create the CRD, then create a CR instance sample-widget in namespace extensions
and verify it can be listed.

Solution Approach:
- Create the CRD with proper names and version config
- Create the CR instance
- Verify with kubectl get
"""

import subprocess
import json


CRD_MANIFEST = {
    "apiVersion": "apiextensions.k8s.io/v1",
    "kind": "CustomResourceDefinition",
    "metadata": {
        "name": "widgets.mycompany.io"
    },
    "spec": {
        "group": "mycompany.io",
        "names": {
            "kind": "Widget",
            "listKind": "WidgetList",
            "plural": "widgets",
            "singular": "widget",
            "shortNames": ["wd"]
        },
        "scope": "Namespaced",
        "versions": [
            {
                "name": "v1",
                "served": True,
                "storage": True,
                "schema": {
                    "openAPIV3Schema": {
                        "type": "object",
                        "properties": {
                            "spec": {
                                "type": "object",
                                "properties": {
                                    "size": {"type": "integer"}
                                }
                            }
                        }
                    }
                }
            }
        ]
    }
}

CR_INSTANCE = {
    "apiVersion": "mycompany.io/v1",
    "kind": "Widget",
    "metadata": {
        "name": "sample-widget",
        "namespace": "extensions"
    },
    "spec": {
        "size": 3
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
    """Verify the CRD and CR instance."""
    # Check CRD
    result = subprocess.run(
        ['kubectl', 'get', 'crd', 'widgets.mycompany.io'],
        capture_output=True, text=True
    )
    print(f"\nCRD:\n{result.stdout}")

    # Check CR instance
    result = subprocess.run(
        ['kubectl', 'get', 'widget', 'sample-widget', '-n', 'extensions'],
        capture_output=True, text=True
    )
    print(f"Widget:\n{result.stdout}")

    # List all widgets
    result = subprocess.run(
        ['kubectl', 'get', 'wd', '-n', 'extensions'],
        capture_output=True, text=True
    )
    print(f"Using short name 'wd':\n{result.stdout}")


def main():
    print("=== Custom Resource Definition Setup ===\n")

    # Create namespace if it doesn't exist
    subprocess.run(['kubectl', 'create', 'namespace', 'extensions'],
                   capture_output=True, text=True)

    print("Step 1: Create CRD")
    apply_manifest(CRD_MANIFEST)

    print("\nStep 2: Create CR instance")
    apply_manifest(CR_INSTANCE)

    print("\nStep 3: Verify")
    verify()


if __name__ == '__main__':
    main()
