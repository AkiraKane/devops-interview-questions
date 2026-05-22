#!/usr/bin/env python3
"""
GitHub Actions workflow: Environment-Gated Deployment
Company: Autodesk | Difficulty: Easy

This workflow implements a gated deployment: staging runs automatically,
production requires manual approval via GitHub Environments.
"""

from __future__ import annotations

from typing import NamedTuple


class Job(NamedTuple):
    name: str
    needs: list[str] | None = None
    environment: str | None = None
    steps: list[str] | None = None

    def to_yaml(self, indent: int = 0) -> str:
        pad = " " * indent
        lines = [f"{self.name}:", f"{pad}  runs-on: ubuntu-latest"]

        if self.environment:
            lines.append(f"{pad}  environment:")
            lines.append(f"{pad}    name: {self.environment}")

        if self.needs:
            lines.append(f"{pad}  needs: [{', '.join(self.needs)}]")

        if self.steps:
            for step in self.steps:
                lines.append(f"{pad}  steps:")
                lines.append(f"{pad}    - {step}")

        return "\n".join(lines)


def generate_deploy_workflow() -> str:
    """Generate the environment-gated deployment workflow YAML."""
    return """name: Deploy Pipeline

on:
  push:
    branches:
      - main

jobs:
  staging:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        run: echo "Deploying to staging..."

  production:
    needs: [staging]
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: echo "Deploying to production..."
"""


def describe_environment_protection() -> None:
    """Describe GitHub Environments protection rules."""
    print("\nGitHub Environments provide:")
    print("  - Required reviewers (manual approval)")
    print("  - Protection rules (branch, timeout, etc.)")
    print("  - Environment-specific secrets")
    print("  - Deployment history tracking")


def main():
    print("Environment-Gated Deployment")
    print("=" * 34)
    print()
    print("Generated workflow:")
    print(generate_deploy_workflow())
    describe_environment_protection()


if __name__ == "__main__":
    main()