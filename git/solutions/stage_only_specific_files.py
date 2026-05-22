"""
Solution for "Stage Only Specific Files" (CrowdStrike, Easy)

Scenario:
You have a Git repository at `/home/interview/repo` where you modified three
files: `app.js`, `style.css`, and `config.json`.

Task:
**Stage only app.js and style.css** for commit in the repository at
`/home/interview/repo`, leaving config.json unstaged.
"""


def stage_only_specific_files(
    repo_path: str = "/home/interview/repo",
    files_to_stage: list = None
):
    """
    Stage only specific files, leaving others unstaged.

    Args:
        repo_path: Path to the Git repository
        files_to_stage: List of file paths to stage
    """
    import subprocess

    if files_to_stage is None:
        files_to_stage = ["app.js", "style.css"]

    # Step 1: Check current status
    print("Current git status:")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 2: Confirm the files we want to stage
    print(f"Files to stage: {files_to_stage}")

    # Step 3: Reset any files that might already be staged
    # This ensures we only stage exactly what we specify
    subprocess.run(
        ["git", "reset", "HEAD"],
        cwd=repo_path,
        capture_output=True
    )

    # Step 4: Stage only the specific files
    print(f"\nStaging {files_to_stage}...")
    for file_path in files_to_stage:
        result = subprocess.run(
            ["git", "add", file_path],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  - Staged: {file_path}")
        else:
            print(f"  - Failed to stage: {file_path} ({result.stderr})")

    # Step 5: Verify status shows only intended files staged
    print("\nGit status after staging:")
    result = subprocess.run(
        ["git", "status"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout)

    # Step 6: Verify what will be committed
    print("\nStaged files ready to commit:")
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    print(result.stdout if result.stdout else "(nothing staged)")


def main():
    """Demonstrate the solution for staging only specific files."""
    print("=" * 60)
    print("Stage Only Specific Files")
    print("=" * 60)

    repo_path = "/home/interview/repo"
    stage_only_specific_files(repo_path)

    print("\n" + "=" * 60)
    print("Solution Summary:")
    print("=" * 60)
    print("""
Key Git Commands:
1. git add app.js style.css       - Stage specific files (space-separated)
2. git add *.js                   - Stage all JS files
3. git add -p                     - Interactively stage specific hunks
4. git reset HEAD                 - Unstage everything

Staging Options:
- git add file1 file2            - Stage specific files
- git add directory/             - Stage all files in directory
- git add -A                     - Stage all changes (careful!)
- git add -u                      - Stage modified files only (not new)

To Leave a File Unstaged:
- Don't include it in git add command
- Use .gitignore for files you never want to stage
- Use git update-index for special cases

Note: git add updates both the index and working directory for each file
""")


if __name__ == "__main__":
    main()