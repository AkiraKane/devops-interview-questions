#!/usr/bin/env python3
"""
Storage Driver Performance: fuse-overlayfs
Company: Red Hat | Difficulty: Medium

Configure Docker to use fuse-overlayfs storage driver for better
performance on rootless containers and check current storage driver.
"""

from __future__ import annotations

import subprocess
import os


def get_current_storage_driver() -> str:
    """Get the current Docker storage driver."""
    result = subprocess.run(
        ["docker", "info", "--format", "{{.Driver}}"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def configure_daemon_for_overlay2() -> None:
    """Configure Docker daemon to use overlay2 storage driver."""
    config = {
        "storage-driver": "overlay2"
    }
    print("Add to /etc/docker/daemon.json:")
    print('{"storage-driver": "overlay2"}')
    print("\nThen restart Docker: sudo systemctl restart docker")


def configure_fuse_overlayfs() -> None:
    """
    Configure fuse-overlayfs for rootless Docker.

    fuse-overlayfs is faster than vfs for rootless environments.
    """
    print("\n1. Install fuse-overlayfs:")
    print("   # Ubuntu/Debian")
    print("   sudo apt install fuse-overlayfs")

    print("\n2. Configure /etc/docker/daemon.json:")
    print('   {"storage-driver": "fuse-overlayfs"}')

    print("\n3. Restart Docker")
    print("   sudo systemctl restart docker")


def check_storage_driver_performance() -> None:
    """Check and compare storage driver performance."""
    driver = get_current_storage_driver()
    print(f"Current storage driver: {driver}")

    print("\nDriver comparison:")
    print("  overlay2  - Best performance for rootful Docker")
    print("  fuse-overlayfs - Best for rootless Docker")
    print("  vfs - Slowest, used only as fallback")
    print("  devicemapper - Legacy, avoid if possible")


def main():
    print("Storage Driver Performance: fuse-overlayfs")
    print("=" * 40)

    driver = get_current_storage_driver()
    print(f"\nCurrent driver: {driver}")

    print("\nConfigure fuse-overlayfs:")
    configure_fuse_overlayfs()

    print("\nCheck current storage info:")
    print("   docker info --format '{{.Driver}}'")


if __name__ == "__main__":
    main()