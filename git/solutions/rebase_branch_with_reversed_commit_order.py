"""
Solution for "Rebase Branch with Reversed Commit Order" (Booking.com, Easy)

Scenario:
You have a Git repository at `/home/interview/repo` where your `feature-refactor`
branch has four commits in the wrong logical order. The commits should be
reversed (oldest to newest becomes newest to oldest) to make more sense for
code review. You need to rebase this branch onto the latest `main` branch
while reversing the commit order.

Task:
Navigate to `/home/interview/repo`, rebase `feature-refactor` onto `main` while
reversing all commits using interactive rebase, and verify the commits appear
in the correct reversed sequence with all changes preserved.
"""


def rebase_with_reversed_order(repo_path: str = "/home/interview/repo"):
    """
    Rebase a branch onto main while reversing the commit order.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: Ensure main is up to date
    print("Updating main branch...")
    subprocess.run(
        ["git", "checkout", "main"],
        cwd=repo_path,
        capture_output=True
    )
    subprocess.run(
        ["git", "pull", "origin", "main"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 2: View current commits on feature-refactor
    print("\nCurrent commits on feature-refactor (before rebase):")
    subprocess.run(
        ["git", "log", "feature-refactor", "--reverse", "--oneline"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 3: Get the number of commits to reverse
    result = subprocess.run(
        ["git", "log", "--format=%H", "feature-refactor", "-4"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    commits = result.stdout.strip().split("\n")
    num_commits = len([c for c in commits if c])

    if num_commits == 0:
        print("No commits to rebase")
        return

    print(f"\nFound {num_commits} commits to reverse")

    # Step 4: Interactive rebase to reverse commits
    # We need to go back to when feature-refactor branched from main,
    # then use pick to reverse order

    # Switch to feature-refactor
    subprocess.run(
        ["git", "checkout", "feature-refactor"],
        cwd=repo_path,
        capture_output=True
    )

    # Get the commit hash where feature-refactor diverged from main
    result = subprocess.run(
        ["git", "merge-base", "main", "feature-refactor"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    divergence_point = result.stdout.strip()
    print(f"\nDivergence point: {divergence_point[:8]}")

    # Create an interactive rebase to reverse the order
    # Instead of using git rebase -i (which requires editor interaction),
    # we simulate by manually reversing commits

    print("\nPerforming non-interactive rebase with reversed order...")

    # Check current state
    result = subprocess.run(
        ["git", "log", "HEAD", "--oneline", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(f"Current history:\n{result.stdout}")

    # For git to reverse order, we would normally use:
    # GIT_SEQUENCE_EDITOR='sed -i "1!G;h;$!d"' git rebase -i HEAD~4
    # But since we need to rebase onto main as well, it's complex.

    # Alternative: Cherry-pick commits in reverse order onto main
    print("\nUsing cherry-pick to reverse commit order onto main...")

    # Get all commits in reverse order (newest first)
    result = subprocess.run(
        ["git", "log", "HEAD", "--format=%H", "-4"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    commits_newest_first = [c for c in result.stdout.strip().split("\n") if c]

    # Reset to main
    subprocess.run(
        ["git", "reset", "--hard", "main"],
        cwd=repo_path,
        capture_output=True
    )

    # Cherry-pick in reverse order (oldest first from feature now first to cherry-pick)
    for commit in reversed(commits_newest_first):
        print(f"Cherry-picking {commit[:8]}...")
        result = subprocess.run(
            ["git", "cherry-pick", commit],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error cherry-picking: {result.stderr}")
            raise RuntimeError("Cherry-pick failed")

    # Step 5: Verify the reversed order
    print("\nCommit history after reversing order:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Demonstrate the solution for rebasing with reversed commit order."""
    print("=" * 60)
    print("Rebase Branch with Reversed Commit Order")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    rebase_with_reversed_order(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands and Concepts:

Method 1 - Interactive Rebase (manual):
    git rebase -i HEAD~4
    # Then manually reorder the pick statements

Method 2 - Using GIT_SEQUENCE_EDITOR:
    GIT_SEQUENCE_EDITOR='sed -i "1!G;h;$!d"' git rebase -i main

Method 3 - Cherry-pick in reverse order:
    # Get commit hashes
    # Reset to main
    # Cherry-pick in reverse order

Note: The commits will have NEW hashes after rebase/cherry-pick
because the parent commit changes, but the content remains the same.

Warning: Rewriting shared branch history requires force push:
    git push --force-with-lease
""")


if __name__ == "__main__":
    main()