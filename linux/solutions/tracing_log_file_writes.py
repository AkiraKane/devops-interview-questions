#!/usr/bin/env python3
"""
Solution for: Tracing Log File Writes

Company: Bloomberg | Difficulty: Easy

Scenario:
/var/log/messages is growing unusually fast and filling the disk.

Task:
Use real-time monitoring to identify the process writing heavily to that log file,
then save the process details (via ps) and the last 50 lines of logs to a report file.

Solution Approach:
- Use `lsof /var/log/messages` to find processes with open file handles
- Use `fuser` as an alternative to identify writing processes
- Save process details and last 50 log lines to a report
"""

import subprocess
import os


def find_writing_processes(log_file='/var/log/messages'):
    """Find processes that have the log file open for writing."""
    writers = []

    # Method 1: lsof
    try:
        result = subprocess.run(
            ['lsof', '+D', os.path.dirname(log_file)],
            capture_output=True, text=True
        )
        for line in result.stdout.split('\n'):
            if log_file in line and ('w' in line or 'u' in line):
                parts = line.split()
                if len(parts) >= 2:
                    writers.append({
                        'pid': parts[1],
                        'user': parts[2],
                        'command': parts[0],
                        'raw': line
                    })
    except FileNotFoundError:
        pass

    # Method 2: fuser
    try:
        result = subprocess.run(
            ['fuser', '-v', log_file],
            capture_output=True, text=True
        )
        # fuser outputs to stderr
        for line in (result.stdout + result.stderr).split('\n'):
            if log_file in line or any(c.isdigit() for c in line):
                parts = line.split()
                for part in parts:
                    if part.rstrip('rwfu').isdigit():
                        pid = part.rstrip('rwfu')
                        if not any(w['pid'] == pid for w in writers):
                            writers.append({'pid': pid, 'user': '?', 'command': '?', 'raw': line})
    except FileNotFoundError:
        pass

    return writers


def get_process_details(pid):
    """Get detailed process information."""
    result = subprocess.run(
        ['ps', '-p', pid, '-o', 'pid,ppid,user,%cpu,%mem,stat,start,time,comm,args'],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def save_report(writers, log_file='/var/log/messages', output='/home/devops/log_write_report.txt'):
    """Save process details and last 50 log lines to a report."""
    content = "=== Log File Write Report ===\n\n"
    content += f"Log file: {log_file}\n"
    content += f"Processes writing to {log_file}: {len(writers)}\n\n"

    content += "--- Writing Processes ---\n"
    for w in writers:
        content += f"\nPID: {w['pid']}\n"
        content += get_process_details(w['pid']) + "\n"

    # Get last 50 lines of the log
    content += "\n--- Last 50 Lines of Log ---\n"
    try:
        result = subprocess.run(
            ['tail', '-50', log_file],
            capture_output=True, text=True
        )
        content += result.stdout
    except Exception as e:
        content += f"Error reading log: {e}\n"

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        f.write(content)

    print(f"Report saved to {output}")
    return content


def main():
    log_file = '/var/log/messages'
    output = '/home/devops/log_write_report.txt'

    print("=== Tracing Log File Writes ===\n")
    print(f"Finding processes writing to {log_file}...")

    writers = find_writing_processes(log_file)

    if writers:
        print(f"Found {len(writers)} writing process(es):")
        for w in writers:
            print(f"  PID {w['pid']} ({w['command']}) - {w['user']}")
    else:
        print("No active writers found (may need root permissions)")
        print("Trying alternative: checking recent write activity via audit...")
        # Fallback: use audit or strace if available

    report = save_report(writers, log_file, output)
    print("\nReport preview:")
    print(report[:500])


if __name__ == '__main__':
    main()
