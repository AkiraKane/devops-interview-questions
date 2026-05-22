"""
Solution for "Merge Feature Branch and Delete" (Expedia, Easy)

Scenario:
You have a Git repository at `/home/interview/repo` where you've completed work
on the `feature-login` branch. The feature is ready to be integrated into the
`main` branch.

Task:
Merge feature-login into main and delete the feature branch in `/home/interview/repo`.
"""


def merge_and_delete_branch(repo_path: str = "/home/interview/repo"):
    """
    Merge a feature branch into main and delete the feature branch.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: Check current branches
    print("Current branches:")
    result = subprocess.run(
        ["git", "branch"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 2: View the feature branch commit
    print("Feature-login last commit:")
    result = subprocess.run(
        ["git", "log", "feature-login", "--oneline", "-1"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 3: Switch to main branch
    print("\nSwitching to main branch...")
    subprocess.run(
        ["git", "checkout", "main"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 4: Merge feature-login into main
    print("Merging feature-login into main...")
    result = subprocess.run(
        ["git", "merge", "feature-login"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Step 5: Verify the merge
    print("\nMain branch after merge:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 6: Delete the feature branch (locally)
    print("\nDeleting feature-login branch...")
    result = subprocess.run(
        ["git", "branch", "-d", "feature-login"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Feature branch deleted successfully!")
    else:
        print(f"Error: {result.stderr}")

    # Step 7: Verify branches
    print("\nRemaining branches:")
    result = subprocess.run(
        ["git", "branch"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Demonstrate the solution for merging and deleting a feature branch."""
    print("=" * 60)
    print("Merge Feature Branch and Delete")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    merge_and_delete_branch(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git checkout main                        - Switch to target branch
2. git merge feature-login                  - Merge feature into main
3. git branch -d feature-login             - Delete local branch (safe)
4. git branch -D feature-login             - Force delete if not merged

Git branch flags:
- -d: Safe delete (only if merged)
- -D: Force delete (works even if not merged)
- -r: List remote branches
- -a: List all branches

After merging, you can also push main to origin:
    git push origin main
""")


if __name__ == "__main__":
    main()