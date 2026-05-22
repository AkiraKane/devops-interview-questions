#!/usr/bin/env python3
"""
Solution for: Using Unmounted Partitions

Company: RedHat | Difficulty: Medium

Scenario:
A server has unmounted partitions that are not being utilized.

Task:
Identify an unmounted partition that is safe to use (avoiding system-critical
mounts like /, /boot, swap), create an ext4 filesystem on it with label
data_extra, mount it at /mnt/test, and verify accessibility.

Solution Approach:
- Use `lsblk` to list all partitions and their mount status
- Identify unmounted, non-critical partitions
- Use `mkfs.ext4` to create a filesystem with label
- Mount at /mnt/test and verify
"""

import subprocess
import os


def get_unmounted_partitions():
    """
    Find partitions that are not currently mounted.

    Uses lsblk to list block devices and filters for unmounted ones.
    """
    result = subprocess.run(
        ['lsblk', '-lnpo', 'NAME,SIZE,TYPE,MOUNTPOINT'],
        capture_output=True, text=True
    )

    all_parts = []
    mounted_parts = set()

    for line in result.stdout.strip().split('\n'):
        parts = line.split()
        if len(parts) >= 3:
            device = parts[0]
            size = parts[1]
            dev_type = parts[2]
            mountpoint = parts[3] if len(parts) > 3 else ''

            if dev_type == 'part':
                all_parts.append((device, size, mountpoint))
                if mountpoint:
                    mounted_parts.add(device)

    # Filter to unmounted partitions
    unmounted = [(dev, size) for dev, size, mp in all_parts if not mp]

    # Also exclude critical system partitions by checking device path
    critical_patterns = ['/dev/sda', '/dev/nvme0n1']  # Typical root disk
    safe = []
    for dev, size in unmounted:
        # Check if this partition's parent disk is the root disk
        # We want non-root-disk partitions
        is_safe = True
        for pattern in critical_patterns:
            if dev.startswith(pattern):
                # Check if it's the root partition itself
                root_result = subprocess.run(
                    ['findmnt', '-n', '-o', 'SOURCE', '/'],
                    capture_output=True, text=True
                )
                root_dev = root_result.stdout.strip()
                if dev == root_dev:
                    is_safe = False
        if is_safe:
            safe.append((dev, size))

    return safe


def create_filesystem(device, label='data_extra'):
    """Create ext4 filesystem on a device with the given label."""
    print(f"Creating ext4 filesystem on {device} with label '{label}'...")

    result = subprocess.run(
        ['mkfs.ext4', '-L', label, device],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Error creating filesystem: {result.stderr}")
        return False

    print(f"Filesystem created successfully")
    return True


def mount_partition(device, mountpoint='/mnt/test'):
    """Mount a device at the specified mountpoint."""
    os.makedirs(mountpoint, exist_ok=True)

    result = subprocess.run(
        ['mount', device, mountpoint],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Error mounting: {result.stderr}")
        return False

    print(f"Mounted {device} at {mountpoint}")
    return True


def verify_mount(mountpoint='/mnt/test'):
    """Verify the mount is accessible and show filesystem info."""
    # Check mount status
    result = subprocess.run(
        ['findmnt', mountpoint],
        capture_output=True, text=True
    )
    print(f"\nMount info:\n{result.stdout}")

    # Check filesystem label
    result = subprocess.run(
        ['lsblk', '-no', 'LABEL', mountpoint],
        capture_output=True, text=True
    )
    print(f"Label: {result.stdout.strip()}")

    # Test write access
    test_file = os.path.join(mountpoint, '.mount_test')
    try:
        with open(test_file, 'w') as f:
            f.write('mount test')
        os.remove(test_file)
        print("Write test: PASSED")
    except PermissionError:
        print("Write test: Permission denied (may need root)")


def main():
    print("=== Using Unmounted Partitions ===\n")

    print("Scanning for unmounted partitions...")
    unmounted = get_unmounted_partitions()

    if not unmounted:
        print("No unmounted partitions available for use")
        print("\nFor demonstration, here are the commands that would be used:")
        print("  lsblk -lnpo NAME,SIZE,TYPE,MOUNTPOINT  # Find unmounted partitions")
        print("  mkfs.ext4 -L data_extra /dev/sdXN       # Create filesystem")
        print("  mount /dev/sdXN /mnt/test                # Mount it")
        return

    print(f"Found {len(unmounted)} unmounted partition(s):")
    for dev, size in unmounted:
        print(f"  {dev} ({size})")

    # Use the first available unmounted partition
    device, size = unmounted[0]
    print(f"\nUsing {device} ({size})")

    if create_filesystem(device, 'data_extra'):
        if mount_partition(device, '/mnt/test'):
            verify_mount('/mnt/test')


if __name__ == '__main__':
    main()
