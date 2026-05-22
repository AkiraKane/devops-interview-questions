"""
Solution for "View Unique Commits Between Branch and Origin" (EPAM, Easy)

Scenario:
A Git repository at `/home/interview/repo` has a `feature-api` branch that was
created from `origin/main` some time ago. The branch has your commits plus
merge commits from pulling updates, making it difficult to identify which
commits are unique to your branch.

Task:
Find commits unique to your branch compared to `origin/main`, exclude merge
commits, write the unique commits to `/home/interview/unique-commits.txt`,
and verify the file contains only the unique commits.
"""


def find_unique_commits(
    repo_path: str = "/home/interview/repo",
    branch: str = "feature-api",
    output_file: str = "/home/interview/unique-commits.txt"
):
    """
    Find commits unique to a branch compared to origin/main.

    Args:
        repo_path: Path to the Git repository
        branch: The branch to find unique commits for
        output_file: Path to write unique commits to
    """
    import subprocess

    # Step 1: Ensure origin/main is up to date
    print("Fetching latest origin/main...")
    subprocess.run(
        ["git", "fetch", "origin"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 2: Show commits unique to feature-api compared to origin/main
    # origin/main..branch means commits in branch but not in origin/main
    print(f"\nFinding commits unique to {branch} (not in origin/main)...")

    result = subprocess.run(
        ["git", "log", f"origin/main..{branch}", "--oneline"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    all_unique_commits = result.stdout
    print(f"All unique commits:\n{all_unique_commits}")

    # Step 3: Remove merge commits from the list
    # Merge commits have multiple parents (identified by merge commit message or ^2)
    print("\nFiltering out merge commits...")

    # Method: Use --no-merges flag to exclude merge commits
    result = subprocess.run(
        ["git", "log", f"origin/main..{branch}", "--oneline", "--no-merges"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    unique_non_merge_commits = result.stdout

    print(f"Unique commits (excluding merges):\n{unique_non_merge_commits}")

    # Step 4: Write commits to file
    print(f"\nWriting unique commits to {output_file}...")

    # Only the commit hashes and messages (no prefix or additional info)
    result = subprocess.run(
        ["git", "log", f"origin/main..{branch}", "--format=%H %s", "--no-merges"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    commit_output = result.stdout

    with open(output_file, "w") as f:
        f.write(commit_output)

    print(f"Written {len(commit_output.strip().split(chr(10)))} commits to {output_file}")

    # Step 5: Verify the file content
    print("\nVerifying file content:")
    with open(output_file, "r") as f:
        print(f.read())

    # Step 6: Show summary statistics
    result = subprocess.run(
        ["git", "log", f"origin/main..{branch}", "--oneline", "--no-merges", "--count"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    count = result.stdout.strip()
    print(f"\nTotal unique non-merge commits: {count}")


def main():
    """Demonstrate the solution for finding unique commits between branches."""
    print("=" * 60)
    print("View Unique Commits Between Branch and Origin")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    branch = "feature-api"
    output_file = "/home/interview/unique-commits.txt"

    find_unique_commits(repo_path, branch, output_file)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git log origin/main..feature-api      - Show commits in feature-api not in origin/main
2. git log origin/main..HEAD --no-merges - Exclude merge commits
3. git log --format="%H %s"              - Custom output format
4. git log --count                       - Count commits

Git Log Range Syntax:
    A..B    = Commits reachable from B but not A
    A...B   = Commits reachable from either A or B but not both (symmetric diff)

Common Patterns:
    git log main..feature                 - Feature branch commits
    git log origin/main..HEAD             - Local commits not pushed
    git log --first-parent                - Only first parent (not merged commits)

Merge Commits:
- Created when combining branches
- Have 2+ parent commits
- --no-merges excludes these
- Use ^2 or --second-parent to identify second parent in some tools

Saving to File:
    git log origin/main..feature-api --format="%H" > commits.txt
    git log origin/main..feature-api --oneline --no-merges > commits.txt
""")


if __name__ == "__main__":
    main()