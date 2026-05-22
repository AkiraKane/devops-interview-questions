"""
Solution for "Recover Lost Commits from Detached Head" (Kayak, Medium)

Scenario:
You have a Git repository at `/home/interview/repo` where you were in a detached
HEAD state, made 3 commits, then switched back to the `main` branch. Those 3
commits are now unreachable and appear to be lost since no branch references them.

Task:
Navigate to the repository at `/home/interview/repo`, check the reflog to locate
the lost commits from the detached HEAD state, create a new branch called
`recovered-work` pointing to those commits.
"""


def recover_lost_commits(repo_path: str = "/home/interview/repo"):
    """
    Recover lost commits from detached HEAD state using reflog.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: Check current state
    print("Current branches:")
    result = subprocess.run(
        ["git", "branch", "-v"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    print("\nCurrent HEAD commit:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 2: Check reflog to find the lost commits
    print("\nSearching reflog for detached HEAD commits...")
    print("(Detached HEAD sessions are marked as 'HEAD@{n}' in reflog)")

    result = subprocess.run(
        ["git", "reflog", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print("Recent reflog entries:")
    print(result.stdout)

    # Step 3: Search for commits made during detached HEAD state
    # These are typically not on any branch
    print("\nSearching for commits not on any branch...")

    # Find all commits not reachable from any branch
    result = subprocess.run(
        ["git", "fsck", "--unreachable", "--no-reflogs"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print("Unreachable commits (may include our lost commits):")
    print(result.stdout if result.stdout else "(no unreachable commits found)")

    # Step 4: Look for our lost commits in reflog
    print("\n\nLooking for detached HEAD state commits in reflog...")

    # Parse reflog to find the HEAD position before we checked out main
    result = subprocess.run(
        ["git", "reflog", "show", "HEAD", "--date=iso"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().split("\n")
    target_commits = []

    for line in lines:
        # Look for checkout entries (detached HEAD)
        if "checkout: moving" in line or "HEAD@{ detached" in line.lower():
            print(f"\nFound detached HEAD reference: {line}")

    # Alternative: Look at HEAD@{} entries for commits
    # In detached HEAD, the reflog will show commits with HEAD@{n} notation
    print("\nSearching for HEAD positions with commits...")

    result = subprocess.run(
        ["git", "log", "-g", "--oneline", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print("Reflog of HEAD (includes detached HEAD commits):")
    print(result.stdout)

    # Step 5: Create branch pointing to recovered commits
    # The lost commits from detached HEAD would be visible in the reflog
    # We can create a branch at a specific reflog entry

    # For simulation, let's create the recovery branch
    # In real scenario, you would identify the specific commit hash

    # Get the commit before we left detached HEAD state
    # This is typically in reflog as "checkout: moving from..."
    recovery_ref = "HEAD@{1}"  # This might need adjustment based on actual reflog

    print(f"\nCreating recovered-work branch at {recovery_ref}...")
    result = subprocess.run(
        ["git", "branch", "recovered-work", recovery_ref],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Branch recovered-work created!")

        # Verify the recovered commits
        print("\nRecovered commits:")
        result = subprocess.run(
            ["git", "log", "recovered-work", "--oneline", "-5"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        print(result.stdout if result.stdout else "(no commits in recovered-work)")

        # Verify branch exists
        print("\nCurrent branches:")
        result = subprocess.run(
            ["git", "branch", "-v"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        print(result.stdout)
    else:
        print(f"Error: {result.stderr}")
        print("\nNote: Detached HEAD commits may have been garbage collected")
        print("or may require a different reflog entry to recover")


def main():
    """Demonstrate the solution for recovering lost commits."""
    print("=" * 60)
    print("Recover Lost Commits from Detached HEAD")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    recover_lost_commits(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git reflog                         - View reflog (commit history references)
2. git reflog HEAD -10                - Show last 10 HEAD positions
3. git log -g --oneline               - Show reflog as log entries
4. git fsck --unreachable             - Find unreachable commits
5. git branch recovered-work HEAD@{n} - Create branch at specific reflog entry

What is Reflog?
- Git maintains a log of where HEAD and branches have pointed
- This includes detached HEAD states
- Default retention: 90 days for dangling commits

Recovery Process:
1. Find the commit in reflog: git reflog or git log -g
2. Note the commit hash or reflog reference
3. Create a branch: git branch recovered-work <hash>
4. Verify commits are restored

Warning:
- Reflog is local - doesn't help recover from another machine
- Garbage collection can remove old unreachable commits
- Force pushes can overwrite reflog entries
""")


if __name__ == "__main__":
    main()