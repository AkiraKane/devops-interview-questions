#!/usr/bin/env python3
"""
Log Rotation Size Limit Configuration
Company: Splunk | Difficulty: Easy

Configure Docker log rotation to prevent logs from consuming
excessive disk space by setting max-size and max-file limits.
"""

from __future__ import annotations

import subprocess
import json


def configure_daemon_logging_defaults(log_max_size: str = "10m", log_max_files: int = 3) -> None:
    """
    Configure Docker daemon with default logging for all containers.

    Args:
        log_max_size: Maximum log file size (e.g., "10m" for 10MB)
        log_max_files: Number of log files to retain
    """
    config = {
        "log-driver": "json-file",
        "log-opts": {
            "max-size": log_max_size,
            "max-file": str(log_max_files)
        }
    }

    print("Configure Docker daemon (/etc/docker/daemon.json):")
    print(json.dumps(config, indent=2))
    print("\nThen restart Docker: sudo systemctl restart docker")


def run_with_log_rotation(
    image: str,
    container_name: str,
    log_max_size: str = "10m",
    log_max_files: int = 3
) -> None:
    """
    Run container with specific logging configuration.

    Note: logging options must be set at daemon level or using docker-compose.
    """
    cmd = [
        "docker", "run",
        "--log-opt", f"max-size={log_max_size}",
        "--log-opt", f"max-file={log_max_files}",
        "--name", container_name,
        image
    ]
    print(f"Command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, capture_output=True)


def create_docker-compose_with_logging(project_name: str = "myapp") -> str:
    """Generate docker-compose.yml with logging configuration."""
    return f'''version: "3.8"
services:
  app:
    image: myapp:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
'''


def main():
    print("Log Rotation Size Limit Configuration")
    print("=" * 38)

    print("\n1. Configure daemon defaults (/etc/docker/daemon.json):")
    configure_daemon_logging_defaults()

    print("\n2. Using docker-compose.yml (recommended):")
    print(create_docker-compose_with_logging())

    print("\n3. Verify current logging settings:")
    print("   docker info --format '{{.LoggingDriver}}'")


if __name__ == "__main__":
    main()