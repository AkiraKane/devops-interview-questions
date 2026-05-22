"""
Solution for: Create Route 53 Hosted Zone and DNS Records

Company: Kayak | Difficulty: Easy

Scenario:
Your team is launching a new application and needs DNS configured in Route 53
for the domain `example.com`.

Task:
1. Create a hosted zone for `example.com`
2. Create an A record for `app.example.com` pointing to `10.20.30.40`
   with TTL set to 60 seconds
"""

import boto3


def create_hosted_zone():
    """Create a public hosted zone for example.com."""
    route53 = boto3.client('route53')

    try:
        zone = route53.create_hosted_zone(
            Name='example.com',
            CallerReference='example-com-hosted-zone',
            HostedZoneConfig={
                'Comment': 'Hosted zone for example.com',
                'PrivateZone': False
            }
        )
        zone_id = zone['HostedZone']['Id']
        print(f"Created hosted zone for 'example.com' (ID: {zone_id})")
        return zone_id
    except route53.exceptions.InvalidDNSNameException:
        # Zone may already exist
        paginator = route53.get_paginator('list_hosted_zones')
        for page in paginator.paginate():
            for z in page['HostedZones']:
                if z['Name'] == 'example.com.':
                    print(f"Hosted zone for 'example.com' already exists (ID: {z['Id']})")
                    return z['Id']
    except route53.exceptions.HostedZoneAlreadyExists:
        print("Hosted zone for 'example.com' already exists")


def create_app_record(zone_id):
    """Create A record for app.example.com pointing to 10.20.30.40 with TTL 60."""
    route53 = boto3.client('route53')

    change_batch = {
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': 'app.example.com',
                    'Type': 'A',
                    'TTL': 60,
                    'ResourceRecords': [
                        {'Value': '10.20.30.40'}
                    ]
                }
            }
        ]
    }

    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch=change_batch
    )
    print(f"\nCreated A record: app.example.com -> 10.20.30.40 (TTL: 60s)")
    print(f"Change status: {response['ChangeInfo']['Status']}")


def main():
    route53 = boto3.client('route53')

    print("=== Step 1: Create hosted zone for example.com ===")
    zone_id = create_hosted_zone()

    print("\n=== Step 2: Create A record for app.example.com ===")
    create_app_record(zone_id)


if __name__ == '__main__':
    main()