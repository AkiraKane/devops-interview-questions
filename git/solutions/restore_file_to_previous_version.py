"""
Solution for "Restore File to Previous Version" (Slack, Medium)

Scenario:
You have a Git repository at `/home/interview/repo` where the `config.js` file
has been modified in the last two commits, but those changes introduced bugs.
You need to **restore only `config.js` to the version it had 2 commits ago**
without affecting any other files.

Task:
Restore `config.js` to its state from 2 commits ago, stage and commit this
change with `Restore config.js` message.
"""


def restore_file_to_previous_version(
    repo_path: str = "/home/interview/repo",
    filename: str = "config.js",
    commits_back: int = 2
):
    """
    Restore a specific file to a previous version.

    Args:
        repo_path: Path to the Git repository
        filename: The file to restore
        commits_back: How many commits back to restore
    """
    import subprocess

    # Step 1: View the file's commit history
    print(f"History of {filename}:")
    result = subprocess.run(
        ["git", "log", "--oneline", "--", filename],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(file has no history)")

    # Step 2: View the current content of the file
    print(f"\nCurrent content of {filename}:")
    result = subprocess.run(
        ["cat", f"{repo_path}/{filename}"],
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(file doesn't exist or is empty)")

    # Step 3: Get the version from N commits ago
    # HEAD~2 means "the commit before the last two"
    target_ref = f"HEAD~{commits_back}"

    print(f"\nGetting {filename} from {target_ref}...")

    # Restore the file to the version from specified commits ago
    # -- before filename signals end of git options
    result = subprocess.run(
        ["git", "checkout", target_ref, "--", filename],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Successfully restored {filename} to {target_ref} version!")
    else:
        print(f"Error restoring file: {result.stderr}")
        raise RuntimeError("Failed to restore file")

    # Step 4: Verify the restored content
    print(f"\nRestored content of {filename}:")
    result = subprocess.run(
        ["cat", f"{repo_path}/{filename}"],
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(file is empty)")

    # Step 5: Check git status to see staged changes
    print("\nGit status:")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 6: Stage the restored file
    print(f"\nStaging {filename}...")
    subprocess.run(
        ["git", "add", filename],
        cwd=repo_path,
        capture_output=True
    )

    print("File staged successfully!")

    # Step 7: Commit the restoration
    print(f"\nCommitting with message 'Restore config.js'...")
    result = subprocess.run(
        ["git", "commit", "-m", "Restore config.js"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Commit successful!")
    else:
        print(f"Error committing: {result.stderr}")
        raise RuntimeError("Failed to commit")

    # Step 8: Verify the commit
    print("\nVerifying commit:")
    subprocess.run(
        ["git", "log", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True
    )


def main():
    """Demonstrate the solution for restoring a file to a previous version."""
    print("=" * 60)
    print("Restore File to Previous Version")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    restore_file_to_previous_version(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git log --oneline -- filename       - View file's commit history
2. git show HEAD~2:filename            - View file content at specific commit
3. git checkout HEAD~2 -- filename     - Restore file to version from N commits ago
4. git add filename                    - Stage the restored file
5. git commit -m "message"           - Commit the restoration

Alternative Methods:
    git restore --source=HEAD~2 filename    # Git 2.23+
    git reset HEAD~2 -- filename            # Reset file from specific commit

Important Notes:
- This only affects the specified file, not other files
- The file gets restored to the exact state at that commit
- A new commit is created to track the restoration
- Original buggy commits remain in history
""")


if __name__ == "__main__":
    main()