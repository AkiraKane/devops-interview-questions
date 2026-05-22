#!/usr/bin/env python3
"""
Docker Volume Cross-Platform Consistency
Company: Google | Difficulty: Hard

Handle volume mounting differences between Linux and macOS/Windows
when using Docker Desktop, ensuring consistent behavior across platforms.
"""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path


def get_docker_host_path(path: str, platform_sys: str = None) -> str:
    """
    Get the correct host path for volume mounting based on OS.

    On macOS with Docker Desktop, paths need translation:
    /Users/foo -> /hostUsers/foo (with gRPC FUSE)
    """
    if platform_sys is None:
        platform_sys = platform.system()

    # Docker Desktop on macOS remaps paths
    if platform_sys == "Darwin":
        path = path.replace("/Users/", "/hostUsers/")
    elif platform_sys == "Windows":
        path = path.replace("\\", "/")

    return path


def run_container_with_volume(
    image: str,
    container_name: str,
    host_path: str,
    container_path: str,
    read_only: bool = False
) -> None:
    """
    Run container with volume mount that works across platforms.

    Args:
        image: Docker image to run
        container_name: Name for the container
        host_path: Path on host to mount
        container_path: Path inside container
        read_only: Make volume read-only
    """
    host_path = get_docker_host_path(host_path)
    read_only_flag = ":ro" if read_only else ":rw"

    cmd = [
        "docker", "run",
        "-v", f"{host_path}:{container_path}{read_only_flag}",
        "--name", container_name,
        image
    ]

    subprocess.run(cmd, check=True)


def create_named_volume(dockerfile_dir: str) -> None:
    """
    Create a Docker named volume for persistent storage.

    Named volumes work consistently across all platforms.
    """
    volume_name = Path(dockerfile_dir).name + "_data"

    print(f"Creating named volume: {volume_name}")
    subprocess.run(["docker", "volume", "create", volume_name], check=True)

    return volume_name


def main():
    print("Docker Volume Cross-Platform Consistency")
    print("=" * 42)

    current_os = platform.system()
    print(f"\nDetected OS: {current_os}")

    print("\n1. For named volumes (recommended for cross-platform):")
    print("   docker volume create mydata")
    print("   docker run -v mydata:/data --name app image")

    print("\n2. For bind mounts with path translation (macOS):")
    host_path = "/Users/user/project"
    translated = get_docker_host_path(host_path)
    print(f"   Host path: {host_path}")
    print(f"   Docker Desktop path: {translated}")
    print("   docker run -v {translated}:/app image")

    print("\n3. Verify volume mount works:")
    print("   docker inspect <container> --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{end}}'")


if __name__ == "__main__":
    main()