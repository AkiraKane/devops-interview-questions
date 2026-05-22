"""
Solution for "Apply Specific Stash from Multiple Stashes" (UBS, Easy)

Scenario:
You have multiple work-in-progress states saved in your Git stash stack and need
to retrieve code from an older snapshot.

Task:
Navigate to `/home/interview/repo`. Identify the **third stash** in the list,
preview its contents, and apply it to your current working directory **without
removing it** from the stack.
"""


def apply_specific_stash(repo_path: str = "/home/interview/repo"):
    """
    Apply the third stash (stash@{2}) without removing it from the stack.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: List all stashes to identify the third one
    result = subprocess.run(
        ["git", "stash", "list"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    stashes = result.stdout.strip().split("\n")
    print("Available stashes:")
    for i, stash in enumerate(stashes):
        print(f"  {stash}")

    # Step 2: Preview the third stash (stash@{2}) contents
    print("\nPreviewing third stash (stash@{2}):")
    result = subprocess.run(
        ["git", "stash", "show", "-p", "stash@{2}"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(empty stash)")

    # Step 3: Apply the third stash without removing it (use --index to restore staged state)
    print("\nApplying third stash (stash@{2})...")
    result = subprocess.run(
        ["git", "stash", "apply", "stash@{2}"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Successfully applied third stash!")
        # Verify stash is still in the list
        result = subprocess.run(
            ["git", "stash", "list"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        print(f"\nStash list after apply (stash still present):\n{result.stdout}")
    else:
        print(f"Error: {result.stderr}")
        raise RuntimeError("Failed to apply stash")


def main():
    """Demonstrate the solution for applying a specific stash."""
    print("=" * 60)
    print("Apply Specific Stash from Multiple Stashes")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    apply_specific_stash(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git stash list              - View all stashes in the stack
2. git stash show -p stash@{2} - Preview the third stash contents
3. git stash apply stash@{2}   - Apply the third stash without removing it

Unlike 'git stash pop' which removes the stash after applying,
'git stash apply' leaves the stash in the stack so it can be
reused multiple times.
""")


if __name__ == "__main__":
    main()