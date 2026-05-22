#!/usr/bin/env python3
"""
Solution for Diagnose Nginx CPU Bottleneck

Company: Palantir
Difficulty: Easy

Scenario:
The web server has become sluggish and users are experiencing timeout errors. Multiple
worker processes are running under the `nginx` user, and one of them is consuming
excessive CPU resources, causing the entire application to slow down.

Task:
Identify the process running under the `nginx` user that consumes the most CPU or
memory, and write its PID to `/home/devops/solution.txt`.

Solution Approach:
- Use ps to find all processes running as nginx user
- Sort by CPU% (or memory) to find the highest consumer
- Write the PID to the solution file
"""

import subprocess
import os


def find_highest_cpu_nginx_process():
    """
    Find nginx process with highest CPU usage.

    Returns:
        tuple: (pid, cpu_percent, mem_percent, command_info)
    """
    try:
        result = subprocess.run(
            ['ps', 'aux', '--sort=-pcpu'],
            capture_output=True,
            text=True,
            check=True
        )

        highest_cpu_proc = None
        for line in result.stdout.split('\n'):
            if 'nginx' in line and 'grep' not in line:
                parts = line.split()
                if len(parts) >= 11:
                    user = parts[0]
                    if user == 'nginx':
                        pid = parts[1]
                        cpu = float(parts[2])
                        mem = float(parts[3])
                        cmd = ' '.join(parts[10:])

                        if highest_cpu_proc is None or cpu > highest_cpu_proc['cpu']:
                            highest_cpu_proc = {
                                'pid': pid,
                                'cpu': cpu,
                                'mem': mem,
                                'cmd': cmd
                            }

        return highest_cpu_proc
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None


def write_solution_file(pid):
    """Write the PID to the solution file."""
    output_file = '/home/devops/solution.txt'

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(pid)

    print(f"PID written to {output_file}")


def main():
    """Main function to diagnose nginx CPU bottleneck."""
    print("=== Diagnosing Nginx CPU Bottleneck ===\n")

    print("Finding nginx processes with highest CPU usage...")
    proc = find_highest_cpu_nginx_process()

    if proc:
        print(f"\nHighest CPU-consuming nginx process found:")
        print(f"  PID: {proc['pid']}")
        print(f"  CPU: {proc['cpu']}%")
        print(f"  MEM: {proc['mem']}%")
        print(f"  Command: {proc['cmd']}")

        # Write to solution file
        write_solution_file(proc['pid'])

        print(f"\nSolution: {proc['pid']}")
    else:
        print("No nginx processes found. Is nginx installed and running?")

        # List all nginx processes for debugging
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                check=True
            )
            nginx_procs = [line for line in result.stdout.split('\n') if 'nginx' in line]
            if nginx_procs:
                print("\nFound nginx processes:")
                for p in nginx_procs:
                    print(f"  {p}")
        except:
            pass


if __name__ == '__main__':
    main()