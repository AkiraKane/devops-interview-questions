"""
Solution for "Checkout Single File from Another Branch" (Twilio, Easy)

Scenario:
You are working on the `main` branch and need to update `config.json` with changes
that currently exist only on the `feature-settings` branch, without switching
your current context.

Task:
Navigate to `/home/interview/repo` and retrieve the `config.json` file from the
`feature-settings` branch into your current working directory.
"""


def checkout_single_file(repo_path: str = "/home/interview/repo"):
    """
    Checkout a single file from another branch without switching branches.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    current_branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
        capture_output=True,
        text=True
    ).stdout.strip()
    print(f"Current branch: {current_branch}")

    # The command to retrieve a file from another branch:
    # git checkout <branch> -- <file>
    # This does NOT switch your current branch, it just updates the file

    print("\nChecking out config.json from feature-settings branch...")
    result = subprocess.run(
        ["git", "checkout", "feature-settings", "--", "config.json"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Successfully retrieved config.json from feature-settings!")

        # Verify the file content and branch status
        result = subprocess.run(
            ["cat", f"{repo_path}/config.json"],
            capture_output=True,
            text=True
        )
        print(f"\nconfig.json content:\n{result.stdout}")

        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()
        print(f"Current branch still: {current_branch}")
    else:
        print(f"Error: {result.stderr}")
        raise RuntimeError("Failed to checkout file")


def main():
    """Demonstrate the solution for checking out a single file from another branch."""
    print("=" * 60)
    print("Checkout Single File from Another Branch")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    checkout_single_file(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Command:
    git checkout <source-branch> -- <file>

This command:
- Retrieves the file from the specified branch
- Does NOT switch your current branch
- Updates only the specified file in your working directory

Alternative syntax (Git 2.23+):
    git restore --source=<branch> <file>
    git restore -s <branch> <file>

This is useful when you need changes from another branch but don't
want to disrupt your current working context.
""")


if __name__ == "__main__":
    main()