#!/usr/bin/env python3
"""
GitHub Actions workflow: GitHub Actions Timeout Enforcement
Company: Bloomberg | Difficulty: Easy

This workflow enforces a job-level timeout of 2 minutes using
timeout-minutes to prevent hanging jobs.
"""

from __future__ import annotations

import subprocess
import signal
from dataclasses import dataclass


@dataclass
class TimeoutConfig:
    minutes: int
    command: str

    def run_with_timeout(self) -> subprocess.CompletedProcess:
        """Run command with timeout, killing if exceeded."""
        try:
            return subprocess.run(
                self.command,
                shell=True,
                timeout=self.minutes * 60,
                check=True,
            )
        except subprocess.TimeoutExpired as e:
            print(f"Job exceeded {self.minutes}-minute timeout and was terminated")
            raise


def generate_timeout_workflow() -> str:
    """Generate the workflow YAML with timeout enforcement."""
    return """name: Deploy with Timeout

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
      - name: Run long-running task
        run: ./scripts/long-running-task.sh
"""


def describe_timeout_behavior() -> None:
    """Describe how job-level timeouts work."""
    print("\nTimeout behavior:")
    print("  - GitHub Actions automatically cancels jobs exceeding timeout-minutes")
    print("  - Job is marked as 'failed' when killed")
    print("  - Prevents resource waste from hanging jobs")
    print("  - Timeout applies to entire job, including all steps")


def main():
    print("GitHub Actions Timeout Enforcement")
    print("=" * 35)
    print()
    print("Generated workflow:")
    print(generate_timeout_workflow())
    describe_timeout_behavior()


if __name__ == "__main__":
    main()