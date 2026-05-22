#!/usr/bin/env python3
"""
GitHub Actions workflow: Path-Based Workflow Execution
Company: Coinbase | Difficulty: Medium

This workflow runs only when files under the /infra directory change,
using path-based filtering with paths option.
"""

from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class PathFilter:
    """Filters paths based on configured patterns."""
    patterns: list[str] = field(default_factory=list)

    def matches(self, path: str) -> bool:
        """Check if path matches any filter pattern."""
        for pattern in self.patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
            # Support directory patterns like 'infra/**'
            if pattern.endswith('/**'):
                dir_pattern = pattern[:-2]
                if path.startswith(dir_pattern + '/') or path == dir_pattern:
                    return True
        return False

    def filter_changed_files(self, files: list[str]) -> list[str]:
        """Return only files matching the filter patterns."""
        return [f for f in files if self.matches(f)]


@dataclass
class WorkflowTrigger:
    """Represents a GitHub Actions workflow trigger with path filtering."""
    paths: list[str] = field(default_factory=list)

    def should_run(self, changed_files: list[str]) -> bool:
        """Determine if workflow should run based on changed files."""
        if not self.paths:
            return True
        return len(self.filter_changed_files(changed_files)) > 0

    def filter_changed_files(self, files: list[str]) -> list[str]:
        """Filter files that match the path patterns."""
        filter_config = PathFilter(patterns=self.paths)
        return filter_config.filter_changed_files(files)


def generate_infra_check_workflow() -> str:
    """Generate the path-based workflow YAML."""
    return """name: Infrastructure Check

on:
  push:
    paths:
      - 'infra/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    container:
      image: node:20-slim
    steps:
      - uses: actions/checkout@v4
      - name: Validate infrastructure
        run: ./validate-infra.sh
      - name: Upload validation report
        uses: ./.github/actions/upload-artifact
        with:
          name: validation-report
          path: validation-result.txt
"""


def main():
    print("Path-Based Workflow Execution")
    print("=" * 32)
    print()
    print("Generated workflow:")
    print(generate_infra_check_workflow())

    # Simulate path filtering
    print("\nSimulated path filtering:")
    trigger = WorkflowTrigger(paths=["infra/**"])

    changed = ["infra/main.tf", "docs/README.md", "src/app.py"]
    matched = trigger.filter_changed_files(changed)
    print(f"Changed files: {changed}")
    print(f"Files matching 'infra/**': {matched}")
    print(f"Should run: {trigger.should_run(changed)}")


if __name__ == "__main__":
    main()