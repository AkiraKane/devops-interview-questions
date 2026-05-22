"""
Solution for "Stash Work Fix Bug Restore and Update" (IBM, Medium)

Scenario:
Uncommitted changes on `feature-ui` prevent you from switching branches to fix
a critical bug on `main`.

Task:
Stash local changes to clean the working directory with message `WIP: UI
improvements`. Switch to a new branch `hotfix-auth` to implement the fix, then
merge it into `main`. Finally, rebase `feature-ui` against the updated `main`
and restore your stashed changes.

Changes in hotfix-auth branch are below:
    echo "Fixing critical bug" >> src/auth.js
    git commit -m "Fix critical authentication bug"
"""


def stash_work_fix_bug_restore_update(repo_path: str = "/home/interview/repo"):
    """
    Stash work, create hotfix branch, merge to main, rebase feature, restore stash.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: Check current status
    print("Initial git status:")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 2: Stash local changes with message "WIP: UI improvements"
    print("\nStashing changes with message 'WIP: UI improvements'...")
    result = subprocess.run(
        ["git", "stash", "push", "-m", "WIP: UI improvements"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Changes stashed successfully!")
    else:
        print(f"Stash output: {result.stdout}")
        print(f"Stash error: {result.stderr}")
        raise RuntimeError("Failed to stash changes")

    # Verify stash list
    result = subprocess.run(
        ["git", "stash", "list"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(f"Stash list:\n{result.stdout}")

    # Step 3: Switch to main and pull latest
    print("\nSwitching to main and pulling latest...")
    subprocess.run(["git", "checkout", "main"], cwd=repo_path, capture_output=True)
    subprocess.run(["git", "pull", "origin", "main"], cwd=repo_path, capture_output=True)

    # Step 4: Create hotfix-auth branch
    print("\nCreating hotfix-auth branch...")
    subprocess.run(
        ["git", "checkout", "-b", "hotfix-auth"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 5: Apply the bug fix changes
    print("\nApplying bug fix to src/auth.js...")
    with open(f"{repo_path}/src/auth.js", "a") as f:
        f.write("\n// Fixing critical bug\n")

    subprocess.run(
        ["git", "add", "src/auth.js"],
        cwd=repo_path,
        capture_output=True
    )

    print("\nCommitting fix...")
    result = subprocess.run(
        ["git", "commit", "-m", "Fix critical authentication bug"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(f"Commit output: {result.stdout}")

    # Step 6: Merge hotfix-auth into main
    print("\nMerging hotfix-auth into main...")
    subprocess.run(["git", "checkout", "main"], cwd=repo_path, capture_output=True)
    result = subprocess.run(
        ["git", "merge", "hotfix-auth", "--no-ff", "-m", "Merge hotfix-auth"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Step 7: Rebase feature-ui against updated main
    print("\nSwitching to feature-ui and rebasing onto updated main...")
    subprocess.run(["git", "checkout", "feature-ui"], cwd=repo_path, capture_output=True)

    result = subprocess.run(
        ["git", "rebase", "main"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Step 8: Restore stashed changes
    print("\nRestoring stashed changes...")
    result = subprocess.run(
        ["git", "stash", "pop"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Stashed changes restored successfully!")
    else:
        print(f"Restore error: {result.stderr}")

    # Step 9: Verify final state
    print("\nFinal git status:")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    print("\nMain branch history:")
    result = subprocess.run(
        ["git", "log", "main", "--oneline", "-3"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Demonstrate the solution for stashing work, fixing bug, and restoring."""
    print("=" * 60)
    print("Stash Work Fix Bug Restore and Update")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    stash_work_fix_bug_restore_update(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git stash push -m "message"     - Stash with custom message
2. git stash list                    - View stash stack
3. git stash pop                    - Apply stash and remove from stack
4. git stash apply                  - Apply stash without removing
5. git checkout -b hotfix-auth      - Create and switch to new branch
6. git merge --no-ff                - Merge with merge commit
7. git rebase main                  - Rebase onto updated main
8. git stash pop                    - Restore changes

Workflow:
1. Stash WIP changes (clears working directory)
2. Create and switch to hotfix branch
3. Make the bug fix commit
4. Merge hotfix into main
5. Switch to feature branch
6. Rebase feature onto updated main
7. Restore stashed work
8. Continue working on feature

Benefits:
- Clean working directory to switch branches
- Hotfix doesn't block feature development
- Feature rebased on latest main integration
""")


if __name__ == "__main__":
    main()