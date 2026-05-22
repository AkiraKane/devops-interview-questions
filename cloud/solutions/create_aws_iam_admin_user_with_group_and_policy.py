"""
Solution for: Create AWS IAM Admin User with Group and Policy

Company: Accenture | Difficulty: Easy

Scenario:
You need to set up a new administrative user account for regular use instead of using the root account.

Task:
Create an IAM user named `devops-admin` with console password access, add the user to
the `admin` group (with `AdministratorAccess` policy attached), and tag the user with
key `Role` and value `DevOps`.
"""

import json
import boto3


def create_admin_group(iam_client):
    """Create the admin group and attach AdministratorAccess policy."""
    try:
        iam_client.create_group(GroupName='admin')
        print("Created IAM group 'admin'")
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("IAM group 'admin' already exists")

    # Attach AdministratorAccess policy
    iam_client.attach_group_policy(
        GroupName='admin',
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    print("Attached AdministratorAccess policy to group 'admin'")


def create_devops_admin_user(iam_client):
    """Create devops-admin user, add to admin group, and tag with Role=DevOps."""
    try:
        iam_client.create_user(
            UserName='devops-admin',
            Tags=[
                {'Key': 'Role', 'Value': 'DevOps'}
            ]
        )
        print("Created IAM user 'devops-admin'")
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("IAM user 'devops-admin' already exists")

    # Add user to admin group
    iam_client.add_user_to_group(
        GroupName='admin',
        UserName='devops-admin'
    )
    print("Added 'devops-admin' to group 'admin'")

    # Create login profile (console password)
    try:
        login_response = iam_client.create_login_profile(
            UserName='devops-admin',
            Password='TempPass123!',  # Should be changed on first login
            PasswordResetRequired=True
        )
        print("Created console login profile for 'devops-admin'")
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("Login profile for 'devops-admin' already exists")

    # Tag the user
    iam_client.tag_user(
        UserName='devops-admin',
        Tags=[
            {'Key': 'Role', 'Value': 'DevOps'}
        ]
    )
    print("Tagged 'devops-admin' with Role=DevOps")


def main():
    iam_client = boto3.client('iam')

    print("=== Step 1: Create admin group with AdministratorAccess ===")
    create_admin_group(iam_client)

    print("\n=== Step 2: Create devops-admin user, add to group, tag ===")
    create_devops_admin_user(iam_client)

    print("\n=== Verification ===")
    user = iam_client.get_user(UserName='devops-admin')
    print(f"User: {user['User']['UserName']}")
    print(f"ARN: {user['User']['Arn']}")
    print(f"Tags: {user['User'].get('Tags', [])}")
    print("Login profile: created (password must be changed on first login)")


if __name__ == '__main__':
    main()