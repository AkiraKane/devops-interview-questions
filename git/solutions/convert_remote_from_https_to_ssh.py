"""
Solution for "Convert Remote from HTTPS to SSH" (EPAM, Easy)

Scenario:
You have a Git repository at `/home/interview/repo` where the remote **origin is
currently configured with an HTTPS URL** (`https://github.com/user/repo.git`).

Task:
Change the remote URL from HTTPS to SSH and verify the connection.
"""


def convert_remote_url(repo_path: str = "/home/interview/repo"):
    """
    Convert the origin remote URL from HTTPS to SSH.

    Args:
        repo_path: Path to the Git repository
    """
    import subprocess

    # Step 1: View current remote configuration
    print("Current remote configuration:")
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(no remotes configured)")

    # Step 2: Get the current HTTPS URL
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    current_url = result.stdout.strip()
    print(f"\nCurrent origin URL: {current_url}")

    # Step 3: Convert HTTPS to SSH
    # HTTPS:  https://github.com/user/repo.git
    # SSH:    git@github.com:user/repo.git

    if current_url.startswith("https://"):
        ssh_url = current_url.replace("https://", "git@").replace("http://", "git@")

        # Handle the domain format: github.com/user/repo -> git@github.com:user/repo
        # The HTTPS URL is: https://github.com/user/repo.git
        # The SSH URL is:   git@github.com:user/repo.git
        ssh_url = ssh_url.replace("github.com/", "github.com:")

        print(f"\nConverting to SSH: {ssh_url}")
        subprocess.run(
            ["git", "remote", "set-url", "origin", ssh_url],
            cwd=repo_path,
            capture_output=True
        )
    elif current_url.startswith("git@"):
        print("Remote is already using SSH!")
        ssh_url = current_url
    else:
        raise ValueError(f"Unknown URL format: {current_url}")

    # Step 4: Verify the new configuration
    print("\nNew remote configuration:")
    result = subprocess.run(
        ["git", "remote", "-v"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 5: Verify SSH connectivity (optional, will test but may prompt for credentials)
    print("\nTesting SSH connection (this may prompt for credentials)...")
    result = subprocess.run(
        ["git", "fetch", "--dry-run"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("SSH connection verification successful!")
    else:
        print(f"SSH verification output: {result.stderr}")


def main():
    """Demonstrate the solution for converting HTTPS to SSH remote URL."""
    print("=" * 60)
    print("Convert Remote from HTTPS to SSH")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    convert_remote_url(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Command:
    git remote set-url origin git@github.com:user/repo.git

URL Transformation:
    https://github.com/user/repo.git
          -->
    git@github.com:user/repo.git

Or use the git config command:
    git config remote.origin.url git@github.com:user/repo.git

Verify with:
    git remote -v           - Show remote URLs
    git remote get-url origin - Get specific remote URL

SSH uses port 22 and requires SSH key authentication, while HTTPS
uses port 443 and may prompt for username/password.
""")


if __name__ == "__main__":
    main()