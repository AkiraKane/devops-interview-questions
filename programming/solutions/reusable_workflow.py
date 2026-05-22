#!/usr/bin/env python3
"""
GitHub Actions workflow: Reusable Workflow with Input Parameters
Company: Adobe | Difficulty: Medium

This implements:
1. A reusable workflow (shared-build.yml) that accepts 'app-name' input
2. A caller workflow (deploy.yml) that calls the reusable workflow
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


class WorkflowInput(TypedDict):
    name: str
    type: str
    required: bool
    default: str | None


@dataclass
class ReusableWorkflow:
    name: str
    inputs: dict[str, WorkflowInput]

    def to_workflow_call_yaml(self) -> str:
        """Generate workflow_call trigger definition."""
        lines = [f"name: {self.name}", "", "on:", "  workflow_call:", "    inputs:"]

        for input_name, input_def in self.inputs.items():
            lines.append(f"      {input_name}:")
            lines.append(f"        required: {str(input_def['required']).lower()}")
            if input_def.get("default"):
                lines.append(f"        default: {input_def['default']}")

        return "\n".join(lines)


def generate_shared_build_workflow() -> str:
    """Generate the reusable workflow YAML."""
    return """name: Shared Build

on:
  workflow_call:
    inputs:
      app-name:
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: node:20-slim
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: ./build.sh ${{ inputs.app-name }}
      - name: Upload build artifact
        uses: ./.github/actions/upload-artifact
        with:
          name: build-${{ inputs.app-name }}
          path: .
"""


def generate_deploy_workflow() -> str:
    """Generate the caller workflow YAML."""
    return """name: Deploy

on:
  push:

jobs:
  build:
    uses: ./.github/workflows/shared-build.yml
    with:
      app-name: frontend
"""


def main():
    print("Reusable Workflow with Input Parameters")
    print("=" * 40)
    print()
    print("Reusable workflow (shared-build.yml):")
    print(generate_shared_build_workflow())
    print()
    print("Caller workflow (deploy.yml):")
    print(generate_deploy_workflow())

    print("\nKey concepts:")
    print("  - workflow_call marks workflow as reusable")
    print("  - inputs define typed parameters")
    print("  - uses: ./path/to/workflow.yml calls reusable workflow")
    print("  - with: passes input parameters")


if __name__ == "__main__":
    main()