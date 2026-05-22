#!/usr/bin/env python3
"""
Solution for Port Conflict Resolution

Company: Datadog
Difficulty: Easy

Scenario:
An application `/home/interview/server.sh` fails to start.

Task:
Find the cause of failure and resolve it so the server can start successfully.

Solution Approach:
- Try to start the server script
- If it fails, identify which port it's trying to use
- Check what's using that port (netstat/ss/lsof)
- Kill or reconfigure the conflicting process
- Restart the server
"""

import subprocess
import os
import re


def get_server_port(script_path):
    """Extract the port number from the server script."""
    try:
        with open(script_path, 'r') as f:
            content = f.read()

        # Look for common port patterns
        patterns = [
            r'PORT[=\s]+(\d+)',
            r'--port[=\s]+(\d+)',
            r'-p\s+(\d+)',
            r'localhost:(\d+)',
            r'127\.0\.0\.1:(\d+)',
            r'0\.0\.0\.0:(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return int(match.group(1))
    except Exception as e:
        print(f"Error reading script: {e}")

    return None


def find_process_on_port(port):
    """Find process using a specific port."""
    # Try ss first (modern)
    try:
        result = subprocess.run(
            ['ss', '-tlnp', f'=:{port}'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout.strip():
            return result.stdout
    except:
        pass

    # Try netstat
    try:
        result = subprocess.run(
            ['netstat', '-tlnp', f'|', 'grep', f':{port}'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout.strip():
            return result.stdout
    except:
        pass

    # Try lsof
    try:
        result = subprocess.run(
            ['lsof', '-i', f':{port}'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout.strip():
            return result.stdout
    except:
        pass

    return None


def kill_process_on_port(port):
    """Kill the process using a specific port."""
    try:
        # Use lsof to find PID
        result = subprocess.run(
            ['lsof', '-t', '-i', f':{port}'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout.strip():
            pid = result.stdout.strip().split('\n')[0]
            print(f"Found process PID {pid} on port {port}")

            # Kill the process
            subprocess.run(['kill', pid], check=False)
            print(f"Killed process {pid}")
            return True
    except Exception as e:
        print(f"Error killing process: {e}")

    return False


def start_server(script_path):
    """Attempt to start the server script."""
    try:
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"Server started successfully")
        print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print("Server started and running (timeout expected)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Server failed to start: {e.stderr}")
        return False


def main():
    """Main function to resolve port conflict."""
    script_path = '/home/interview/server.sh'

    print("=== Port Conflict Resolution ===\n")

    if not os.path.exists(script_path):
        print(f"Server script not found at {script_path}")
        print("In a real scenario, the script would exist at this location.")
        return

    # Try to start the server
    print(f"Attempting to start {script_path}...")
    success = start_server(script_path)

    if success:
        print("Server started without issues")
        return

    # Extract port from script
    print("\nAnalyzing server script for port configuration...")
    port = get_server_port(script_path)

    if port:
        print(f"Server likely uses port {port}")
    else:
        print("Could not determine port from script")

    # Find what's using the port
    if port:
        print(f"\nChecking what is using port {port}...")
        conflict = find_process_on_port(port)

        if conflict:
            print("Found process on port:")
            print(conflict)

            print("\nResolving conflict...")
            if kill_process_on_port(port):
                # Try starting again
                print("\nRetrying server start...")
                start_server(script_path)
        else:
            print(f"No process found on port {port}")


if __name__ == '__main__':
    main()