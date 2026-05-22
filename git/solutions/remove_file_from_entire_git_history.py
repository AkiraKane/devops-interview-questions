"""
Solution for "Remove File from Entire Git History" (Netflix, Medium)

Scenario:
A file named `secrets.env` containing sensitive credentials exists in the
repository's commit history. You need to purge this file from the entire history.

Task:
Navigate to `/home/interview/repo` and rewrite the commit history to
permanently remove `secrets.env` from all commits.
"""


def remove_file_from_history(repo_path: str = "/home/interview/repo", filename: str = "secrets.env"):
    """
    Remove a file from entire Git history using git filter-branch or BFG.

    Args:
        repo_path: Path to the Git repository
        filename: The file to remove from history
    """
    import subprocess

    # Step 1: Verify the file exists in history
    print(f"Searching for {filename} in git history...")
    result = subprocess.run(
        ["git", "log", "--all", "--oneline", "--", filename],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(f"Commits containing {filename}:")
    print(result.stdout if result.stdout else "(file not found in history)")

    # Step 2: Filter the history to remove the file
    # Using git filter-branch (slower but built-in)
    print(f"\nRemoving {filename} from entire history using git filter-branch...")
    print("This may take time for large repositories...")

    # Method 1: Using git filter-branch
    # --tree-filter applies command after checking out each commit
    result = subprocess.run(
        ["git", "filter-branch", "--force", "--index-filter",
         f"git rm --cached --ignore-unmatch {filename}", "--prune-empty", "--tag-name-filter", "cat",
         "--", "--all"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode == 0:
        print(f"Successfully removed {filename} from history!")
        print("\nVerifying the file is removed from history:")

        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "--", filename],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        print(result.stdout if result.stdout else "(file successfully removed)")

        # Step 3: Verify garbage collection
        print("\nCleaning up...")
        subprocess.run(
            ["git", "reflog", "expire", "--expire=now", "--all"],
            cwd=repo_path,
            capture_output=True
        )
        subprocess.run(
            ["git", "gc", "--prune=now", "--aggressive"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
    else:
        print(f"filter-branch output: {result.stdout}")
        print(f"filter-branch error: {result.stderr}")


def remove_file_using_bfg(repo_path: str = "/home/interview/repo", filename: str = "secrets.env"):
    """
    Remove a file using BFG Repo-Cleaner (faster alternative).

    Note: BFG must be installed separately (brew install bfg)

    Args:
        repo_path: Path to the Git repository
        filename: The file to remove from history
    """
    import subprocess

    print(f"\nAlternative: Using BFG Repo-Cleaner (faster)...")

    # Create a backup notice
    print("IMPORTANT: Create a backup before using BFG!")
    print("  cp -r repo repo-backup")

    # Run BFG to remove the file
    # --no-blob-protection allows removing files in recent commits
    # --delete-files removes all instances of the filename
    result = subprocess.run(
        ["bfg", "--delete-files", filename, "--no-blob-protection"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("BFG completed. Now pruning...")
        subprocess.run(
            ["git", "reflog", "expire", "--expire=now", "--all"],
            cwd=repo_path,
            capture_output=True
        )
        subprocess.run(
            ["git", "gc", "--prune=now", "--aggressive"],
            cwd=repo_path,
            capture_output=True
        )
    else:
        print(f"BFG not installed or error: {result.stderr}")


def main():
    """Demonstrate the solution for removing a file from git history."""
    print("=" * 60)
    print("Remove File from Entire Git History")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    filename = "secrets.env"

    remove_file_from_history(repo_path, filename)
    remove_file_using_bfg(repo_path, filename)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:

Method 1: git filter-branch (built-in, slow)
    git filter-branch --force --index-filter \\
        "git rm --cached --ignore-unmatch secrets.env" \\
        --prune-empty --tag-name-filter cat -- --all

Method 2: BFG Repo-Cleaner (faster, separate install)
    # Install: brew install bfg
    # Run from repo root:
    bfg --delete-files secrets.env
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive

Important Notes:
1. ALWAYS create a backup before rewriting history
2. Git rewrite may fail if hooks block it (--force flag may help)
3. After rewrite, you MUST force push:
       git push --force --all
4. Collaborators must re-clone the repository
5. Consider using .gitignore to prevent re-addition

Prevention:
- Use .gitignore before adding files
- Use git secrets scanning tools in CI
- Never commit credentials to version control
""")


if __name__ == "__main__":
    main()