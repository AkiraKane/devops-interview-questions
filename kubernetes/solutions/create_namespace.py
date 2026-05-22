#!/usr/bin/env python3
"""
Solution for: Create Namespace

Company: Accenture | Difficulty: Easy

Scenario:
Create a single namespace named playground.

Task:
Create the namespace using kubectl.

Solution Approach:
- Use kubectl create namespace
"""

import subprocess


def create_namespace(name='playground'):
    """Create a Kubernetes namespace."""
    result = subprocess.run(
        ['kubectl', 'create', 'namespace', name],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Created: {result.stdout.strip()}")
    elif 'AlreadyExists' in result.stderr:
        print(f"Namespace '{name}' already exists")
    else:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def verify(name='playground'):
    """Verify the namespace exists."""
    result = subprocess.run(
        ['kubectl', 'get', 'namespace', name],
        capture_output=True, text=True
    )
    print(f"\n{result.stdout}")


def main():
    print("=== Create Namespace ===\n")
    create_namespace('playground')
    verify('playground')


if __name__ == '__main__':
    main()
