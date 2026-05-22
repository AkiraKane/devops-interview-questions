#!/usr/bin/env python3
"""
GitHub Actions workflow: GitHub Actions Retry Logic
Company: Etsy | Difficulty: Easy

This workflow implements automatic retry for flaky deployment scripts
using the nick-fields/retry@v3 action.
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass


@dataclass
class RetryConfig:
    timeout_minutes: int = 2
    max_attempts: int = 3
    retry_on: tuple[str, ...] = ("error", "warning")


def retry_command(
    cmd: str,
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    verbose: bool = True
) -> tuple[bool, int]:
    """
    Retry a command up to max_attempts times until it succeeds.

    Returns (success, attempt_count).
    """
    for attempt in range(1, max_attempts + 1):
        if verbose:
            print(f"Attempt {attempt}/{max_attempts}: {cmd}")

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            if verbose:
                print(f"  Success on attempt {attempt}")
            return True, attempt

        if verbose:
            print(f"  Failed (exit {result.returncode})")

        if attempt < max_attempts:
            time.sleep(delay_seconds)

    return False, max_attempts


def generate_retry_workflow() -> str:
    """Generate the workflow YAML with retry logic."""
    return """name: Deploy with Retry

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 2
    steps:
      - uses: actions/checkout@v4
      - name: Deploy with retry
        uses: nick-fields/retry@v3
        with:
          timeout_minutes: 2
          max_attempts: 3
          command: ./scripts/flaky-deploy.sh
"""


def main():
    print("GitHub Actions Retry Logic")
    print("=" * 31)
    print()
    print("Generated workflow:")
    print(generate_retry_workflow())
    print()
    print("Key concepts:")
    print("  - nick-fields/retry@v3 wraps steps with retry logic")
    print("  - timeout_minutes: 2 limits command execution time")
    print("  - max_attempts: 3 retries up to 3 times before failing")


if __name__ == "__main__":
    main()