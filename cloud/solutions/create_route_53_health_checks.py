"""
Solution for: Create Route 53 Health Checks

Company: Autodesk | Difficulty: Easy

Scenario:
Infrastructure has two application endpoints requiring distinct monitoring strategies
through Route 53 health checks with different protocols, ports, intervals, and thresholds.

Task:
Configure two health checks:
1. web-server: 10.0.1.10, HTTP port 80, /health path, 3-failure threshold, 30-second intervals
2. api-server: 10.0.2.10, HTTPS port 443, 5-failure threshold, 10-second fast intervals,
   inverted status enabled, monitoring from US East, EU Ireland, Asia Pacific Singapore
"""

import boto3


def create_health_checks():
    """Create the two Route 53 health checks as specified."""
    route53 = boto3.client('route53')

    # Health check 1: web-server
    # HTTP on port 80, /health path, 30-second interval, 3 failures
    web_check = route53.create_health_check(
        CallerReference='web-server-health-check',
        HealthCheckConfig={
            'IPAddress': '10.0.1.10',
            'Port': 80,
            'Type': 'HTTP',
            'Path': '/health',
            'Interval': 30,
            'FailureThreshold': 3,
            'MeasureLatency': False,
            'Regions': [],  # Default: AWS will choose regions
        }
    )
    web_check_id = web_check['HealthCheck']['Id']
    print(f"Created health check 'web-server' (ID: {web_check_id})")
    print(f"  IP: 10.0.1.10, Protocol: HTTP, Port: 80, Path: /health")
    print(f"  Interval: 30s, FailureThreshold: 3")

    # Health check 2: api-server
    # HTTPS on port 443, 10-second fast interval, 5 failures, inverted, 3 regions
    api_check = route53.create_health_check(
        CallerReference='api-server-health-check',
        HealthCheckConfig={
            'IPAddress': '10.0.2.10',
            'Port': 443,
            'Type': 'HTTPS',
            'Interval': 10,
            'FailureThreshold': 5,
            'Inverted': True,
            'HealthThreshold': 1,
            'Regions': ['us-east-1', 'eu-west-1', 'ap-southeast-1'],
        }
    )
    api_check_id = api_check['HealthCheck']['Id']
    print(f"\nCreated health check 'api-server' (ID: {api_check_id})")
    print(f"  IP: 10.0.2.10, Protocol: HTTPS, Port: 443")
    print(f"  Interval: 10s (fast), FailureThreshold: 5")
    print(f"  Inverted: True, Regions: us-east-1, eu-west-1, ap-southeast-1")


def main():
    print("=== Creating Route 53 Health Checks ===\n")
    create_health_checks()


if __name__ == '__main__':
    main()