#!/usr/bin/env python3
"""
Solution for: Track Forking Process Hierarchies

Company: Splunk | Difficulty: Easy

Scenario:
An unusually large process tree is consuming system resources.

Task:
Identify the parent process with the most child processes and save its full
hierarchy (PIDs and command arguments) to a report file using pstree.

Solution Approach:
- Use `ps` to count children per parent PID
- Find the parent with the most children
- Use `pstree -p` to show the full hierarchy
- Save to a report file
"""

import subprocess
import os


def find_largest_process_tree():
    """
    Find the parent PID with the most child processes.

    Returns (ppid, child_count, command).
    """
    # Get all processes with their PPID
    result = subprocess.run(
        ['ps', '-eo', 'ppid,pid,comm,args'],
        capture_output=True, text=True
    )

    children_count = {}
    ppid_to_cmd = {}

    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
        parts = line.split(None, 3)
        if len(parts) >= 3:
            ppid = parts[0]
            cmd = parts[2] if len(parts) < 4 else parts[3]
            children_count[ppid] = children_count.get(ppid, 0) + 1
            if ppid not in ppid_to_cmd:
                ppid_to_cmd[ppid] = cmd

    if not children_count:
        return None, 0, ''

    # Find the parent with the most children
    top_ppid = max(children_count, key=children_count.get)
    return top_ppid, children_count[top_ppid], ppid_to_cmd.get(top_ppid, 'unknown')


def get_process_tree(pid):
    """Get full process tree from a given PID using pstree."""
    result = subprocess.run(
        ['pstree', '-p', '-a', str(pid)],
        capture_output=True, text=True
    )
    return result.stdout


def save_report(ppid, child_count, cmd, tree, output='/home/devops/process_tree_report.txt'):
    """Save the process hierarchy report."""
    content = f"""=== Process Hierarchy Report ===

Parent PID: {ppid}
Command: {cmd}
Child process count: {child_count}

--- Full Process Tree (pstree -p -a) ---
{tree}
"""

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.write(content)

    print(f"Report saved to {output}")


def main():
    output = '/home/devops/process_tree_report.txt'

    print("=== Track Forking Process Hierarchies ===\n")

    print("Analyzing process tree...")
    ppid, count, cmd = find_largest_process_tree()

    if ppid is None:
        print("No processes found")
        return

    print(f"Largest process tree: PID {ppid} ({cmd})")
    print(f"  Child processes: {count}")

    print(f"\nGetting full hierarchy for PID {ppid}...")
    tree = get_process_tree(ppid)

    save_report(ppid, count, cmd, tree, output)

    # Print preview
    lines = tree.split('\n')
    print("\n--- Tree preview (first 20 lines) ---")
    print('\n'.join(lines[:20]))
    if len(lines) > 20:
        print(f"... ({len(lines)} total lines)")


if __name__ == '__main__':
    main()
