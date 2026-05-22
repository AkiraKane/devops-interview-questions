"""
Solution for "Remove Last Commit and Discard Changes" (Gitlab, Easy)

Scenario:
You have created a commit locally that contains incorrect changes and you want
to completely erase it from history.

Task:
Navigate to `/home/interview/repo`. Remove the last commit entirely and
discard all associated file changes.
"""


def remove_last_commit_discard_changes(repo_path: str = "/home/interview/repo"):
    """
    Remove the last commit and discard all changes.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: View current commit history
    print("Current commit history:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no commits)")

    # Step 2: View what files were changed
    print("\nFiles changed in last commit:")
    result = subprocess.run(
        ["git", "show", "--stat", "--name-only", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 3: Check current working directory status
    print("Working directory status:")
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(clean)")

    # Step 4: Reset --hard to remove the commit AND discard changes
    # HEAD~1 moves the branch pointer back 1 commit
    # --hard discards all changes in working directory and staging
    print("\nRemoving last commit and discarding all changes...")
    result = subprocess.run(
        ["git", "reset", "--hard", "HEAD~1"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Successfully removed last commit and discarded changes!")
    else:
        print(f"Error: {result.stderr}")
        raise RuntimeError("Reset failed")

    # Step 5: Verify the result
    print("\nCommit history after reset:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no more commits)")

    print("\nWorking directory status after reset:")
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(clean)")


def main():
    """Demonstrate the solution for removing last commit and discarding changes."""
    print("=" * 60)
    print("Remove Last Commit and Discard Changes")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    remove_last_commit_discard_changes(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Command:
    git reset --hard HEAD~1

What this does:
1. Moves HEAD back 1 commit (branch pointer moves)
2. Updates staging area to match previous commit
3. Updates working directory to match staging

Reset Modes Comparison:
    git reset --soft HEAD~1    - Only moves HEAD, keeps changes staged
    git reset --mixed HEAD~1   - Moves HEAD, unstages changes (default)
    git reset --hard HEAD~1    - Moves HEAD, unstages, discards changes

DANGER:
- --hard DISCARDS changes permanently
- This cannot be undone without using reflog

For undoing a public commit (already pushed):
    git revert HEAD             - Creates new commit that undoes changes
    git push origin main       - Push the revert commit

For local-only commits:
    git reset --hard HEAD~1    - Permanent removal
""")


if __name__ == "__main__":
    main()