#!/usr/bin/env python3
"""
GitHub Actions workflow: Multi-Job Workflow with Artifact Handoff
Company: Anthropic | Difficulty: Medium

This workflow implements a two-stage pipeline:
- Job A (test-job): Runs tests and uploads results
- Job B (report-job): Downloads results, creates summary, uploads summary
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Artifact:
    name: str
    path: str
    content: str = ""


class TestResultAnalyzer:
    """Analyzes test results and generates summaries."""

    @staticmethod
    def count_passed_tests(results_file: str | Path) -> int:
        """Count number of PASS: lines in test results."""
        path = Path(results_file)
        if not path.exists():
            return 0
        content = path.read_text()
        return content.count("PASS:")

    @staticmethod
    def generate_summary(passed_count: int) -> str:
        """Generate test summary in specified format."""
        return f"Total Passed Tests: {passed_count}"


class LocalArtifactClient:
    """Simulates .github/actions/upload-artifact and download-artifact."""

    def __init__(self, artifact_dir: str | Path = "/tmp/github-artifacts/1"):
        self.artifact_dir = Path(artifact_dir)
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, name: str, path: str | Path) -> None:
        """Upload artifact (copy to artifact directory)."""
        src = Path(path)
        dst = self.artifact_dir / name
        if src.is_file():
            dst.write_text(src.read_text())
        else:
            dst.write_text("")
        print(f"Uploaded artifact: {name}")

    def download(self, name: str) -> Path:
        """Download artifact (return path to artifact)."""
        artifact_path = self.artifact_dir / name
        if not artifact_path.exists():
            raise FileNotFoundError(f"Artifact not found: {name}")
        return artifact_path


def generate_artifact_handoff_workflow() -> str:
    """Generate the artifact handoff workflow YAML."""
    return """name: Artifact Handoff

on:
  pull_request:

jobs:
  test-job:
    runs-on: ubuntu-latest
    container:
      image: node:20-slim
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: ./run-tests.sh
      - name: Upload test results
        uses: ./.github/actions/upload-artifact
        with:
          name: test-results
          path: test-results.txt

  report-job:
    needs: test-job
    runs-on: ubuntu-latest
    container:
      image: node:20-slim
    steps:
      - uses: actions/checkout@v4
      - name: Download test results
        uses: ./.github/actions/download-artifact
        with:
          name: test-results
      - name: Create summary
        run: |
          if [ -f test-results.txt ]; then
            COUNT=$(grep -c "PASS:" test-results.txt)
            echo "Total Passed Tests: $COUNT" > summary.txt
          fi
      - name: Upload summary
        uses: ./.github/actions/upload-artifact
        with:
          name: test-summary
          path: summary.txt
"""


def main():
    print("Multi-Job Workflow with Artifact Handoff")
    print("=" * 40)
    print()
    print("Generated workflow:")
    print(generate_artifact_handoff_workflow())

    # Simulate artifact handling
    print("\nSimulated artifact handoff:")
    client = LocalArtifactClient()

    # Create mock test results
    test_results = Path("/tmp/test-results.txt")
    test_results.write_text("PASS: test_1\nPASS: test_2\nFAIL: test_3\nPASS: test_4\n")

    # Upload
    client.upload("test-results", test_results)

    # Download and analyze
    analyzer = TestResultAnalyzer()
    passed = analyzer.count_passed_tests(client.download("test-results"))
    summary = analyzer.generate_summary(passed)
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()