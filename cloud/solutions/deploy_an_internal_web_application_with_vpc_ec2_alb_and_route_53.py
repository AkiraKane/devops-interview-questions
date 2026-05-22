"""
Solution for: Deploy an Internal Web Application with VPC, EC2, ALB, and Route 53

Company: Lyft | Difficulty: Hard

Scenario:
Deploy a web application accessible only within a VPC. EC2 instances run in private
subnets behind an Application Load Balancer in public subnets. A startup script at
/tmp/userdata.sh runs a simple HTTP server with a /health endpoint on port 80.

Task:
1. Create VPC `app-vpc` using CIDR 10.0.0.0/16 with public and private subnets
   across two availability zones
2. Create security groups: alb-sg (HTTP from internal networks), ec2-sg (HTTP from ALB only)
3. Launch two EC2 instances in private subnets using Amazon Linux 2 with startup script
4. Configure ALB `app-alb` with target group `app-tg`, health checks at /health, HTTP:80
5. Create private Route 53 hosted zone for `internal.example.com` and CNAME record
   `app.internal.example.com` pointing to ALB
"""

import json
import boto3
import time


VPC_CIDR = '10.0.0.0/16'
SUBNET_PUBLIC_AZ1_CIDR = '10.0.1.0/24'
SUBNET_PUBLIC_AZ2_CIDR = '10.0.2.0/24'
SUBNET_PRIVATE_AZ1_CIDR = '10.0.10.0/24'
SUBNET_PRIVATE_AZ2_CIDR = '10.0.11.0/24'

# The startup script at /tmp/userdata.sh (referenced in the task)
DEFAULT_USERDATA = '''#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
echo "Hello from $(hostname)" > /var/www/html/index.html
cat > /var/www/html/health <<EOF
OK
EOF
'''


# ---------------------------------------------------------------------------
# Step 1: VPC + Subnets
# ---------------------------------------------------------------------------

def create_vpc_and_subnets(ec2_client):
    """Create VPC with public and private subnets across two AZs."""
    # Create VPC
    vpc_resp = ec2_client.create_vpc(CidrBlock=VPC_CIDR)
    vpc_id = vpc_resp['Vpc']['VpcId']
    ec2_client.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'app-vpc'}])
    print(f"Created VPC: app-vpc (ID: {vpc_id})")

    # Enable VPC for DNS hostnames
    ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})

    # Create Internet Gateway
    igw_id = ec2_client.create_internet_gateway()['InternetGateway']['InternetGatewayId']
    ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"Created and attached Internet Gateway: {igw_id}")

    # Create public subnets
    pub_subnet_az1 = ec2_client.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PUBLIC_AZ1_CIDR,
        AvailabilityZone='us-east-1a'
    )['Subnet']['SubnetId']
    pub_subnet_az2 = ec2_client.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PUBLIC_AZ2_CIDR,
        AvailabilityZone='us-east-1b'
    )['Subnet']['SubnetId']
    print(f"Created public subnets: {pub_subnet_az1} (AZ1), {pub_subnet_az2} (AZ2)")

    # Create private subnets
    priv_subnet_az1 = ec2_client.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PRIVATE_AZ1_CIDR,
        AvailabilityZone='us-east-1a'
    )['Subnet']['SubnetId']
    priv_subnet_az2 = ec2_client.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PRIVATE_AZ2_CIDR,
        AvailabilityZone='us-east-1b'
    )['Subnet']['SubnetId']
    print(f"Created private subnets: {priv_subnet_az1} (AZ1), {priv_subnet_az2} (AZ2)")

    # Create public route table
    pub_rt = ec2_client.create_route_table(VpcId=vpc_id)['RouteTable']['RouteTableId']
    ec2_client.create_route(
        RouteTableId=pub_rt, DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id
    )
    ec2_client.associate_route_table(SubnetId=pub_subnet_az1, RouteTableId=pub_rt)
    ec2_client.associate_route_table(SubnetId=pub_subnet_az2, RouteTableId=pub_rt)
    ec2_client.modify_subnet_attribute(SubnetId=pub_subnet_az1, MapPublicIpOnLaunch={'Value': True})
    ec2_client.modify_subnet_attribute(SubnetId=pub_subnet_az2, MapPublicIpOnLaunch={'Value': True})
    print(f"Created public route table: {pub_rt} (with IGW route)")

    return {
        'vpc_id': vpc_id,
        'pub_subnet_az1': pub_subnet_az1,
        'pub_subnet_az2': pub_subnet_az2,
        'priv_subnet_az1': priv_subnet_az1,
        'priv_subnet_az2': priv_subnet_az2,
        'igw_id': igw_id,
        'pub_rt': pub_rt,
    }


# ---------------------------------------------------------------------------
# Step 2: Security Groups
# ---------------------------------------------------------------------------

def create_security_groups(ec2_client, vpc_id):
    """Create alb-sg and ec2-sg security groups."""
    # ALB security group: allow HTTP from internal networks (10.0.0.0/16)
    alb_sg = ec2_client.create_security_group(
        GroupName='alb-sg', Description='Security group for ALB',
        VpcId=vpc_id
    )['GroupId']
    ec2_client.authorize_security_group_ingress(
        GroupId=alb_sg, IpPermissions=[{
            'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
            'CidrIp': '10.0.0.0/16'
        }]
    )
    print(f"Created alb-sg (ID: {alb_sg}) - HTTP from 10.0.0.0/16")

    # EC2 security group: allow HTTP only from ALB
    ec2_sg = ec2_client.create_security_group(
        GroupName='ec2-sg', Description='Security group for EC2 instances',
        VpcId=vpc_id
    )['GroupId']
    ec2_client.authorize_security_group_ingress(
        GroupId=ec2_sg, IpPermissions=[{
            'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
            'UserIdGroupPairs': [{'GroupId': alb_sg}]
        }]
    )
    print(f"Created ec2-sg (ID: {ec2_sg}) - HTTP from alb-sg only")

    return alb_sg, ec2_sg


# ---------------------------------------------------------------------------
# Step 3: EC2 Instances
# ---------------------------------------------------------------------------

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


def launch_ec2_instances(ec2_client, priv_subnet_az1, priv_subnet_az2, ec2_sg):
    """Launch two EC2 instances in private subnets with userdata."""
    ami_id = get_amazon_linux2_ami(ec2_client)

    # Try to read provided userdata script
    try:
        with open('/tmp/userdata.sh', 'r') as f:
            userdata = f.read()
    except FileNotFoundError:
        userdata = DEFAULT_USERDATA

    instance_ids = []
    for i, (az, subnet_id) in enumerate([('AZ1', priv_subnet_az1), ('AZ2', priv_subnet_az2)], 1):
        resp = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType='t2.micro',
            SubnetId=subnet_id,
            SecurityGroupIds=[ec2_sg],
            UserData=userdata,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': f'app-instance-{i}'}]
            }],
            MinCount=1,
            MaxCount=1
        )
        instance_id = resp['Instances'][0]['InstanceId']
        instance_ids.append(instance_id)
        print(f"Launched EC2 instance {instance_id} in {az} ({subnet_id}), tagged web-{i}")

    # Wait for instances to be running
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=instance_ids)
    print(f"All {len(instance_ids)} instances are running")

    return instance_ids


# ---------------------------------------------------------------------------
# Step 4: ALB
# ---------------------------------------------------------------------------

def create_alb(elbv2_client, vpc_id, alb_sg, ec2_sg, pub_subnet_az1, pub_subnet_az2,
               instance_ids):
    """Create ALB, target group, and register instances."""
    # Create ALB in public subnets
    alb = elbv2_client.create_load_balancer(
        Name='app-alb',
        Subnets=[pub_subnet_az1, pub_subnet_az2],
        SecurityGroups=[alb_sg],
        Scheme='internet-facing',
        Tags=[{'Key': 'Name', 'Value': 'app-alb'}]
    )
    alb_arn = alb['LoadBalancers'][0]['LoadBalancerArn']
    alb_dns = alb['LoadBalancers'][0]['DNSName']
    print(f"Created ALB 'app-alb' (ARN: {alb_arn}, DNS: {alb_dns})")

    # Create target group
    tg = elbv2_client.create_target_group(
        Name='app-tg',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        HealthCheckPath='/health',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=2,
        UnhealthyThresholdCount=2,
    )
    tg_arn = tg['TargetGroups'][0]['TargetGroupArn']
    print(f"Created target group 'app-tg' (ARN: {tg_arn})")

    # Register EC2 instances
    elbv2_client.register_targets(TargetGroupArn=tg_arn, Targets=[
        {'Id': iid} for iid in instance_ids
    ])
    print(f"Registered {len(instance_ids)} instances to target group")

    # Create HTTP listener on port 80
    listener = elbv2_client.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[{
            'Type': 'forward',
            'TargetGroupArn': tg_arn
        }]
    )
    print("Created HTTP listener on port 80")

    return alb_arn, alb_dns, tg_arn


# ---------------------------------------------------------------------------
# Step 5: Route 53
# ---------------------------------------------------------------------------

def create_private_zone_and_record(route53, vpc_id, alb_dns):
    """Create private hosted zone for internal.example.com and CNAME record."""
    # Create private hosted zone
    zone = route53.create_hosted_zone(
        Name='internal.example.com',
        CallerReference='internal-example-com',
        HostedZoneConfig={
            'Comment': 'Private hosted zone for internal.example.com',
            'PrivateZone': True
        },
        VPC={'VPCId': vpc_id, 'VPCRegion': 'us-east-1'}
    )
    zone_id = zone['HostedZone']['Id']
    print(f"Created private hosted zone 'internal.example.com' (ID: {zone_id})")

    # Create CNAME record
    route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [{
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': 'app.internal.example.com',
                    'Type': 'CNAME',
                    'TTL': 60,
                    'ResourceRecords': [{'Value': alb_dns}]
                }
            }]
        }
    )
    print("Created CNAME record: app.internal.example.com -> " + alb_dns)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ec2_client = boto3.client('ec2')
    elbv2_client = boto3.client('elbv2')
    route53 = boto3.client('route53')

    print("=== Step 1: Create VPC with public/private subnets across 2 AZs ===")
    net = create_vpc_and_subnets(ec2_client)

    # Wait for VPC to be fully available
    time.sleep(5)

    print("\n=== Step 2: Create security groups ===")
    alb_sg, ec2_sg = create_security_groups(ec2_client, net['vpc_id'])

    print("\n=== Step 3: Launch EC2 instances in private subnets ===")
    instance_ids = launch_ec2_instances(
        ec2_client, net['priv_subnet_az1'], net['priv_subnet_az2'], ec2_sg
    )

    print("\n=== Step 4: Configure ALB with target group and health checks ===")
    alb_arn, alb_dns, tg_arn = create_alb(
        elbv2_client, net['vpc_id'], alb_sg, ec2_sg,
        net['pub_subnet_az1'], net['pub_subnet_az2'], instance_ids
    )

    print("\n=== Step 5: Create private Route 53 zone and CNAME ===")
    create_private_zone_and_record(route53, net['vpc_id'], alb_dns)


if __name__ == '__main__':
    main()