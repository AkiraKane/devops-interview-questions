#!/usr/bin/env python3
"""
Solutions Runner for Git Interview Questions

This script can run all Git solution scripts or a specific one by name.
Provides verification and documentation for all 22 Git interview questions.

Usage:
    python3 solutions_runner.py              # Run all solutions
    python3 solutions_runner.py --list      # List all available solutions
    python3 solutions_runner.py <solution>  # Run a specific solution
    python3 solutions_runner.py --verify    # Verify Python syntax only
"""

import argparse
import glob
import os
import subprocess
import sys


# Map of solution names to their module names and descriptions
SOLUTIONS = {
    "apply_specific_stash_from_multiple_stashes": {
        "module": "apply_specific_stash_from_multiple_stashes",
        "company": "UBS",
        "difficulty": "Easy",
        "description": "Identify the third stash, preview it, and apply without removing"
    },
    "checkout_single_file_from_another_branch": {
        "module": "checkout_single_file_from_another_branch",
        "company": "Twilio",
        "difficulty": "Easy",
        "description": "Retrieve config.json from feature-settings without switching branches"
    },
    "cherry_pick_specific_commit": {
        "module": "cherry_pick_specific_commit",
        "company": "Ubisoft",
        "difficulty": "Easy",
        "description": "Cherry-pick a bug fix commit from feature branch to main"
    },
    "convert_remote_from_https_to_ssh": {
        "module": "convert_remote_from_https_to_ssh",
        "company": "EPAM",
        "difficulty": "Easy",
        "description": "Change remote URL from HTTPS to SSH"
    },
    "create_an_annotated_tag": {
        "module": "create_an_annotated_tag",
        "company": "Nintendo",
        "difficulty": "Medium",
        "description": "Create an annotated tag v3.1.0 and push to origin"
    },
    "fix_repository_with_unrelated_histories": {
        "module": "fix_repository_with_unrelated_histories",
        "company": "Zscaler",
        "difficulty": "Medium",
        "description": "Merge unrelated local and remote histories using rebase"
    },
    "merge_feature_branch_and_delete": {
        "module": "merge_feature_branch_and_delete",
        "company": "Expedia",
        "difficulty": "Easy",
        "description": "Merge feature-login into main and delete the branch"
    },
    "merge_repositories_preserving_both_histories": {
        "module": "merge_repositories_preserving_both_histories",
        "company": "Zscaler",
        "difficulty": "Medium",
        "description": "Combine repo-a and repo-b into monorepo using subtree"
    },
    "rebase_branch_with_reversed_commit_order": {
        "module": "rebase_branch_with_reversed_commit_order",
        "company": "Booking.com",
        "difficulty": "Easy",
        "description": "Rebase feature-refactor onto main while reversing commit order"
    },
    "rebase_feature_branch": {
        "module": "rebase_feature_branch",
        "company": "Github",
        "difficulty": "Easy",
        "description": "Rebase feature-payment onto main and resolve conflicts"
    },
    "rebase_feature_branch_onto_correct_base": {
        "module": "rebase_feature_branch_onto_correct_base",
        "company": "Samsung",
        "difficulty": "Easy",
        "description": "Rebase feature-login from main onto develop"
    },
    "recover_lost_commits_from_detached_head": {
        "module": "recover_lost_commits_from_detached_head",
        "company": "Kayak",
        "difficulty": "Medium",
        "description": "Recover lost commits from detached HEAD state using reflog"
    },
    "remove_file_from_entire_git_history": {
        "module": "remove_file_from_entire_git_history",
        "company": "Netflix",
        "difficulty": "Medium",
        "description": "Remove secrets.env from entire git history"
    },
    "remove_last_commit_and_discard_changes": {
        "module": "remove_last_commit_and_discard_changes",
        "company": "Gitlab",
        "difficulty": "Easy",
        "description": "Remove last commit and discard all changes"
    },
    "restore_file_to_previous_version": {
        "module": "restore_file_to_previous_version",
        "company": "Slack",
        "difficulty": "Medium",
        "description": "Restore config.js to version from 2 commits ago"
    },
    "shallow_clone_limited_to_latest_commit": {
        "module": "shallow_clone_limited_to_latest_commit",
        "company": "Elastic",
        "difficulty": "Easy",
        "description": "Create shallow clone with only the latest commit"
    },
    "stage_only_specific_files": {
        "module": "stage_only_specific_files",
        "company": "CrowdStrike",
        "difficulty": "Easy",
        "description": "Stage only app.js and style.css for commit"
    },
    "stash_work_fix_bug_restore_and_update": {
        "module": "stash_work_fix_bug_restore_and_update",
        "company": "IBM",
        "difficulty": "Medium",
        "description": "Stash work, create hotfix, merge to main, rebase feature, restore"
    },
    "stash_work_fix_bug_resume": {
        "module": "stash_work_fix_bug_resume",
        "company": "Kraken",
        "difficulty": "Medium",
        "description": "Stash changes, fix syntax error, merge fix, restore stash"
    },
    "undo_commits_but_keep_changes": {
        "module": "undo_commits_but_keep_changes",
        "company": "CrowdStrike",
        "difficulty": "Easy",
        "description": "Undo last 3 commits while keeping changes in working directory"
    },
    "update_submodule_to_latest_commit": {
        "module": "update_submodule_to_latest_commit",
        "company": "GoDaddy",
        "difficulty": "Medium",
        "description": "Update vendor/utils submodule to latest commit"
    },
    "view_unique_commits_between_branch_and_origin": {
        "module": "view_unique_commits_between_branch_and_origin",
        "company": "EPAM",
        "difficulty": "Easy",
        "description": "Find unique commits on feature-api vs origin/main, write to file"
    },
}


def get_solutions_dir():
    """Get the solutions directory path."""
    return os.path.dirname(os.path.abspath(__file__))


def verify_syntax():
    """Verify Python syntax for all solution files."""
    solutions_dir = get_solutions_dir()
    py_files = glob.glob(os.path.join(solutions_dir, "*.py"))

    print("=" * 60)
    print("Verifying Python Syntax")
    print("=" * 60)

    success = True
    for filepath in sorted(py_files):
        filename = os.path.basename(filepath)
        print(f"\nChecking: {filename}")

        result = subprocess.run(
            ["python3", "-m", "py_compile", filepath],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"  [OK] Syntax valid")
        else:
            print(f"  [FAIL] Syntax error:")
            print(f"  {result.stderr}")
            success = False

    print("\n" + "=" * 60)
    if success:
        print("All files passed syntax verification!")
    else:
        print("Some files have syntax errors.")

    return success


def list_solutions():
    """List all available solutions."""
    print("=" * 60)
    print("Available Git Interview Question Solutions")
    print("=" * 60)
    print()

    easy = [(k, v) for k, v in SOLUTIONS.items() if v["difficulty"] == "Easy"]
    medium = [(k, v) for k, v in SOLUTIONS.items() if v["difficulty"] == "Medium"]

    print("Easy Questions:")
    for key, info in easy:
        print(f"  [{info['company']}] {key}")
        print(f"    {info['description']}")
        print()

    print("Medium Questions:")
    for key, info in medium:
        print(f"  [{info['company']}] {key}")
        print(f"    {info['description']}")
        print()

    print("=" * 60)
    print(f"Total: {len(SOLUTIONS)} solutions")


def run_solution(solution_name):
    """Run a specific solution by name."""
    solutions_dir = get_solutions_dir()

    if solution_name not in SOLUTIONS:
        print(f"Unknown solution: {solution_name}")
        print("Use --list to see available solutions.")
        return 1

    module_name = SOLUTIONS[solution_name]["module"]
    info = SOLUTIONS[solution_name]

    print("=" * 60)
    print(f"Running: {solution_name}")
    print(f"Company: {info['company']} | Difficulty: {info['difficulty']}")
    print(f"Description: {info['description']}")
    print("=" * 60)
    print()

    # Import and run the solution
    sys.path.insert(0, solutions_dir)
    try:
        module = __import__(module_name)

        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"Error: Module {module_name} has no main() function")
            return 1

    except Exception as e:
        print(f"Error running solution: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


def run_all_solutions():
    """Run all solutions sequentially."""
    print("=" * 60)
    print("Running All Git Solutions")
    print("=" * 60)
    print()

    # Note: Running solutions in a real repo may fail because they
    # expect specific repositories to exist. This simulates the process.

    for solution_name in sorted(SOLUTIONS.keys()):
        info = SOLUTIONS[solution_name]
        print(f"\n{'='*60}")
        print(f"Solution: {solution_name}")
        print(f"Company: {info['company']} | {info['difficulty']}")
        print(f"{'='*60}")

        # Each solution's main() describes what commands it would run
        # Without a real repo, we just import and describe

        solutions_dir = get_solutions_dir()
        module_name = SOLUTIONS[solution_name]["module"]

        print(f"\nCommands used by this solution:")
        print("-" * 40)

        sys.path.insert(0, solutions_dir)
        try:
            import importlib
            module = importlib.import_module(module_name)

            # Read the docstrings
            if module.__doc__:
                # Extract key commands from the docstring
                doc = module.__doc__
                if "Key Git Command" in doc or "Key Git Commands" in doc:
                    start = doc.find("Key Git Command")
                    if start == -1:
                        start = doc.find("Key Git Commands")
                    if start != -1:
                        end = doc.find("```", start)
                        if end != -1:
                            print(doc[start:end].strip())

        except Exception as e:
            print(f"  (Could not load module details: {e})")

        print()

    print("\nTo run these solutions in a real repository,")
    print("navigate to the repo path specified in each solution.")


def main():
    """Main entry point for the solutions runner."""
    parser = argparse.ArgumentParser(
        description="Git Interview Question Solutions Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 solutions_runner.py --list       List all solutions
  python3 solutions_runner.py --verify     Verify syntax only
  python3 solutions_runner.py <name>        Run specific solution
  python3 solutions_runner.py --all        Run all solutions (demo mode)
        """
    )

    parser.add_argument(
        "solution",
        nargs="?",
        help="Solution name to run"
    )

    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available solutions"
    )

    parser.add_argument(
        "--verify", "-v",
        action="store_true",
        help="Verify Python syntax only"
    )

    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all solutions (demo mode)"
    )

    args = parser.parse_args()

    if args.list:
        list_solutions()
        return 0

    if args.verify:
        success = verify_syntax()
        return 0 if success else 1

    if args.all:
        run_all_solutions()
        return 0

    if args.solution:
        return run_solution(args.solution)

    # Default: show help
    parser.print_help()
    print("\nUse --list to see all solutions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())