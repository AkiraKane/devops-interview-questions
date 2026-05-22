"""
Solution for "Rebase Feature Branch Onto Correct Base" (Samsung, Easy)

Scenario:
A Git repository at `/home/interview/repo` has a feature branch `feature-login`
with several commits, but it was created from the wrong base branch.

Task:
Rebase `feature-login` onto `develop` (it's currently based on `main`)
while preserving all commits.
"""


def rebase_onto_correct_base(repo_path: str = "/home/interview/repo"):
    """
    Rebase a feature branch from main onto develop.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: Check current branch state
    print("Current branch state:")

    print("\nBranches:")
    result = subprocess.run(
        ["git", "branch", "-v"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    print("\nfeature-login current history:")
    result = subprocess.run(
        ["git", "log", "feature-login", "--oneline", "-5"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no commits)")

    print("\ndevelop current history:")
    result = subprocess.run(
        ["git", "log", "develop", "--oneline", "-5"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(branch may not exist)")

    # Step 2: Switch to feature-login
    print("\nSwitching to feature-login...")
    subprocess.run(
        ["git", "checkout", "feature-login"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 3: Verify develop exists, create if needed
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "develop"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("develop branch doesn't exist, can't proceed with rebase")
        return

    # Step 4: Rebase feature-login onto develop
    # This moves the branch from main as base to develop as base
    print("\nRebasing feature-login onto develop...")
    result = subprocess.run(
        ["git", "rebase", "develop"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Step 5: Verify the rebase
    print("\nfeature-login history after rebase:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-10"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 6: Show the git graph to visualize
    print("\nVisualizing branch structure:")
    result = subprocess.run(
        ["git", "log", "--graph", "--oneline", "--all", "-15"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Demonstrate the solution for rebasing onto correct base branch."""
    print("=" * 60)
    print("Rebase Feature Branch Onto Correct Base")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    rebase_onto_correct_base(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Command:
    git rebase develop

When you run this from feature-login, Git will:
1. Find where feature-login diverged from its current base (main)
2. Replay feature-login commits onto develop
3. Update feature-login pointer to the new HEAD

Before rebase:
    main:      A--B--C
                        \\--D--E (feature-login)

After rebase (git checkout feature-login && git rebase develop):
    main:      A--B--C
    develop:   A--B--C--X--Y
                        \\--D'--E' (feature-login)

All commits are preserved with new hashes.

Alternative: git rebase --onto
    git rebase --onto <new-base> <old-base> <branch>
    git rebase --onto develop main feature-login
""")


if __name__ == "__main__":
    main()