from .client import client

def list_sg_in_vpc(account, region, vpc_id):
    # Create a Boto3 client for the EC2 service
    ec2_client = client(account, 'ec2', region)

    # Use the describe_security_groups method to retrieve information about security groups in the specified VPC
    response = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    return {sg['GroupId']: sg for sg in response['SecurityGroups']}

def sg_populate(accounts):
    for description, account in accounts.items():
        for region, region_resources in account['regions'].items():
            for vpc_id in region_resources['vpcs']:
                region_resources['vpcs'][vpc_id]['security_groups'] = list_sg_in_vpc(account, region, vpc_id)
    return accounts