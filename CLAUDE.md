# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **DevOps interview question bank** — a markdown-only repository containing ~115 hands-on interview questions organized into 8 topic directories. Each question describes a real-world scenario with a task to solve. Questions are sourced from real company interviews (Google, Amazon, Meta, Apple, Coinbase, Airbnb, etc.).

The repository is a static markdown resource — there is no code to build, test, or run. The primary work is writing and maintaining question content.

## Directory Structure

```
cloud/         # AWS questions (IAM, VPC, Lambda, Route53, EC2, DynamoDB)
docker/        # Container security, resource limits, networking, multi-arch
git/           # Version control (rebase, stash, cherry-pick, history)
kubernetes/    # Pod issues, Deployments, ConfigMaps, RBAC, Storage
linux/         # System administration, process management, disk/memory
networking/    # Routing, DNS, SSH, HTTP, port management
programming/   # GitHub Actions CI/CD pipelines and workflows
security/      # SSL/TLS certificates (single file)
```

Total: ~116 markdown files, one per question. `README.md` at root is the master index table linking all questions.

## Question File Format

Each question file follows this pattern:

```markdown
# Question Title (Title Case)

> **Company:** [Company] | **Difficulty:** [Easy/Medium/Hard]

---

#### Scenario

[Context and problem description]

#### Task

[Specific action(s) to perform]

#### Example (optional)

[Before/after or expected output]

---
📹 [Video Solution](https://prepare.sh/interview/...)
```

- Title is Title Case, filename is kebab-case
- Difficulty: Entry (Easy), Mid (Medium), Senior (Hard)
- Video links point to prepare.sh for interactive solving
- Never remove existing content — only add new `#### Solution` section

## Writing Solutions

When adding a solution to a question file, append a `## Solution` section after the `---` divider (keeping the video link intact):

```markdown
---

## Solution

### Step-by-Step Answer

[Exact commands or YAML changes needed]

### Detailed Explanation

[Why each step works, under-the-hood behavior, edge cases]

### Verification

[Commands to verify the solution — include expected output]

### Key Concepts

- [Related concept 1]
- [Related concept 2]
```

- Use `code blocks` for all commands and configs
- For Linux/Git/Docker/Networking: lead with exact commands, explain flags
- For Kubernetes/Cloud: walk through the YAML/resource manifest changes
- For CI-CD: walk through workflow syntax and job logic
- Keep existing `📹 Video Solution` link — do not remove it