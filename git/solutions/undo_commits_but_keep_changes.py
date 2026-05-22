"""
Solution for "Undo Commits but Keep Changes" (CrowdStrike, Easy)

Scenario:
You have a Git repository at `/home/interview/repo` with three recent commits
on the `main` branch that were premature and need to be reorganized.

Task:
Undo the last three commits while keeping all changes in your working directory
so you can recommit them properly.
"""


def undo_commits_keep_changes(repo_path: str = "/home/interview/repo", num_commits: int = 3):
    """
    Undo the last N commits while keeping changes staged.

    Args:
        repo_path: Path to the Git repository
        num_commits: Number of commits to undo
    """
    import subprocess

    # Step 1: View current commit history
    print(f"Current commit history (last {num_commits + 1} commits):")
    result = subprocess.run(
        ["git", "log", "--oneline", f"-{num_commits + 1}"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no commits)")

    # Step 2: Check what's in these commits (for context)
    print("\nWhat's in the commits to be undone:")
    result = subprocess.run(
        ["git", "diff", f"HEAD~{num_commits}", "--stat"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")

    # Step 3: Reset HEAD by 3 commits but keep changes staged
    # --soft keeps changes in staging area
    # --mixed (default) keeps changes in working directory (unstaged)
    # We'll use --mixed to match the example which shows "Changes not staged"

    print(f"\nResetting last {num_commits} commits (keeping changes in working directory)...")
    result = subprocess.run(
        ["git", "reset", "--mixed", f"HEAD~{num_commits}"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Reset successful!")
    else:
        print(f"Reset error: {result.stderr}")
        raise RuntimeError("Reset failed")

    # Step 4: Verify commit history
    print("\nCommit history after reset:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no commits)")

    # Step 5: Verify working directory changes
    print("\nWorking directory status after reset:")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 6: Show what files have changes
    print("Files with changes available for recommit:")
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no changes)")


def main():
    """Demonstrate the solution for undoing commits while keeping changes."""
    print("=" * 60)
    print("Undo Commits but Keep Changes")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    undo_commits_keep_changes(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Command:
    git reset HEAD~3               # --mixed by default
    git reset --mixed HEAD~3       # Explicit: unstages changes, keeps files
    git reset --soft HEAD~3        # Keeps changes staged

Comparison of Reset Modes:
    git reset --soft HEAD~3
    - Moves HEAD back 3 commits
    - Keeps changes staged
    - Working directory unchanged

    git reset --mixed HEAD~3 (default)
    - Moves HEAD back 3 commits
    - Unstages changes (moves to working directory)
    - Working directory unchanged

    git reset --hard HEAD~3
    - Moves HEAD back 3 commits
    - Discards all changes (staged and working directory)
    - DANGEROUS - cannot recover without reflog

Use When:
- Premature commits need reorganization
- Need to split/merge commits differently
- Accidentally committed to wrong branch
- Want to recommit with better message

Alternative for Undoing Commits:
    git revert HEAD~3..HEAD        # Creates new commits that undo changes
    (safer for shared/pushed history)
""")


if __name__ == "__main__":
    main()