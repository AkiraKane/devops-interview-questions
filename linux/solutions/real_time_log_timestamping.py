#!/usr/bin/env python3
"""
Solution for Real-Time Log Timestamping

Company: Adobe
Difficulty: Medium

Scenario:
You're troubleshooting a service that produces untagged log output when run manually,
making it difficult to analyze timing and sequence of events.

Task:
Create a command that reads from standard input line by line and appends the current
timestamp to the end of each line. Test it interactively, then save the solution to
`/usr/local/bin/timestamp.sh` and make it executable.

Solution Approach:
- Create a shell script that reads stdin line by line
- Append `date` output (timestamp) to each line
- Save script and make executable
"""

import subprocess
import os


def create_timestamp_script():
    """Create the timestamp.sh script."""
    script_content = '''#!/bin/bash
#
# timestamp.sh - Add timestamps to stdin lines in real-time
# Usage: some_command | timestamp.sh
#
# For each line read from stdin, outputs: LINE - YYYY-MM-DD HH:MM:SS
#

while IFS= read -r line; do
    echo "$line - $(date +"%Y-%m-%d %H:%M:%S")"
done
'''

    script_path = '/usr/local/bin/timestamp.sh'

    with open(script_path, 'w') as f:
        f.write(script_content)

    # Make executable
    os.chmod(script_path, 0o755)

    print(f"Script created at {script_path}")
    return script_path


def test_timestamp_script():
    """Test the timestamp script interactively."""
    script_path = '/usr/local/bin/timestamp.sh'

    print("\nTesting timestamp script with sample output...")

    # Create some test lines
    test_lines = [
        "Application started",
        "Processing request #1234",
        "Database connection established",
        "Request completed"
    ]

    # Pipe test lines through timestamp script
    process = subprocess.Popen(
        [script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, _ = process.communicate(input='\n'.join(test_lines))

    print("\nSample output:")
    print(output)

    return True


def main():
    """Main function to create and test timestamp script."""
    print("=== Real-Time Log Timestamping ===\n")

    # Create the script
    script_path = create_timestamp_script()

    # Make it executable
    try:
        subprocess.run(['chmod', '+x', script_path], check=True)
        print(f"Made {script_path} executable")
    except:
        pass

    # Test it
    test_timestamp_script()

    print("\nThe timestamp script is ready for use:")
    print(f"  {script_path}")
    print("\nUsage examples:")
    print("  cat logfile.log | /usr/local/bin/timestamp.sh")
    print("  ./your_app | /usr/local/bin/timestamp.sh")
    print("  tail -f app.log | /usr/local/bin/timestamp.sh")


if __name__ == '__main__':
    main()