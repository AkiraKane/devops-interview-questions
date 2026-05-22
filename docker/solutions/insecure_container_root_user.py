#!/usr/bin/env python3
"""
Insecure Container Root User Fix
Company: Cloudflare | Difficulty: Easy

Fix containers running as root by creating a non-root user and
 configuring the Dockerfile to run as that user for improved security.
"""

from __future__ import annotations

import subprocess
import os


def create_non_root_user(username: str = "appuser") -> str:
    """Generate Dockerfile instructions to create non-root user."""
    return f'''
# Create non-root user
RUN useradd -m -s /bin/bash {username}

# Set ownership of application directory
RUN chown -R {username}:{username} /app

# Switch to non-root user
USER {username}
'''


def update_dockerfile_for_non_root(dockerfile_path: str, username: str = "appuser") -> None:
    """Update existing Dockerfile to run as non-root user."""
    content = f'''
# Create non-root user
RUN useradd -m -s /bin/bash {username}

# Switch to non-root user
USER {username}
'''

    with open(dockerfile_path, "a") as f:
        f.write(content)

    print(f"Updated {dockerfile_path} with non-root user: {username}")


def run_container_as_non_root(image: str, container_name: str) -> None:
    """Run container as non-root user using docker run."""
    cmd = [
        "docker", "run",
        "--user", "1000:1000",
        "--name", container_name,
        image
    ]
    subprocess.run(cmd, check=True)


def main():
    print("Insecure Container Root User Fix")
    print("=" * 36)

    print("\nSolution - Add to Dockerfile:")
    print(create_non_root_user())

    print("\nCommands:")
    print("  # Build image")
    print("  docker build -t myapp:secure .")
    print()
    print("  # Run as non-root user")
    print("  docker run --user 1000:1000 --name myapp myapp:secure")
    print()
    print("  # Verify user")
    print("  docker exec myapp whoami  # Should show 'appuser'")


if __name__ == "__main__":
    main()