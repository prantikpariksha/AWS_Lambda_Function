import json
import boto3
sns_client = boto3.client('sns')
ec2_console_cli = boto3.client("ec2","us-east-1")
ec2_console_re = boto3.resource("ec2","us-east-1")
fi = [{'Name':'tag:Name', 'Values':["testserver"]}]

def lambda_handler(event, context):
    required_ins = ec2_console_cli.describe_instances(Filters=fi)
    instance_id = required_ins["Reservations"][0]["Instances"][0]["InstanceId"]
    sg_id = str(required_ins["Reservations"][0]["Instances"][0]["SecurityGroups"][0]["GroupId"])

    response = ec2_console_cli.describe_security_groups(
            GroupIds = [sg_id])
            
    current_sg_rules = response["SecurityGroups"][0]["IpPermissions"]
    length=len(current_sg_rules)
    
    for each in range(1,length):
        current_sg_rules = response["SecurityGroups"][0]["IpPermissions"]
        from_port = current_sg_rules[each]['FromPort']
        ip_prtcl = current_sg_rules[each]["IpProtocol"]
        to_port =  current_sg_rules[each]["ToPort"]
        ip_range = current_sg_rules[each]["IpRanges"]
        ec2_console_cli.revoke_security_group_ingress(
                GroupId = sg_id,
                IpPermissions = [{'FromPort' : from_port,
                                'IpProtocol' : ip_prtcl,
                                'IpRanges' : ip_range,
                                'ToPort' : to_port}])
sns_client.publish(
    TopicArn='arn:aws:sns:us-east-1:243874029274:test_prantik_topic',
    Message='Security group was tried to chnage. It has been revokedm')
