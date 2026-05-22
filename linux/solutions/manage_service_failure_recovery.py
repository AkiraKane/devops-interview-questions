#!/usr/bin/env python3
"""
Solution for Manage Service Failure Recovery

Company: Apple
Difficulty: Hard

Scenario:
You have a shell script at `/usr/local/bin/check_app.sh` that runs periodically
and exits with a non-zero code. The script is currently failing due to a
simulated error condition.

Task:
Create a systemd service named `check_app.service` that automatically restarts
the script when it fails, but stops retrying after 3 restart attempts within
60 seconds. Configure the service to start on boot with a 5-second delay
between restart attempts, then start the service and verify it hits the restart limit.

Solution Approach:
- Create a systemd service unit file with appropriate restart configuration
- Use StartLimitIntervalSec=60 and StartLimitBurst=3 for restart limiting
- Use RestartSec=5 for delay between restart attempts
- Enable and start the service
"""

import subprocess
import os


def create_systemd_service():
    """Create the systemd service unit file."""
    service_content = """[Unit]
Description=Application Health Check Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/check_app.sh
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

    service_path = '/etc/systemd/system/check_app.service'

    with open(service_path, 'w') as f:
        f.write(service_content)

    print(f"Service file created at {service_path}")
    return service_path


def reload_daemon():
    """Reload systemd daemon to recognize new service."""
    try:
        subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
        print("Systemd daemon reloaded")
    except subprocess.CalledProcessError as e:
        print(f"Error reloading daemon: {e}")


def enable_and_start_service():
    """Enable and start the service."""
    try:
        # Enable service to start on boot
        subprocess.run(['sudo', 'systemctl', 'enable', 'check_app.service'], check=True)
        print("Service enabled for boot start")

        # Start the service
        subprocess.run(['sudo', 'systemctl', 'start', 'check_app.service'], check=True)
        print("Service started")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error managing service: {e}")
        return False


def verify_service():
    """Verify service status and restart limit behavior."""
    try:
        result = subprocess.run(
            ['sudo', 'systemctl', 'status', 'check_app.service'],
            capture_output=True,
            text=True,
            check=False
        )
        print("\nService Status:")
        print(result.stdout)

        # Check if restart limit was hit
        result = subprocess.run(
            ['sudo', 'systemctl', 'show', 'check_app.service', '--property', 'NRestarts'],
            capture_output=True,
            text=True,
            check=False
        )
        print(f"Restart count: {result.stdout}")

        # Check for failure
        result = subprocess.run(
            ['sudo', 'journalctl', '-u', 'check_app.service', '-n', '20', '--no-pager'],
            capture_output=True,
            text=True,
            check=False
        )
        print("\nRecent Logs:")
        print(result.stdout)
    except Exception as e:
        print(f"Error verifying service: {e}")


def main():
    """Main function to set up service failure recovery."""
    print("=== Manage Service Failure Recovery ===\n")

    # Create the service file
    create_systemd_service()

    # Reload systemd
    reload_daemon()

    # Enable and start service
    print("\nEnabling and starting service...")
    enable_and_start_service()

    # Verify
    print("\nVerifying service configuration...")
    verify_service()

    print("\nNote: With StartLimitBurst=3 and StartLimitIntervalSec=60,")
    print("the service will stop restarting after 3 failures within 60 seconds.")


if __name__ == '__main__':
    main()