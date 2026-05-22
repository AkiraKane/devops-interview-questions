#!/usr/bin/env python3
"""
Graceful Shutdown with SIGTERM Handling
Company: Robinhood | Difficulty: Medium

Fix application to properly handle SIGTERM signals for graceful shutdown,
implementing cleanup logic so containers exit within 20 seconds on docker stop.
"""

from __future__ import annotations

import signal
import subprocess
import sys
import time
from pathlib import Path


class GracefulShutdown:
    """Handle graceful shutdown with SIGTERM and cleanup."""

    def __init__(self):
        self.cleanup_done = False
        self.shutdown_timeout = 20  # seconds

    def handle_terminate(self, signum, frame):
        """Handle SIGTERM signal - perform cleanup and exit gracefully."""
        print(f"Received signal {signum} - initiating graceful shutdown...")
        self.perform_cleanup()
        self.cleanup_done = True
        sys.exit(0)

    def perform_cleanup(self) -> None:
        """Execute cleanup tasks before shutdown."""
        print("Performing cleanup tasks...")
        # Close database connections
        # Flush buffers
        # Close file handles
        # Finalize logs
        time.sleep(1)  # Simulate cleanup work
        print("Cleanup complete")

    def register_signal_handlers(self) -> None:
        """Register SIGTERM and SIGINT handlers."""
        signal.signal(signal.SIGTERM, self.handle_terminate)
        signal.signal(signal.SIGINT, self.handle_terminate)

    def run(self) -> None:
        """Run the main application loop."""
        self.register_signal_handlers()
        print("Application started - handling graceful shutdown on SIGTERM")
        print(f"Clean shutdown will complete within {self.shutdown_timeout} seconds")

        # Main loop
        import time
        while not self.cleanup_done:
            time.sleep(1)


def generate_app_script() -> str:
    """Generate sample Python application with proper signal handling."""
    return '''#!/usr/bin/env python3
import signal
import sys
import time

shutdown_requested = False

def handle_terminate(signum, frame):
    global shutdown_requested
    print(f"Received SIGTERM - shutting down gracefully...")
    shutdown_requested = True

signal.signal(signal.SIGTERM, handle_terminate)

# Your application code here
print("Application running...")
while not shutdown_requested:
    time.sleep(1)

print("Cleanup complete - exiting")
'''


def create_dockerfile_with_graceful_shutdown() -> str:
    """Generate Dockerfile that properly handles SIGTERM."""
    return '''FROM python:3.11-slim

WORKDIR /app
COPY app.py .
RUN chmod +x app.py

# Use exec form so PID 1 is the app process (receives SIGTERM directly)
CMD ["python", "app.py"]

# Alternative: shell form wrapper for cleanup
# ENTRYPOINT ["/bin/bash", "-c"]
# CMD ["trap exit 15; python app.py"]
'''


def main():
    print("Graceful Shutdown with SIGTERM Handling")
    print("=" * 40)

    print("\n1. Application code with proper signal handling:")
    print(generate_app_script())

    print("\n2. Dockerfile (exec form for proper signal delivery):")
    print(create_dockerfile_with_graceful_shutdown())

    print("\n3. Key concepts:")
    print("   - Use exec form in CMD/ENTRYPOINT so app is PID 1")
    print("   - Register SIGTERM handler in your application")
    print("   - Perform cleanup (close DB, flush buffers) on SIGTERM")
    print("   - Exit cleanly with code 0")
    print("\n4. Testing:")
    print("   docker run --name test-app myapp:grace")
    print("   docker stop test-app  # Should complete within 10 seconds")


if __name__ == "__main__":
    main()