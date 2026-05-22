#!/usr/bin/env python3
"""
Solution for: ImagePullBackOff Secrets

Company: Datadog | Difficulty: Medium

Scenario:
A Deployment backend in namespace dev is stuck in ImagePullBackOff.

Task:
Create an image pull Secret with ghcr.io credentials and reference it in the
Deployment's imagePullSecrets.

Solution Approach:
- Create docker-registry secret with ghcr.io credentials
- Patch the Deployment to add imagePullSecrets
"""

import subprocess
import json


def create_image_pull_secret(username, password):
    """Create a docker-registry secret for ghcr.io."""
    result = subprocess.run(
        ['kubectl', 'create', 'secret', 'docker-registry', 'ghcr-pull-secret',
         '-n', 'dev',
         '--docker-server=ghcr.io',
         f'--docker-username={username}',
         f'--docker-password={password}'],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"Created: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def patch_deployment():
    """Patch the backend Deployment to use the image pull secret."""
    patch = {
        "spec": {
            "template": {
                "spec": {
                    "imagePullSecrets": [
                        {"name": "ghcr-pull-secret"}
                    ]
                }
            }
        }
    }

    result = subprocess.run(
        ['kubectl', 'patch', 'deployment', 'backend', '-n', 'dev',
         '--type=strategic', '-p', json.dumps(patch)],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"Patched: {result.stdout.strip()}")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify():
    """Verify the deployment is pulling images correctly."""
    result = subprocess.run(
        ['kubectl', 'get', 'deployment', 'backend', '-n', 'dev',
         '-o', 'jsonpath={.spec.template.spec.imagePullSecrets[*].name}'],
        capture_output=True, text=True
    )
    print(f"ImagePullSecrets: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'pods', '-n', 'dev', '-l', 'app=backend'],
        capture_output=True, text=True
    )
    print(f"Pod status:\n{result.stdout}")


def main():
    print("=== ImagePullBackOff Secrets Fix ===\n")

    print("Step 1: Create image pull secret")
    create_image_pull_secret('user', 'token')

    print("\nStep 2: Patch Deployment with imagePullSecrets")
    patch_deployment()

    print("\nStep 3: Verify")
    verify()


if __name__ == '__main__':
    main()
