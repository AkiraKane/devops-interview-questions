"""
Solution for "Create an Annotated Tag" (Nintendo, Medium)

Scenario:
You have a Git repository at `/home/interview/repo` where you've just completed
version 3.1.0 of your application. You need to **create an annotated tag** to
mark this release with a proper message and metadata.

Task:
Create an annotated tag for version v3.1.0 with a descriptive message and push
it to the remote `origin` repository v3.1.0
"""


def create_annotated_tag(repo_path: str = "/home/interview/repo", version: str = "v3.1.0"):
    """
    Create and push an annotated tag for a release version.

    Args:
        repo_path: Path to the Git repository
        version: The version tag to create
    """
    import subprocess

    # Step 1: Verify we're on main and have a clean state
    print("Checking repository status...")
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        print("Warning: Working directory is not clean. Commit or stash changes first.")

    # Step 2: Get the current commit hash to tag
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    commit_hash = result.stdout.strip()
    print(f"Current commit: {commit_hash[:8]}")

    # Step 3: Create an annotated tag with a message
    # -a flag creates an annotated tag
    # -m flag provides the tag message
    tag_message = f"Release version {version} - Production deployment"

    print(f"\nCreating annotated tag: {version}")
    print(f"Tag message: {tag_message}")

    result = subprocess.run(
        ["git", "tag", "-a", version, "-m", tag_message],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Tag {version} created successfully!")
    else:
        print(f"Error creating tag: {result.stderr}")
        raise RuntimeError("Failed to create tag")

    # Step 4: Verify the tag was created
    print("\nVerifying tag:")
    result = subprocess.run(
        ["git", "tag", "-l", "-n", "1", version],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 5: Push the tag to remote
    print(f"\nPushing tag {version} to origin...")
    result = subprocess.run(
        ["git", "push", "origin", version],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Tag {version} pushed to origin successfully!")
    else:
        print(f"Error pushing tag: {result.stderr}")
        raise RuntimeError("Failed to push tag")

    # Step 6: Verify remote tag
    print("\nVerifying remote tag exists:")
    result = subprocess.run(
        ["git", "ls-remote", "--tags", "origin"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)


def main():
    """Demonstrate the solution for creating an annotated tag."""
    print("=" * 60)
    print("Create an Annotated Tag")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    create_annotated_tag(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git tag -a v3.1.0 -m "Release message"    - Create annotated tag
2. git tag -n -1 v3.1.0                       - Show tag details
3. git push origin v3.1.0                     - Push tag to remote
4. git push origin --tags                      - Push all tags

Annotated vs Lightweight Tags:
- Annotated: Contains full tag message, tagger info, date, GPG signature
- Lightweight: Just a pointer to a specific commit

Best Practices:
- Use annotated tags for releases (they include metadata)
- Use lightweight tags for local bookmarks
- Always push tags explicitly (tags are not pushed by default with git push)
""")


if __name__ == "__main__":
    main()