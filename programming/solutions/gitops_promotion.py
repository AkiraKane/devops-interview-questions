#!/usr/bin/env python3
"""
GitHub Actions workflow: Automated GitOps Promotion
Company: CapitalOne | Difficulty: Medium

This workflow:
1. Calculates SHORT_SHA from GITHUB_SHA
2. Builds Docker image tagged with SHORT_SHA
3. Clones repo-b (infrastructure) into 'infra' directory
4. Updates values.yaml tag and commits with message
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitOpsClient:
    """Client for GitOps promotion operations."""

    def __init__(self, repo_path: str | Path = "."):
        self.repo_path = Path(repo_path)

    def run(self, *args, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
        """Run git command."""
        return subprocess.run(
            ["git", "-C", str(self.repo_path)] + list(args),
            check=check,
            capture_output=capture,
            text=True,
        )

    def get_short_sha(self) -> str:
        """Get first 7 characters of current commit SHA."""
        result = self.run("rev-parse", "--short", "HEAD")
        return result.stdout.strip()

    def checkout_infra_repo(self, repo_url: str, infra_dir: str = "infra") -> None:
        """Clone infrastructure repository into specified directory."""
        infra_path = self.repo_path / infra_dir
        if infra_path.exists():
            self.run("pull", cwd=infra_path)
        else:
            subprocess.run(
                ["git", "clone", repo_url, str(infra_path)],
                check=True,
            )

    def update_values_tag(self, infra_dir: str, new_tag: str) -> None:
        """Update tag in values.yaml within infra directory."""
        values_path = self.repo_path / infra_dir / "values.yaml"
        if values_path.exists():
            content = values_path.read_text()
            # Simple tag replacement
            import re
            new_content = re.sub(r'^tag:.*', f'tag: {new_tag}', content, flags=re.MULTILINE)
            values_path.write_text(new_content)

    def commit_and_push(self, files: list[str], message: str) -> None:
        """Commit changes and push."""
        self.run("config", "user.name", "CI Bot")
        self.run("config", "user.email", "ci-bot@example.com")
        for f in files:
            self.run("add", f)
        self.run("commit", "-m", message)
        self.run("push")


def generate_promote_workflow() -> str:
    """Generate the GitOps promotion workflow YAML."""
    return """name: Promote

on:
  push:
    branches:
      - main

jobs:
  promote:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Calculate SHORT_SHA
        run: echo "SHORT_SHA=$(echo $GITHUB_SHA | head -c 7)" >> $GITHUB_ENV

      - name: Build Docker image
        run: docker build -t app:${{ env.SHORT_SHA }} .

      - name: Checkout Infrastructure
        uses: actions/checkout@v4
        with:
          repository: interview/repo-b
          path: infra

      - name: Promote
        run: |
          cd infra
          sed -i 's/^tag:.*/tag: ${{ env.SHORT_SHA }}/' values.yaml
          git config user.name "CI Bot"
          git config user.email "ci-bot@example.com"
          git add values.yaml
          git commit -m "Update tag to ${{ env.SHORT_SHA }}"
          git push
"""


def main():
    print("Automated GitOps Promotion")
    print("=" * 28)
    print()
    print("Generated workflow:")
    print(generate_promote_workflow())

    print("\nKey concepts:")
    print("  - Calculate SHORT_SHA using $GITHUB_SHA | head -c 7")
    print("  - docker build -t app:$SHORT_SHA for image tagging")
    print("  - checkout with path: infra to clone repo-b into subdirectory")
    print("  - sed for in-place YAML tag replacement")
    print("  - Automated commit and push to repo-b")


if __name__ == "__main__":
    main()