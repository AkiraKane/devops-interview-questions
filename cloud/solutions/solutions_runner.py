"""
Amazon Cloud Solutions — solutions_runner.py

Runs all 10 AWS cloud solutions in sequence.

Each solution maps to a markdown question file in the cloud/ directory and implements
the scenario using AWS CLI / boto3.

Usage:
    # Run all solutions
    python3 solutions_runner.py

    # Run a specific solution by name
    python3 solutions_runner.py audit_and_enforce_least_privilege_iam_permissions

    # Dry-run (just print what would run)
    python3 solutions_runner.py --dry-run
"""

import argparse
import importlib
import sys
import os

# Ensure the cloud/ package directory is on sys.path so "import solutions" works
# __file__ = /.../cloud/solutions/solutions_runner.py  →  parent = /.../cloud/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from solutions import (
    audit_and_enforce_least_privilege_iam_permissions,
    build_a_serverless_api,
    create_hello_world_lambda_function,
    create_aws_iam_admin_user,
    create_iam_role_for_ec2,
    create_route_53_health_checks,
    create_route_53_hosted_zone,
    deploy_internal_web_application,
    design_egress_only_vpc,
    launch_ec2_web_server,
)

ALL_SOLUTIONS = [
    ("audit_and_enforce_least_privilege_iam_permissions",
     audit_and_enforce_least_privilege_iam_permissions,
     "Audit and Enforce Least-Privilege IAM Permissions"),
    ("build_a_serverless_api",
     build_a_serverless_api,
     "Build a Serverless API with Lambda, API GW, and DynamoDB"),
    ("create_hello_world_lambda_function",
     create_hello_world_lambda_function,
     "Create a Hello World Lambda Function"),
    ("create_aws_iam_admin_user",
     create_aws_iam_admin_user,
     "Create AWS IAM Admin User with Group and Policy"),
    ("create_iam_role_for_ec2",
     create_iam_role_for_ec2,
     "Create IAM Role for EC2 with Full IAM Access"),
    ("create_route_53_health_checks",
     create_route_53_health_checks,
     "Create Route 53 Health Checks"),
    ("create_route_53_hosted_zone",
     create_route_53_hosted_zone,
     "Create Route 53 Hosted Zone and DNS Records"),
    ("deploy_internal_web_application",
     deploy_internal_web_application,
     "Deploy an Internal Web Application with VPC, EC2, ALB, Route 53"),
    ("design_egress_only_vpc",
     design_egress_only_vpc,
     "Design Egress Only VPC with NAT"),
    ("launch_ec2_web_server",
     launch_ec2_web_server,
     "Launch an EC2 Web Server Instance"),
]


def run_all():
    """Run all 10 solutions in sequence."""
    print("=" * 70)
    print("  Amazon Cloud Solutions — Running All Solutions")
    print("=" * 70)

    passed = 0
    failed = 0

    for name, module, description in ALL_SOLUTIONS:
        print(f"\n{'─' * 70}")
        print(f"  [{name}]")
        print(f"  {description}")
        print(f"{'─' * 70}")
        try:
            module.main()
            passed += 1
            print(f"  [PASSED] {name}")
        except Exception as e:
            failed += 1
            print(f"  [FAILED] {name}: {e}")

    print(f"\n{'=' * 70}")
    print(f"  Results: {passed} passed, {failed} failed out of {len(ALL_SOLUTIONS)}")
    print(f"{'=' * 70}")


def run_one(name: str):
    """Run a single named solution."""
    for n, module, description in ALL_SOLUTIONS:
        if n == name:
            print(f"Running: {description}")
            module.main()
            return
    print(f"Unknown solution: {name}")
    print("Available solutions:")
    for n, _, description in ALL_SOLUTIONS:
        print(f"  {n} — {description}")


def dry_run():
    """Print the list of all solutions without executing."""
    print("Available solutions (dry-run):")
    for n, _, description in ALL_SOLUTIONS:
        print(f"  {n}")
        print(f"    → {description}")


def main():
    parser = argparse.ArgumentParser(description="Amazon Cloud Solutions Runner")
    parser.add_argument(
        'solution', nargs='?',
        help="Name of a specific solution to run. Omit to run all."
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help="List all solutions without running them."
    )
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
    elif args.solution:
        run_one(args.solution)
    else:
        run_all()


if __name__ == '__main__':
    main()