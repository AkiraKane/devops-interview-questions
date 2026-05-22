"""
Solution for "Shallow Clone Limited to Latest Commit" (Elastic, Easy)

Scenario:
A deployment pipeline is experiencing slow build times because it performs
full history clones.

Task:
Navigate to `/home/interview/workspace` and create a shallow clone of the
repository (`file:///tmp/source-repo/repo.git`) named `shallow-repo`, restricted
to the latest commit only.
"""


def shallow_clone(
    source_repo: str = "file:///tmp/source-repo/repo.git",
    workspace: str = "/home/interview/workspace",
    clone_name: str = "shallow-repo"
):
    """
    Create a shallow clone with only the latest commit.

    Args:
        source_repo: URL/path to the source repository
        workspace: Directory to create the clone in
        clone_name: Name of the clone directory
    """
    import subprocess
    import os

    # Step 1: Ensure workspace exists
    os.makedirs(workspace, exist_ok=True)

    # Step 2: Define the clone path
    clone_path = os.path.join(workspace, clone_name)

    # Step 3: Remove existing clone if present
    if os.path.exists(clone_path):
        print(f"Removing existing {clone_name}...")
        subprocess.run(["rm", "-rf", clone_path])

    # Step 4: Create shallow clone with --depth 1
    # --depth 1 limits history to only the latest commit
    # Clone into the specified directory
    print(f"Creating shallow clone at {clone_path}...")
    print(f"Source: {source_repo}")

    result = subprocess.run(
        ["git", "clone", "--depth", "1", source_repo, clone_path],
        cwd=workspace,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Shallow clone created successfully!")
    else:
        print(f"Clone output: {result.stdout}")
        print(f"Clone error: {result.stderr}")
        raise RuntimeError("Failed to create shallow clone")

    # Step 5: Verify the clone is shallow
    print("\nVerifying shallow clone...")

    # Check commit count
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=clone_path,
        capture_output=True,
        text=True
    )
    commit_count = result.stdout.strip()
    print(f"Number of commits in clone: {commit_count}")

    # Show the log
    print("\nCommit history (should be only 1 commit):")
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=clone_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no commits)")

    # Show remote and branch info
    print("Clone info:")
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=clone_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no remote)")

    result = subprocess.run(
        ["git", "branch", "-a"],
        cwd=clone_path,
        capture_output=True,
        text=True
    )
    print(f"Branches: {result.stdout.strip()}")


def main():
    """Demonstrate the solution for creating a shallow clone."""
    print("=" * 60)
    print("Shallow Clone Limited to Latest Commit")
    print("=" * 60)

    source_repo = "file:///tmp/source-repo/repo.git"
    workspace = "/home/interview/workspace"
    clone_name = "shallow-repo"

    shallow_clone(source_repo, workspace, clone_name)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Command:
    git clone --depth 1 <repository> <directory>

What --depth 1 Does:
- Only downloads the latest commit
- Does not download full history (all parent commits)
- Creates a shallow repository with truncated history
- Reduces clone size and time significantly

Shallow Clone Limitations:
- Cannot push back to original repo without unshallowing
- Cannot see full history
- Some Git operations may not work correctly

Convert Shallow to Full (Unshallow):
    git fetch --unshallow    # Converts to full repository

Alternative Flags:
    --depth 10              - Shallow clone with 10 commits of history
    --no-single-branch      - Clone all branches (not just current)
    --single-branch         - Clone only current branch (default with --depth)

For CI/CD Pipelines:
- Use shallow clones for faster deployment
- Use --no-tags to avoid downloading tag objects
- Use --filter=blob:none for partial clone (Git 2.19+)
""")


if __name__ == "__main__":
    main()