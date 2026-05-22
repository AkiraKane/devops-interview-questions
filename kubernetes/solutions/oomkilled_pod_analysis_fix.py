#!/usr/bin/env python3
"""
Solution for: OOMKilled Pod Analysis and Fix

Company: Accenture | Difficulty: Medium

Scenario:
Inspect pod oom-demo in namespace apps, confirm it is being OOMKilled.

Task:
Recreate/update the pod with the memory limit raised from 20Mi to 100Mi
so it stabilizes in Running state.

Solution Approach:
- Inspect the pod to confirm OOMKilled termination reason
- Patch the pod (or delete and recreate) with higher memory limit
"""

import subprocess
import json


def inspect_pod():
    """Check pod status and termination reason."""
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'oom-demo', '-n', 'apps', '-o', 'yaml'],
        capture_output=True, text=True
    )

    if 'OOMKilled' in result.stdout:
        print("CONFIRMED: Pod is being OOMKilled")
        # Extract last state info
        for line in result.stdout.split('\n'):
            if 'reason' in line.lower() and 'oomkilled' in line.lower():
                print(f"  {line.strip()}")
        return True
    else:
        print("Pod is not in OOMKilled state")
        return False


def fix_pod():
    """
    Fix the pod by raising memory limit to 100Mi.

    Since pods are mostly immutable, we delete and recreate with the fix.
    """
    # Get existing pod spec
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'oom-demo', '-n', 'apps', '-o', 'json'],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        # Create a new pod manifest directly
        pod = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "oom-demo",
                "namespace": "apps"
            },
            "spec": {
                "containers": [
                    {
                        "name": "app",
                        "image": "nginx:latest",
                        "resources": {
                            "requests": {"memory": "64Mi"},
                            "limits": {"memory": "100Mi"}
                        }
                    }
                ]
            }
        }
    else:
        pod = json.loads(result.stdout)
        # Clean up metadata for re-creation
        for key in ['resourceVersion', 'uid', 'creationTimestamp',
                     'managedFields', 'status']:
            pod['metadata'].pop(key, None)
        if 'status' in pod:
            del pod['status']

        # Update memory limit to 100Mi
        for container in pod['spec']['containers']:
            if 'resources' not in container:
                container['resources'] = {}
            if 'limits' not in container['resources']:
                container['resources']['limits'] = {}
            container['resources']['limits']['memory'] = '100Mi'
            if 'requests' not in container['resources']:
                container['resources']['requests'] = {}
            container['resources']['requests']['memory'] = '64Mi'

    # Delete old pod
    subprocess.run(
        ['kubectl', 'delete', 'pod', 'oom-demo', '-n', 'apps'],
        capture_output=True, text=True
    )

    # Create fixed pod
    result = subprocess.run(
        ['kubectl', 'apply', '-f', '-'],
        input=json.dumps(pod),
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Recreated pod with 100Mi memory limit")
    else:
        print(f"Error: {result.stderr}")


def verify():
    """Verify the pod is running with the new memory limit."""
    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'oom-demo', '-n', 'apps',
         '-o', 'jsonpath={.status.phase}'],
        capture_output=True, text=True
    )
    print(f"Pod status: {result.stdout}")

    result = subprocess.run(
        ['kubectl', 'get', 'pod', 'oom-demo', '-n', 'apps',
         '-o', 'jsonpath={.spec.containers[0].resources.limits.memory}'],
        capture_output=True, text=True
    )
    print(f"Memory limit: {result.stdout}")


def main():
    print("=== OOMKilled Pod Analysis and Fix ===\n")

    print("Step 1: Inspect pod for OOMKilled")
    inspect_pod()

    print("\nStep 2: Fix memory limit (20Mi -> 100Mi)")
    fix_pod()

    print("\nStep 3: Verify pod is stable")
    verify()


if __name__ == '__main__':
    main()
