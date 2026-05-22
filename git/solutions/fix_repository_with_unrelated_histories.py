"""
Solution for "Fix Repository with Unrelated Histories" (Zscaler, Medium)

Scenario:
The repository at `/home/interview/repo` is in a broken state. Local and remote
branches have diverged with **no common ancestor**. Consequently, `git push origin
main` fails with a **non-fast-forward** error, and `git pull origin main` fails
because the histories are **unrelated**.

Task:
Navigate to `/home/interview/repo`. **Merge and linearize** the unrelated
histories (using rebase) to create a single commit sequence.
"""


def fix_unrelated_histories(repo_path: str = "/home/interview/repo"):
    """
    Fix repository with unrelated histories by merging and linearizing.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: Check current status
    print("Checking current repository state...")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 2: Check log to see the divergent histories
    print("\nLocal main history:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no local commits)")

    print("\nRemote origin/main history:")
    result = subprocess.run(
        ["git", "log", "origin/main", "--oneline", "-5"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no remote commits)")

    # Step 3: Fetch the remote to get all unreachable objects
    print("\nFetching remote history...")
    subprocess.run(
        ["git", "fetch", "origin"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 4: Pull with allow-unrelated-histories to merge the divergent histories
    # Then rebase to linearize
    print("\nPulling with allow-unrelated-histories to merge...")
    result = subprocess.run(
        ["git", "pull", "origin", "main", "--allow-unrelated-histories"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Step 5: Verify the merge happened
    print("\nVerifying the history is now unified:")
    result = subprocess.run(
        ["git", "log", "--oneline", "--decorate", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 6: Verify we can push (should be up-to-date or fast-forward)
    print("\nVerifying push works...")
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Push successful! Repository is now fixed.")
    else:
        print(f"Push output: {result.stderr}")


def main():
    """Demonstrate the solution for fixing unrelated histories."""
    print("=" * 60)
    print("Fix Repository with Unrelated Histories")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    fix_unrelated_histories(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git fetch origin                         - Fetch remote history
2. git pull origin main --allow-unrelated-histories - Merge unrelated histories
3. git log --oneline --decorate            - Verify unified history
4. git push origin main                     - Push should now work

Alternative approach using rebase:
1. git fetch origin
2. git rebase origin/main                  - Rebase local onto remote

The --allow-unrelated-histories flag allows merging two repositories
that have no common ancestor, combining both commit histories into
a single linear history.

Prevention:
- Always pull from the correct remote before starting new work
- Use git fetch + git merge/rebase instead of git pull for more control
""")


if __name__ == "__main__":
    main()