#!/usr/bin/env python3
"""
GitHub Actions workflow: Automated Rollback on Deployment Failure
Company: NVIDIA | Difficulty: Medium

This workflow implements automatic rollback: when deployment fails,
it restores values.yaml from the previous commit with CI Bot author.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitOpsClient:
    """Client for Git operations used in deployment rollback."""

    CI_BOT_NAME = "CI Bot"
    CI_BOT_EMAIL = "ci-bot@example.com"
    ROLLBACK_COMMIT_MSG = "chore: automatic rollback due to deployment failure"

    def __init__(self, repo_path: str | Path = "."):
        self.repo_path = Path(repo_path)

    def run(self, *args, check: bool = True) -> subprocess.CompletedProcess:
        """Run a git command in the repository."""
        return subprocess.run(
            ["git", "-C", str(self.repo_path)] + list(args),
            check=check,
            capture_output=True,
            text=True
        )

    def get_file_at_commit(self, file_path: str, commit_ref: str = "HEAD~1") -> str:
        """Get content of a file at a specific commit."""
        result = self.run("show", f"{commit_ref}:{file_path}")
        return result.stdout

    def restore_file_from_previous_commit(self, file_path: str) -> None:
        """Restore a file to its state from the previous commit."""
        self.run("checkout", "HEAD~1", "--", file_path)

    def commit_changes(self, files: list[str], message: str) -> str:
        """Commit changes with given message and CI Bot author."""
        self.run("config", "user.name", self.CI_BOT_NAME)
        self.run("config", "user.email", self.CI_BOT_EMAIL)
        for f in files:
            self.run("add", f)
        result = self.run("commit", "-m", message)
        return result.stdout


def generate_deploy_workflow() -> str:
    """Generate the GitHub Actions deploy+rollback workflow YAML."""
    return """name: Deploy and Rollback

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh

  rollback:
    needs: deploy
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Restore previous values.yaml
        run: |
          git checkout HEAD~1 -- values.yaml
      - name: Commit rollback
        run: |
          git config user.name "CI Bot"
          git config user.email "ci-bot@example.com"
          git add values.yaml
          git commit -m "chore: automatic rollback due to deployment failure"
          git push
"""


def simulate_deployment_failure(client: GitOpsClient, values_file: str = "values.yaml") -> None:
    """Simulate a deployment failure and rollback."""
    print(f"Current values.yaml state: {client.get_file_at_commit(values_file)}")
    print("\nSimulating deployment failure...")

    # Restore from previous commit
    print(f"Restoring {values_file} from HEAD~1...")
    client.restore_file_from_previous_commit(values_file)

    # Commit rollback
    print("Committing rollback...")
    client.commit_changes([values_file], "chore: automatic rollback due to deployment failure")
    print("Rollback completed successfully!")


def main():
    print("Automated Rollback on Deployment Failure")
    print("=" * 42)
    print()
    print("Generated workflow:")
    print(generate_deploy_workflow())


if __name__ == "__main__":
    main()