#!/usr/bin/env python3
"""
Solution for Monitoring Process Ownership

Company: HashiCorp
Difficulty: Medium

Scenario:
The server is consuming excessive resources. This server is used by multiple teams
with their own credentials (e.g. each team has a username dev-team, qa-team,
ops-team, etc.).

Task:
Identify which user is running the most number of processes on the server,
regardless of CPU or memory usage, and write that username to /home/devops/solution.txt.

Solution Approach:
- Use ps to list all processes with user information
- Count processes per user
- Find the user with the highest count
- Write the username to the solution file
"""

import subprocess
import os
from collections import Counter


def count_processes_per_user():
    """
    Count the number of processes for each user.

    Returns:
        dict: Dictionary mapping username to process count
    """
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True,
            check=True
        )

        user_counts = Counter()

        for line in result.stdout.split('\n'):
            if 'ps aux' in line or 'USER' in line:
                continue

            parts = line.split()
            if len(parts) >= 1:
                user = parts[0]
                user_counts[user] += 1

        return user_counts
    except subprocess.CalledProcessError as e:
        print(f"Error counting processes: {e.stderr}")
        return Counter()


def find_top_process_user(user_counts):
    """
    Find the user with the most processes.

    Returns:
        tuple: (username, count)
    """
    if not user_counts:
        return None, 0

    top_user = user_counts.most_common(1)[0]
    return top_user[0], top_user[1]


def write_solution_file(username):
    """Write the solution username to file."""
    output_file = '/home/devops/solution.txt'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(username)

    print(f"Solution written to {output_file}")


def main():
    """Main function to monitor process ownership."""
    print("=== Monitoring Process Ownership ===\n")

    # Count processes per user
    print("Counting processes per user...")
    user_counts = count_processes_per_user()

    if not user_counts:
        print("Could not get process counts")
        return

    # Sort by count descending
    sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop 10 users by process count:")
    print(f"{'USER':<20} {'PROCESSES':<10}")
    print("-" * 30)

    for user, count in sorted_users[:10]:
        print(f"{user:<20} {count:<10}")

    # Find user with most processes
    top_user, count = find_top_process_user(user_counts)

    print(f"\n=== Solution ===")
    print(f"User with most processes: {top_user} ({count} processes)")

    # Write to solution file
    write_solution_file(top_user)


if __name__ == '__main__':
    main()