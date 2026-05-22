#!/usr/bin/env python3
"""
Container CPU Limit Configuration
Company: IBM | Difficulty: Easy

Limit CPU usage to 500m (0.5 CPU cores) to prevent container from using
excessive CPU and impacting other services on the host.
"""

from __future__ import annotations

import subprocess


def update_container_cpu_limit(container_name: str, cpu_limit: str = "500m") -> None:
    """
    Update an existing container's CPU limit using docker update.

    Args:
        container_name: Name of the container to update
        cpu_limit: CPU limit in millicores (e.g., "500m" = 0.5 CPU)
    """
    subprocess.run(
        ["docker", "update", "--cpu-period", "100000", "--cpu-quota", "50000", container_name],
        check=True
    )


def run_container_with_cpu_limit(
    image: str,
    container_name: str,
    cpu_limit: str = "500m"
) -> None:
    """
    Run a container with CPU limit using docker run with --cpus flag.

    Args:
        image: Docker image to run
        container_name: Name for the container
        cpu_limit: CPU limit (e.g., "0.5" for 500m)
    """
    cpu_value = str(int(cpu_limit.rstrip('m')) / 1000)
    subprocess.run(
        ["docker", "run", "--cpus=" + cpu_value, "--name", container_name, image],
        check=True
    )


def main():
    print("Container CPU Limit Configuration")
    print("=" * 36)

    # Solution 1: Update existing container
    print("\n1. Update running container 'cpu_test' to 500m CPU limit:")
    print("   docker update --cpu-period 100000 --cpu-quota 50000 cpu_test")
    update_container_cpu_limit("cpu_test", "500m")

    # Solution 2: Run new container with CPU limit
    print("\n2. Run new container with CPU limit:")
    print("   docker run --cpus=0.5 --name cpu_test myapp:cpu")
    # run_container_with_cpu_limit("myapp:cpu", "cpu_test", "500m")

    print("\nVerification:")
    print("   docker stats cpu_test")
    print("   # Should show < 60% CPU usage")


if __name__ == "__main__":
    main()