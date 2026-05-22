#!/usr/bin/env python3
"""
Docker Network Configuration Fix
Company: Twitter | Difficulty: Medium

Fix Docker networking issues by investigating container connectivity,
DNS resolution, and network mode configuration.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Literal


NetworkMode = Literal["bridge", "host", "none", "overlay", "container"]


@dataclass
class NetworkInfo:
    """Container network information."""
    name: str
    driver: str
    subnet: str | None
    gateway: str | None


def inspect_container_networking(container: str) -> dict:
    """Get detailed network info for a container."""
    result = subprocess.run(
        ["docker", "inspect", container, "--format", "{{json .NetworkSettings}}"],
        capture_output=True,
        text=True,
        check=True
    )
    return {"raw": result.stdout}


def list_networks() -> list[NetworkInfo]:
    """List all Docker networks."""
    result = subprocess.run(
        ["docker", "network", "ls", "--format", "{{.Name}}"],
        capture_output=True,
        text=True,
        check=True
    )
    return [NetworkInfo(name=name, driver="", subnet=None, gateway=None)
            for name in result.stdout.strip().split("\n")]


def create_bridge_network(name: str, subnet: str) -> None:
    """Create a custom bridge network."""
    subprocess.run(
        ["docker", "network", "create", "--driver", "bridge", "--subnet", subnet, name],
        check=True
    )


def connect_container_to_network(container: str, network: str) -> None:
    """Connect a container to a specific network."""
    subprocess.run(["docker", "network", "connect", network, container], check=True)


def run_container_in_network(
    image: str,
    container_name: str,
    network: str,
    ports: list[str] | None = None
) -> None:
    """Run a container in a specific network."""
    cmd = ["docker", "run", "--network", network, "--name", container_name, image]
    if ports:
        for p in ports:
            cmd.extend(["-p", p])
    subprocess.run(cmd, check=True)


def troubleshoot_connectivity(container: str) -> None:
    """Troubleshoot container connectivity issues."""
    print(f"\nTroubleshooting container: {container}")

    # Check if container is running
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    if container not in result.stdout:
        print(f"  ERROR: Container '{container}' is not running")
        return

    # Inspect networking
    print("  Inspecting network settings...")
    subprocess.run(["docker", "inspect", container, "--format", "{{.NetworkSettings.Networks}}"])

    # Test DNS resolution
    print("  Testing DNS resolution...")
    subprocess.run(["docker", "exec", container, "nslookup", "google.com"], check=False)

    # Ping test
    print("  Testing connectivity...")
    subprocess.run(["docker", "exec", container, "ping", "-c", "2", "8.8.8.8"], check=False)


def main():
    print("Docker Network Configuration Fix")
    print("=" * 34)

    print("\n1. List Docker networks:")
    print("   docker network ls")

    print("\n2. Inspect a container's network:")
    print("   docker inspect <container> --format '{{json .NetworkSettings.Networks}}'")

    print("\n3. Create custom bridge network:")
    print("   docker network create --driver bridge --subnet 172.20.0.0/16 mynetwork")

    print("\n4. Connect container to network:")
    print("   docker network connect mynetwork <container>")

    print("\n5. Run container in specific network:")
    print("   docker run --network mynetwork -p 8080:80 --name web nginx")


if __name__ == "__main__":
    main()