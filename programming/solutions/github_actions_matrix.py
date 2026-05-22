#!/usr/bin/env python3
"""
GitHub Actions workflow: GitHub Actions Matrix Build Strategy
Company: Spotify | Difficulty: Medium

This workflow runs tests across Node.js versions 18, 20, and 22
using a matrix strategy with Docker container images.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class MatrixConfig:
    node_versions: list[int] = field(default_factory=lambda: [18, 20, 22])

    def __iter__(self) -> Iterator[int]:
        return iter(self.node_versions)

    def generate_jobs(self) -> list[dict]:
        return [
            {
                "node-version": version,
                "container": f"node:{version}-slim",
            }
            for version in self.node_versions
        ]


def generate_pr_tests_workflow() -> str:
    """Generate the matrix build workflow YAML."""
    return """name: PR Tests

on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    container:
      image: node:${{ matrix.node-version }}-slim
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: ./run-tests.sh
      - name: Create version artifact
        run: echo ${{ matrix.node-version }} > node-version.txt
      - name: Upload artifact
        uses: ./.github/actions/upload-artifact
        with:
          name: node-version-${{ matrix.node-version }}
          path: node-version.txt
"""


def main():
    print("GitHub Actions Matrix Build Strategy")
    print("=" * 38)
    print()
    print("Generated workflow:")
    print(generate_pr_tests_workflow())
    print()
    print("Matrix jobs to be created:")
    matrix = MatrixConfig()
    for job in matrix.generate_jobs():
        print(f"  - {job}")


if __name__ == "__main__":
    main()