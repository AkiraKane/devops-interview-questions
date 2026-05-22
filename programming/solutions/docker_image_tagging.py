#!/usr/bin/env python3
"""
GitHub Actions workflow: Docker Image Tagging with Commit SHA
Company: Microsoft | Difficulty: Medium

This workflow automatically builds a Docker image named 'app' and tags it
with the short commit SHA on every push to the main branch.
"""

from __future__ import annotations

import os
import subprocess


def generate_build_workflow() -> str:
    """Generate the GitHub Actions workflow YAML for Docker image tagging."""
    return """name: Build and Tag

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract commit SHA
        run: echo "SHA=$(echo $GITHUB_SHA | head -c 7)" >> $GITHUB_ENV

      - name: Build Docker image
        run: docker build -t app:${{ env.SHA }} .
"""


def extract_short_sha(full_sha: str) -> str:
    """Extract first 7 characters of commit SHA."""
    return full_sha[:7]


def build_docker_image(image_name: str, tag: str, dockerfile_path: str = ".") -> subprocess.CompletedProcess:
    """Build Docker image with specified tag."""
    return subprocess.run(
        ["docker", "build", "-t", f"{image_name}:{tag}", dockerfile_path],
        check=True
    )


def main():
    print("Docker Image Tagging with Commit SHA")
    print("=" * 40)
    print()
    print("Generated workflow:")
    print(generate_build_workflow())

    # Simulate extracting SHA
    example_sha = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    short_sha = extract_short_sha(example_sha)
    print(f"\nExample: Full SHA = {example_sha}")
    print(f"         Short SHA = {short_sha}")


if __name__ == "__main__":
    main()