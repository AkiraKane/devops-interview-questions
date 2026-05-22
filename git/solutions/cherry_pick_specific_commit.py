"""
Solution for "Cherry Pick Specific Commit" (Ubisoft, Easy)

Scenario:
You have a Git repository at `/home/interview/repo` on the main branch. A commit
on the `feature` branch contains a bug fix you need on `main`, but you don't
want to merge the entire feature branch.

Task:
Navigate to `/home/interview/repo`, identify the bug fix commit on the `feature`
branch from the commit history, then apply it to `main`.
"""


def find_and_cherry_pick_commit(repo_path: str = "/home/interview/repo"):
    """
    Find a bug fix commit on feature branch and cherry-pick it to main.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess
    import re

    # Step 1: Switch to main branch
    print("Switching to main branch...")
    subprocess.run(["git", "checkout", "main"], cwd=repo_path, capture_output=True)

    # Step 2: View commits on feature branch to identify the bug fix
    print("\nViewing commits on feature branch:")
    result = subprocess.run(
        ["git", "log", "feature", "--oneline", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 3: Find commits related to "bug fix" or "fix" on feature branch
    result = subprocess.run(
        ["git", "log", "feature", "--oneline", "--grep=bug", "--grep=fix", "--all-match"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        # Fallback: get the most recent commit
        result = subprocess.run(
            ["git", "log", "feature", "-1", "--format=%H %s"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

    commit_info = result.stdout.strip().split(" ", 1)
    commit_hash = commit_info[0]
    commit_message = commit_info[1] if len(commit_info) > 1 else ""

    print(f"\nFound bug fix commit: {commit_hash[:8]} - {commit_message}")

    # Step 4: Cherry-pick the commit onto main
    print(f"\nCherry-picking {commit_hash[:8]} onto main...")
    result = subprocess.run(
        ["git", "cherry-pick", commit_hash],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Successfully cherry-picked the bug fix!")
    else:
        print(f"Cherry-pick had conflicts: {result.stderr}")
        print("Resolve conflicts and complete with: git cherry-pick --continue")
        raise RuntimeError("Cherry-pick failed with conflicts")

    # Step 5: Verify the result
    print("\nVerifying main branch history:")
    result = subprocess.run(
        ["git", "log", "main", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Demonstrate the solution for cherry-picking a specific commit."""
    print("=" * 60)
    print("Cherry Pick Specific Commit")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    find_and_cherry_pick_commit(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git log feature --oneline              - View commits on feature branch
2. git log feature --grep="bug"           - Search for commits with "bug" in message
3. git cherry-pick <commit-hash>          - Apply a specific commit to current branch

Cherry-pick creates a NEW commit with the SAME changes but a NEW hash.
This is useful for:
- Applying specific bug fixes without merging entire branches
- Backporting fixes to release branches
- Integrating specific changes while keeping history clean
""")


if __name__ == "__main__":
    main()