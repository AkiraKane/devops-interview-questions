#!/usr/bin/env python3
"""
Docker Multi-Architecture Image Build
Company: Docker | Difficulty: Hard

Build a Docker image that supports multiple architectures (amd64, arm64)
using Docker buildx for cross-platform builds.
"""

from __future__ import annotations

import subprocess
import os


def setup_docker_buildx() -> None:
    """Enable Docker buildx for multi-architecture builds."""
    subprocess.run(["docker", "buildx", "install"], check=False)
    subprocess.run(["docker", "buildx", "create", "--name", "mybuilder"], check=False)
    subprocess.run(["docker", "buildx", "use", "mybuilder"], check=True)


def build_multiarch_image(
    image_name: str,
    dockerfile: str = "Dockerfile",
    platforms: list[str] = None
) -> None:
    """
    Build Docker image for multiple architectures.

    Args:
        image_name: Name and tag for the image (e.g., "myapp:multi")
        dockerfile: Path to Dockerfile
        platforms: List of target platforms (e.g., ["linux/amd64", "linux/arm64"])
    """
    if platforms is None:
        platforms = ["linux/amd64", "linux/arm64"]

    platforms_str = ",".join(platforms)

    cmd = [
        "docker", "buildx", "build",
        "--platform", platforms_str,
        "--tag", image_name,
        "--push",
        "-f", dockerfile, "."
    ]

    print(f"Building multi-architecture image: {image_name}")
    print(f"Platforms: {platforms_str}")
    print(f"Command: {' '.join(cmd)}")

    subprocess.run(cmd, check=True)


def main():
    print("Docker Multi-Architecture Image Build")
    print("=" * 39)

    print("\n1. Setup buildx:")
    print("   docker buildx create --name mybuilder")
    print("   docker buildx use mybuilder")
    print("   docker buildx inspect --bootstrap")

    print("\n2. Build for multiple architectures:")
    print("   docker buildx build \\")
    print("     --platform linux/amd64,linux/arm64 \\")
    print("     --tag myapp:multi \\")
    print("     --push \\")
    print("     -f Dockerfile .")

    # Example: Build nginx for amd64 and arm64
    print("\n3. Example - Build nginx for multiple platforms:")
    setup_docker_buildx()
    # build_multiarch_image("myapp:multi", platforms=["linux/amd64", "linux/arm64"])


if __name__ == "__main__":
    main()