#!/usr/bin/env python3
"""
GitHub Actions workflow: PR Test Gate
Company: Adobe | Difficulty: Medium

This workflow runs tests on pull requests and uploads results
as artifacts, using 'if: always()' to upload even on failure.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class StepCondition(Enum):
    ALWAYS = "always"
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class Step:
    name: str
    run: str | None = None
    uses: str | None = None
    condition: StepCondition = StepCondition.SUCCESS
    with_args: dict | None = None

    def to_yaml(self, indent: int = 0) -> str:
        pad = " " * indent
        lines = [f"{pad}- name: {self.name}"]

        if self.run:
            lines.append(f"{pad}  run: {self.run}")

        if self.uses:
            lines.append(f"{pad}  uses: {self.uses}")

        if self.with_args:
            lines.append(f"{pad}  with:")
            for key, value in self.with_args.items():
                lines.append(f"{pad}    {key}: {value}")

        if self.condition != StepCondition.SUCCESS:
            lines.append(f"{pad}  if: {self.condition.value}()")

        return "\n".join(lines)


class TestRunner:
    """Runs test suite and handles results."""

    def __init__(self, test_script: str = "./run-tests.sh"):
        self.test_script = test_script
        self.results_path = Path("test-results.txt")

    def run(self) -> subprocess.CompletedProcess:
        """Execute the test suite."""
        return subprocess.run(
            self.test_script,
            shell=True,
            capture_output=True,
            text=True,
        )

    def save_results(self, output: str) -> None:
        """Save test output to results file."""
        self.results_path.write_text(output)

    def run_and_save(self) -> subprocess.CompletedProcess:
        """Run tests and save results."""
        result = self.run()
        self.save_results(result.stdout + result.stderr)
        return result


def generate_pr_tests_workflow() -> str:
    """Generate the PR test gate workflow YAML."""
    return """name: PR Tests

on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run test suite
        run: ./run-tests.sh
      - name: Upload test results
        uses: ./.github/actions/upload-artifact
        if: always()
        with:
          name: test-results
          path: test-results.txt
"""


def main():
    print("PR Test Gate")
    print("=" * 15)
    print()
    print("Generated workflow:")
    print(generate_pr_tests_workflow())

    print("\nKey concepts:")
    print("  - pull_request trigger fires on PR events")
    print("  - if: always() ensures artifact upload runs regardless of test outcome")
    print("  - Test results persist for debugging failed runs")


if __name__ == "__main__":
    main()