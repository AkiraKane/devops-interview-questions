"""
Solution for: Create IAM Role for EC2 with Full IAM Access

Company: Coinbase | Difficulty: Easy

Scenario:
Your team needs an EC2 instance to manage IAM resources programmatically.
Use an IAM role instead of embedding credentials.

Task:
Create an IAM role named `IAMFullAccessEC2` that:
1. Allows the EC2 service to assume the role
2. Has `IAMFullAccess` AWS managed policy attached
"""

import json
import boto3


def create_iam_full_access_ec2_role():
    """Create IAMFullAccessEC2 role with EC2 trust policy and IAMFullAccess."""
    iam = boto3.client('iam')

    # Trust policy allowing EC2 to assume this role
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        role = iam.create_role(
            RoleName='IAMFullAccessEC2',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='EC2 role with full IAM access'
        )
        role_arn = role['Role']['Arn']
        print(f"Created IAM role 'IAMFullAccessEC2' ({role_arn})")
    except iam.exceptions.EntityAlreadyExistsException:
        role = iam.get_role(RoleName='IAMFullAccessEC2')
        role_arn = role['Role']['Arn']
        print(f"Role 'IAMFullAccessEC2' already exists ({role_arn})")

    # Attach AWS managed IAMFullAccess policy
    iam.attach_role_policy(
        RoleName='IAMFullAccessEC2',
        PolicyArn='arn:aws:iam::aws:policy/IAMFullAccess'
    )
    print("Attached IAMFullAccess AWS managed policy to 'IAMFullAccessEC2'")

    # Create an instance profile to allow EC2 to use this role
    try:
        iam.create_instance_profile(InstanceProfileName='IAMFullAccessEC2')
        print("Created instance profile 'IAMFullAccessEC2'")
    except iam.exceptions.EntityAlreadyExistsException:
        print("Instance profile 'IAMFullAccessEC2' already exists")

    iam.add_role_to_instance_profile(
        InstanceProfileName='IAMFullAccessEC2',
        RoleName='IAMFullAccessEC2'
    )
    print("Added role to instance profile")


def main():
    print("=== Creating IAMFullAccessEC2 role ===")
    create_iam_full_access_ec2_role()
    print("\nTo attach to an EC2 instance, use:")
    print("  aws ec2 associate-iam-instance-profile \\")
    print("    --instance-id <INSTANCE_ID> \\")
    print("    --iam-instance-profile Name=IAMFullAccessEC2")


if __name__ == '__main__':
    main()