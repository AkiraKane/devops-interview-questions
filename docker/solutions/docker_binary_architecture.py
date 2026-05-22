#!/usr/bin/env python3
"""
Docker Binary Architecture
Company: Uber | Difficulty: Medium

Identify whether the docker binary is a standalone binary or a client-server
architecture by using `docker version` and `docker info` commands.
"""

from __future__ import annotations

import subprocess
import re


def check_docker_architecture() -> dict:
    """
    Check Docker architecture type by examining docker version output.

    Returns dict with server info if Docker daemon is running.
    """
    result = subprocess.run(
        ["docker", "version", "--format", "{{json .}}"],
        capture_output=True,
        text=True
    )

    info = {}
    if result.returncode == 0:
        # Docker has server/client architecture (daemon running)
        info["type"] = "client_server"
        info["has_daemon"] = True
    else:
        # Docker is standalone binary
        info["type"] = "standalone"
        info["has_daemon"] = False

    return info


def get_docker_info() -> str:
    """Get detailed Docker daemon information."""
    result = subprocess.run(
        ["docker", "info", "--format", "{{json .}}"],
        capture_output=True,
        text=True
    )
    return result.stdout if result.returncode == 0 else ""


def main():
    print("Docker Binary Architecture Check")
    print("=" * 36)

    print("\n1. Check if Docker is client-server or standalone:")
    print("   docker version")

    result = subprocess.run(["docker", "version"], capture_output=True, text=True)
    has_server = "Server:" in result.stdout or "Engine:" in result.stdout

    if has_server:
        print("\n=> Docker uses CLIENT-SERVER architecture")
        print("   - docker CLI is the client")
        print("   - dockerd is the server/daemon")
    else:
        print("\n=> Docker is a STANDALONE binary")

    print("\n2. Get Docker daemon info:")
    print("   docker info")

    info = get_docker_info()
    print(f"\nDaemon running: {has_server}")


if __name__ == "__main__":
    main()