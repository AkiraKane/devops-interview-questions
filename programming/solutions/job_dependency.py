#!/usr/bin/env python3
"""
GitHub Actions workflow: Job Dependency Enforcement
Company: Splunk | Difficulty: Medium

This workflow enforces a strict execution sequence: Lint → Test → Build
using the 'needs' keyword to define job dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


class Job(TypedDict):
    name: str
    needs: list[str]
    runs_on: str
    steps: list[str]


@dataclass
class Pipeline:
    jobs: list[Job] = field(default_factory=list)

    def add_job(self, name: str, needs: list[str] | None = None) -> "Pipeline":
        """Add a job with optional dependencies."""
        job: Job = {
            "name": name,
            "needs": needs or [],
            "runs_on": "ubuntu-latest",
            "steps": [],
        }
        self.jobs.append(job)
        return self

    def to_yaml(self) -> str:
        """Convert pipeline to GitHub Actions YAML format."""
        lines = [
            "name: Pipeline",
            "on: push",
            "jobs:",
        ]
        for job in self.jobs:
            lines.append(f"  {job['name']}:")
            lines.append(f"    runs-on: {job['runs_on']}")
            if job["needs"]:
                needs_str = ", ".join(f"'{n}'" for n in job["needs"])
                lines.append(f"    needs: [{needs_str}]")
            lines.append("    steps:")
            lines.append("      - uses: actions/checkout@v4")
            if job["steps"]:
                for step in job["steps"]:
                    lines.append(f"      - run: echo \"{step}\"")
        return "\n".join(lines)


def generate_pipeline_workflow() -> str:
    """Generate the workflow YAML with job dependencies."""
    return """name: Pipeline

on:
  push:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: echo "Running lint..."

  test:
    needs: [lint]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: echo "Running tests..."

  build:
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: echo "Building..."
"""


def main():
    print("Job Dependency Enforcement")
    print("=" * 28)
    print()
    print("Generated workflow:")
    print(generate_pipeline_workflow())
    print()
    print("Execution order: lint → test → build")
    print()
    print("Key concepts:")
    print("  - 'needs' defines job dependencies as a DAG")
    print("  - Jobs without 'needs' run in parallel")
    print("  - Jobs with 'needs' wait for all dependencies to complete successfully")


if __name__ == "__main__":
    main()