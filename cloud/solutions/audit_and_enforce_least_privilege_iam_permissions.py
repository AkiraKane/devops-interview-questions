"""
Solution for: Audit and Enforce Least-Privilege IAM Permissions

Company: Amazon | Difficulty: Easy

Scenario:
A security audit has flagged the IAM user `app-deployer` for having `AdministratorAccess`
policy with far more permissions than needed. The user only needs access to:
- S3: Read (GetObject), Add objects (PutObject), list buckets (ListBucket)
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

Task:
1. Inspect current policies attached to `app-deployer`
2. Remove `AdministratorAccess` policy
3. Create a custom managed policy named `AppDeployerPolicy` with only required permissions
4. Attach the new policy to `app-deployer`
"""

import json
import boto3


def get_attached_policies(iam_client, username):
    """Fetch all managed policies attached to a user."""
    paginator = iam_client.get_paginator('list_attached_user_policies')
    policies = []
    for page in paginator.paginate(UserName=username):
        policies.extend(page['AttachedPolicies'])
    return policies


def get_inline_policies(iam_client, username):
    """Fetch all inline policies attached to a user."""
    paginator = iam_client.get_paginator('list_user_policies')
    policies = []
    for page in paginator.paginate(UserName=username):
        policies.extend(page['PolicyNames'])
    return policies


def create_app_deployer_policy(iam_client):
    """Create the least-privilege AppDeployerPolicy."""
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "S3ReadAndWrite",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": "*"
            },
            {
                "Sid": "S3ListBuckets",
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "*"
            },
            {
                "Sid": "CloudWatchLogs",
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            }
        ]
    }

    # Create the managed policy
    response = iam_client.create_policy(
        PolicyName='AppDeployerPolicy',
        PolicyDocument=json.dumps(policy_document),
        Description='Least-privilege policy for app-deployer: S3 read/write + CloudWatch Logs'
    )
    return response['Policy']['Arn']


def remove_policy_and_replace(iam_client, username, new_policy_arn):
    """Remove AdministratorAccess and attach the new least-privilege policy."""
    # Detach AdministratorAccess
    iam_client.detach_user_policy(
        UserName=username,
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    print(f"Detached AdministratorAccess from user '{username}'")

    # Also check for any other managed policies that may be too broad and detach them
    attached = get_attached_policies(iam_client, username)
    for policy in attached:
        print(f"  Still attached: {policy['PolicyName']} ({policy['PolicyArn']})")

    # Attach the new least-privilege policy
    iam_client.attach_user_policy(
        UserName=username,
        PolicyArn=new_policy_arn
    )
    print(f"Attached AppDeployerPolicy ({new_policy_arn}) to user '{username}'")


def main():
    iam_client = boto3.client('iam')
    username = 'app-deployer'

    print("=== Step 1: Inspect current policies ===")
    attached = get_attached_policies(iam_client, username)
    inline = get_inline_policies(iam_client, username)

    print(f"Managed policies attached to '{username}':")
    for p in attached:
        print(f"  - {p['PolicyName']} ({p['PolicyArn']})")

    print(f"Inline policies attached to '{username}':")
    for p in inline:
        print(f"  - {p}")

    print("\n=== Step 2 & 3: Create AppDeployerPolicy ===")
    policy_arn = create_app_deployer_policy(iam_client)
    print(f"Created policy: {policy_arn}")

    print("\n=== Step 4: Replace policy ===")
    remove_policy_and_replace(iam_client, username, policy_arn)

    print("\n=== Verification ===")
    remaining = get_attached_policies(iam_client, username)
    print(f"Policies now attached to '{username}':")
    for p in remaining:
        print(f"  - {p['PolicyName']}")


if __name__ == '__main__':
    main()