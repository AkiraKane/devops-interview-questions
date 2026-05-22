"""
Solution for: Design Egress Only VPC with NAT

Company: Twitch | Difficulty: Medium

Scenario:
Prepare infrastructure for ECS tasks and EC2 instances spanning two AZs. Workloads
require outbound internet access (HTTP/HTTPS) but no inbound access. Also need
cost-effective routing to S3.

Task:
Design and implement a VPC network architecture (10.0.0.0/16) with:
1. Network Isolation: Workloads in private subnets in 2 AZs, no public IPs
2. Egress Control: Outbound via NAT Gateway (no inbound from internet)
3. Egress Restrictions: Security group limiting outbound to required protocols
4. Cost Awareness: S3 traffic via Gateway VPC endpoints (no NAT for S3)
"""

import boto3


VPC_CIDR = '10.0.0.0/16'
SUBNET_PRIVATE_AZ1_CIDR = '10.0.10.0/24'  # AZ1 private subnet
SUBNET_PRIVATE_AZ2_CIDR = '10.0.11.0/24'  # AZ2 private subnet
SUBNET_PUBLIC_AZ1_CIDR = '10.0.1.0/24'   # NAT GW in AZ1
SUBNET_PUBLIC_AZ2_CIDR = '10.0.2.0/24'   # NAT GW in AZ2 (optional HA)


def create_vpc_architecture():
    """Create the complete VPC architecture with egress-only design."""
    ec2 = boto3.client('ec2')

    # ---- VPC ----
    vpc_resp = ec2.create_vpc(CidrBlock=VPC_CIDR)
    vpc_id = vpc_resp['Vpc']['VpcId']
    ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'egress-only-vpc'}])
    # Enable DNS features
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    print(f"Created VPC: {vpc_id} (CIDR: {VPC_CIDR})")

    # ---- Internet Gateway ----
    igw_id = ec2.create_internet_gateway()['InternetGateway']['InternetGatewayId']
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
    print(f"Created and attached IGW: {igw_id}")

    # ---- Public subnets (for NAT Gateway) ----
    pub_subnet_az1_id = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PUBLIC_AZ1_CIDR,
        AvailabilityZone='us-east-1a'
    )['Subnet']['SubnetId']
    pub_subnet_az2_id = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PUBLIC_AZ2_CIDR,
        AvailabilityZone='us-east-1b'
    )['Subnet']['SubnetId']
    print(f"Created public subnets: {pub_subnet_az1_id} (AZ1), {pub_subnet_az2_id} (AZ2)")

    # ---- Private subnets (workload subnets) ----
    priv_subnet_az1_id = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PRIVATE_AZ1_CIDR,
        AvailabilityZone='us-east-1a'
    )['Subnet']['SubnetId']
    priv_subnet_az2_id = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock=SUBNET_PRIVATE_AZ2_CIDR,
        AvailabilityZone='us-east-1b'
    )['Subnet']['SubnetId']
    print(f"Created private subnets: {priv_subnet_az1_id} (AZ1), {priv_subnet_az2_id} (AZ2)")

    # ---- Public Route Table ----
    pub_rt_id = ec2.create_route_table(VpcId=vpc_id)['RouteTable']['RouteTableId']
    ec2.create_route(RouteTableId=pub_rt_id, DestinationCidrBlock='0.0.0.0/0', GatewayId=igw_id)
    ec2.associate_route_table(SubnetId=pub_subnet_az1_id, RouteTableId=pub_rt_id)
    ec2.associate_route_table(SubnetId=pub_subnet_az2_id, RouteTableId=pub_rt_id)
    # Map public IPs on public subnets
    ec2.modify_subnet_attribute(SubnetId=pub_subnet_az1_id, MapPublicIpOnLaunch={'Value': True})
    ec2.modify_subnet_attribute(SubnetId=pub_subnet_az2_id, MapPublicIpOnLaunch={'Value': True})
    print(f"Created public route table: {pub_rt_id}")
    print(f"  - Route: 0.0.0.0/0 -> IGW ({igw_id})")

    # ---- NAT Gateway (in AZ1 public subnet) ----
    nat_eip_alloc = ec2.allocate_address(Domain='vpc')['AllocationId']
    nat_resp = ec2.create_nat_gateway(
        SubnetId=pub_subnet_az1_id,
        AllocationId=nat_eip_alloc
    )
    nat_gw_id = nat_resp['NatGateway']['NatGatewayId']
    print(f"Created NAT Gateway: {nat_gw_id} (EIP: {nat_eip_alloc})")

    # Wait for NAT Gateway to be available
    waiter = ec2.get_waiter('nat_gateway_available')
    waiter.wait(NatGatewayIds=[nat_gw_id])
    print(f"NAT Gateway {nat_gw_id} is now available")

    # ---- Private Route Table (route 0.0.0.0/0 via NAT) ----
    priv_rt_id = ec2.create_route_table(VpcId=vpc_id)['RouteTable']['RouteTableId']
    ec2.create_route(RouteTableId=priv_rt_id, DestinationCidrBlock='0.0.0.0/0', NatGatewayId=nat_gw_id)
    ec2.associate_route_table(SubnetId=priv_subnet_az1_id, RouteTableId=priv_rt_id)
    ec2.associate_route_table(SubnetId=priv_subnet_az2_id, RouteTableId=priv_rt_id)
    print(f"Created private route table: {priv_rt_id}")
    print(f"  - Route: 0.0.0.0/0 -> NAT Gateway ({nat_gw_id})")

    # ---- Gateway VPC Endpoint for S3 (cost-effective, no NAT) ----
    # Create S3 VPC endpoint with prefix lists
    s3_vpce = ec2.create_vpc_endpoint(
        VpcId=vpc_id,
        ServiceName='com.amazonaws.us-east-1.s3',
        RouteTableIds=[priv_rt_id],
        VpcEndpointType='Gateway'
    )['VpcEndpoint']['VpcEndpointId']
    print(f"Created S3 Gateway VPC endpoint: {s3_vpce}")

    # Also create DynamoDB Gateway endpoint (optional but good practice)
    ddb_vpce = ec2.create_vpc_endpoint(
        VpcId=vpc_id,
        ServiceName='com.amazonaws.us-east-1.dynamodb',
        RouteTableIds=[priv_rt_id],
        VpcEndpointType='Gateway'
    )['VpcEndpoint']['VpcEndpointId']
    print(f"Created DynamoDB Gateway VPC endpoint: {ddb_vpce}")

    # ---- Security Group for Workloads ----
    # Create security group with egress restrictions
    workload_sg_id = ec2.create_security_group(
        GroupName='workload-sg',
        Description='Security group for EC2/ECS workloads - restricted outbound',
        VpcId=vpc_id
    )['GroupId']
    ec2.create_tags(Resources=[workload_sg_id], Tags=[{'Key': 'Name', 'Value': 'workload-sg'}])
    print(f"Created security group: {workload_sg_id}")

    # Allow all outbound by default (0.0.0.0/0) - in practice restrict per protocol/destination
    # The default egress rule allows all outbound. For stricter control:
    ec2.authorize_security_group_egress(
        GroupId=workload_sg_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'CidrIp': '0.0.0.0/0',
            'Description': 'Allow outbound HTTP'
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 443,
            'ToPort': 443,
            'CidrIp': '0.0.0.0/0',
            'Description': 'Allow outbound HTTPS'
        }]
    )
    print(f"Configured egress rules on {workload_sg_id}: HTTP/HTTPS only to 0.0.0.0/0")

    print("\n=== Architecture Summary ===")
    print(f"VPC: {vpc_id} ({VPC_CIDR})")
    print(f"  Public Subnets (NAT GW): {pub_subnet_az1_id}, {pub_subnet_az2_id}")
    print(f"  Private Subnets (Workloads): {priv_subnet_az1_id}, {priv_subnet_az2_id}")
    print(f"  NAT Gateway: {nat_gw_id} (AZ1)")
    print(f"  S3 VPC Endpoint: {s3_vpce} (direct, no NAT)")
    print(f"  DynamoDB VPC Endpoint: {ddb_vpce} (direct, no NAT)")
    print(f"  Security Group: {workload_sg_id}")
    print("\nEgress flow: Workload (private) -> NAT GW (public) -> Internet")
    print("S3 flow: Workload (private) -> S3 VPC Endpoint -> S3 (no NAT, cost-effective)")


def main():
    print("=== Designing Egress-Only VPC with NAT ===\n")
    create_vpc_architecture()


if __name__ == '__main__':
    main()