"""
Solution for "Update Submodule to Latest Commit" (GoDaddy, Medium)

Scenario:
You have a Git repository at `/home/interview/repo` that contains a **submodule
in the `vendor/utils` directory**. The submodule is pointing to an old commit,
but **newer commits exist on the submodule's remote repository**.

Task:
Update the submodule to the latest commit on its default branch and commit
this change in the parent repository.
"""


def update_submodule_to_latest(repo_path: str = "/home/interview/repo", submodule_path: str = "vendor/utils"):
    """
    Update a Git submodule to the latest commit.

    Args:
        repo_path: Path to the parent Git repository
        submodule_path: Path to the submodule directory
    """
    import subprocess
    import os

    submodule_full_path = os.path.join(repo_path, submodule_path)

    # Step 1: Check current submodule status
    print("Current submodule configuration:")
    result = subprocess.run(
        ["git", "submodule", "status", submodule_path],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(submodule not initialized)")

    # Step 2: Check current commit in submodule
    print(f"\n{submodule_path} current state:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=submodule_full_path,
        capture_output=True,
        text=True
    )
    print(f"Current submodule commit: {result.stdout if result.stdout else '(no commits)'}")

    # Step 3: Fetch latest from submodule's remote
    print("\nFetching latest from submodule's remote...")
    result = subprocess.run(
        ["git", "fetch", "origin"],
        cwd=submodule_full_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Step 4: Check what the latest commit is
    print("\nSubmodule remote has these branches:")
    result = subprocess.run(
        ["git", "branch", "-r"],
        cwd=submodule_full_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")

    # Step 5: Get the latest commit on default branch
    print("\nFinding latest commit on default branch...")
    result = subprocess.run(
        ["git", "log", "origin/main", "--oneline", "-1"],
        cwd=submodule_full_path,
        capture_output=True,
        text=True
    )
    default_branch_commit = result.stdout.strip() if result.stdout else result.stderr.strip()

    # Try origin/master if main doesn't exist
    if not default_branch_commit or "unknown" in default_branch_commit.lower():
        result = subprocess.run(
            ["git", "log", "origin/master", "--oneline", "-1"],
            cwd=submodule_full_path,
            capture_output=True,
            text=True
        )
        default_branch_commit = result.stdout.strip()

    print(f"Latest commit on submodule's default branch: {default_branch_commit}")

    # Step 6: Update submodule to latest commit
    # Use git submodule update with --remote to fetch latest
    # Or use git checkout to switch to the latest commit

    print("\nUpdating submodule to latest commit...")
    result = subprocess.run(
        ["git", "submodule", "update", "--remote", "--init", submodule_path],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "")
    if result.stderr:
        print(result.stderr)

    # Alternative: git checkout in the submodule
    # submodule.run(["git", "checkout", "origin/main"], cwd=submodule_full_path)

    # Step 7: Check the new commit
    print("\nSubmodule state after update:")
    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        cwd=submodule_full_path,
        capture_output=True,
        text=True
    )
    print(f"New submodule commit: {result.stdout}")

    # Step 8: Commit the submodule update in parent repo
    print("\nStaging submodule change in parent repository...")
    subprocess.run(
        ["git", "add", submodule_path],
        cwd=repo_path,
        capture_output=True
    )

    # Check if there are changes to commit
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(f"Git status:\n{result.stdout}")

    if "new commits" in result.stdout or "modified:" in result.stdout:
        print("\nCommitting submodule update...")
        result = subprocess.run(
            ["git", "commit", "-m", f"Update {submodule_path} submodule to latest"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Submodule update committed!")
        else:
            print(f"Commit error: {result.stderr}")
    else:
        print("No submodule changes to commit")


def main():
    """Demonstrate the solution for updating a Git submodule."""
    print("=" * 60)
    print("Update Submodule to Latest Commit")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    submodule_path = "vendor/utils"

    update_submodule_to_latest(repo_path, submodule_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git submodule status             - Check submodule current commit
2. git submodule update --remote --init <path>  - Update to latest
3. git checkout origin/main         - Switch submodule to latest
4. git add <submodule-path>        - Stage submodule change
5. git commit -m "Update submodule" - Commit in parent repo

Submodule Workflow:
1. Clone parent repo (submodules are empty initially)
2. git submodule init              - Initialize submodule config
3. git submodule update            - Checkout submodule files
4. Make changes in submodule
5. Commit in submodule
6. Commit in parent repo (records new submodule commit)

Challenges with Submodules:
- Easy to forget --recursive in clone
- Updates require two commits (submodule + parent)
- Can become detached HEAD in submodules
- Merging can be complex

For Git 2.9+:
    git submodule update --remote    # Fetches and checks out latest
    git submodule update --remote --merge  # Merges remote changes
""")


if __name__ == "__main__":
    main()