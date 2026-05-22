"""
Solution for: Launch an EC2 Web Server Instance

Company: EPAM | Difficulty: Easy

Scenario:
A basic landing page needs to be delivered via an EC2 instance accessible over
HTTP with its own security group.

Task:
1. Create security group `web-sg` permitting TCP port 80 from any IPv4
2. Launch a `t2.micro` instance tagged as `web-1` using the `web-sg` security group
3. Automatically provision `/var/www/html/index.html` containing "Hello from web-1"
   during startup using user data
"""

import boto3


def get_amazon_linux2_ami(ec2_client):
    """Get the latest Amazon Linux 2 AMI ID."""
    resp = ec2_client.describe_images(
        Filters=[
            {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
            {'Name': 'owner-alias', 'Values': ['amazon']},
            {'Name': 'state', 'Values': ['available']},
        ],
        Owners=['amazon']
    )
    images = sorted(resp['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return images[0]['ImageId']


def create_web_security_group(ec2_client, vpc_id=None):
    """Create web-sg security group allowing TCP port 80 from anywhere."""
    # If no vpc_id provided, use the default VPC
    if vpc_id is None:
        vpcs = ec2_client.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
        vpc_id = vpcs['Vpcs'][0]['VpcId']

    sg_resp = ec2_client.create_security_group(
        GroupName='web-sg',
        Description='Security group for web server - port 80 open to all',
        VpcId=vpc_id
    )
    sg_id = sg_resp['GroupId']
    print(f"Created security group 'web-sg' (ID: {sg_id})")

    # Allow HTTP (port 80) from any IPv4
    ec2_client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'CidrIp': '0.0.0.0/0',
            'Description': 'Allow HTTP from anywhere'
        }]
    )
    print("Ingress rule added: TCP 80 from 0.0.0.0/0")
    return sg_id


def launch_web_instance(ec2_client, sg_id):
    """Launch t2.micro instance tagged web-1 with userdata to create index.html."""
    ami_id = get_amazon_linux2_ami(ec2_client)
    print(f"Using AMI: {ami_id}")

    # User data script that installs httpd and creates index.html
    userdata_script = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "Hello from web-1" > /var/www/html/index.html
echo "<html><body>Hello from web-1</body></html>" >> /var/www/html/index.html
"""

    resp = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        SecurityGroupIds=[sg_id],
        UserData=userdata_script,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'web-1'}]
        }],
        MinCount=1,
        MaxCount=1
    )

    instance = resp['Instances'][0]
    instance_id = instance['InstanceId']
    print(f"Launched instance 'web-1': {instance_id}")
    print(f"  State: {instance['State']['Name']}")
    print("  User data will provision /var/www/html/index.html on first boot")

    return instance_id


def main():
    ec2_client = boto3.client('ec2')

    print("=== Step 1: Create web-sg security group ===")
    sg_id = create_web_security_group(ec2_client)
    print(f"Security group ID: {sg_id}")

    print("\n=== Step 2 & 3: Launch t2.micro instance web-1 with userdata ===")
    instance_id = launch_web_instance(ec2_client, sg_id)
    print(f"\nInstance launched: {instance_id}")
    print("Wait for instance to be 'running', then access over HTTP on port 80.")


if __name__ == '__main__':
    main()