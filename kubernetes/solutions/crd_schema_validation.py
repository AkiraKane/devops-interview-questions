#!/usr/bin/env python3
"""
Solution for: CRD Schema Validation

Company: RedHat | Difficulty: Hard

Scenario:
Modify the existing widgets.mycompany.io CRD to add a schema that requires
spec.size as an integer with minimum value 1.

Task:
Add OpenAPI v3 schema validation to the CRD, then verify that creating a
bad-widget resource (missing the size field) is rejected.

Solution Approach:
- Patch the CRD to add a structural OpenAPI schema
- Require spec.size as integer with minimum 1
- Test that invalid resources are rejected
"""

import subprocess
import json


CRD_PATCH = {
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
                                "required": ["size"],
                                "properties": {
                                    "size": {
                                        "type": "integer",
                                        "minimum": 1
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ]
    }
}

BAD_WIDGET = {
    "apiVersion": "mycompany.io/v1",
    "kind": "Widget",
    "metadata": {
        "name": "bad-widget",
        "namespace": "default"
    },
    "spec": {}
}


def apply_crd():
    """Apply the CRD with schema validation."""
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(CRD_PATCH),
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"CRD applied: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def test_bad_widget():
    """Attempt to create a bad widget and verify it's rejected."""
    print("\nAttempting to create bad-widget (missing spec.size)...")
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(BAD_WIDGET),
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"EXPECTED: Request rejected by API server")
        print(f"Error: {result.stderr.strip()}")
        return True
    else:
        print("UNEXPECTED: Bad widget was accepted (schema may not be enforced yet)")
        return False


def verify():
    """Verify the CRD has schema validation."""
    result = subprocess.run(
        ['kubectl', 'get', 'crd', 'widgets.mycompany.io',
         '-o', 'jsonpath={.spec.versions[*].schema.openAPIV3Schema.spec.required}'],
        capture_output=True, text=True
    )
    print(f"\nCRD schema required fields: {result.stdout}")


def main():
    print("=== CRD Schema Validation ===\n")

    print("Step 1: Patch CRD with OpenAPI schema validation")
    apply_crd()

    print("\nStep 2: Verify CRD has schema")
    verify()

    print("\nStep 3: Test invalid resource rejection")
    test_bad_widget()


if __name__ == '__main__':
    main()
