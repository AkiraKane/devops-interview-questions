#!/usr/bin/env python3
"""
Memory Limit and OOM Killer Handling
Company: Netflix | Difficulty: Medium

Set memory limits on containers and understand how the OOM Killer
terminates containers that exceed their memory allocation.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class MemoryLimit:
    """Memory limit configuration for a container."""
    soft_limit: str | None = None
    hard_limit: str | None = None
    swap_limit: str | None = None


def run_container_with_memory_limit(
    image: str,
    container_name: str,
    memory_limit: str,
    memory_swap_limit: str | None = None
) -> None:
    """
    Run container with memory limits.

    Args:
        image: Docker image
        container_name: Name for container
        memory_limit: Max memory (e.g., "512m" for 512MB)
        memory_swap_limit: Max swap (optional)
    """
    cmd = [
        "docker", "run",
        "--memory", memory_limit,
        "--name", container_name,
    ]

    if memory_swap_limit:
        cmd.extend(["--memory-swap", memory_swap_limit])

    cmd.append(image)

    print(f"Running with --memory={memory_limit}")
    subprocess.run(cmd, check=True)


def update_container_memory_limit(container_name: str, memory_limit: str) -> None:
    """Update memory limit for running container."""
    subprocess.run(
        ["docker", "update", "--memory", memory_limit, container_name],
        check=True
    )


def check_oom_killer_status(container_name: str) -> None:
    """Check if container was killed by OOM Killer."""
    result = subprocess.run(
        ["docker", "inspect", container_name, "--format", "{{.State.OOMKilled}}"],
        capture_output=True,
        text=True
    )
    oom_killed = result.stdout.strip().lower() == "true"
    print(f"Container OOM Killed: {oom_killed}")


def diagnose_memory_issues(container_name: str) -> None:
    """Diagnose container memory issues."""
    print(f"\nDiagnosing memory issues for {container_name}")

    # Memory stats
    subprocess.run([
        "docker", "stats", "--no-stream",
        "--format", "table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.PIDs}}",
        container_name
    ])

    # Check OOM status
    check_oom_killer_status(container_name)


def main():
    print("Memory Limit and OOM Killer Handling")
    print("=" * 38)

    print("\n1. Run container with 512MB memory limit:")
    print("   docker run --memory=512m --name web myapp:latest")

    print("\n2. Run with memory and swap limit (memory-swap = 2x memory):")
    print("   docker run --memory=512m --memory-swap=1g --name web myapp:latest")

    print("\n3. Update memory limit for running container:")
    print("   docker update --memory=1g web")

    print("\n4. Check if container was OOM killed:")
    print("   docker inspect --format '{{.State.OOMKilled}}' web")


if __name__ == "__main__":
    main()