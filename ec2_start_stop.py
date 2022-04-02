#!/usr/bin/env python3

import time
import argparse
import boto3.ec2
import sys
from botocore.exceptions import ClientError


class aws_ec2:
    """Class which start/stop the ec2 instance using boto3"""

    def __init__(self):
        try:
            parser = argparse.ArgumentParser(description='Script will be responsible for creating \
                                                                        the aws ec2 instance using boto3')
            parser.add_argument('-k', '--aws_access_key', help='AWS access key of IAM user')
            parser.add_argument('-s', '--aws_secret_key', help='AWS secert key of IAM user')
            parser.add_argument('-r', '--aws_region', help='AWS region where we want to launch ec2 instance')
            parser.add_argument('-t', '--ec2_tag', help='AWS instance tag name to start and stop')
            parser.add_argument('-u', '--ec2_up', help="Start the EC2 instance", action='store_true')
            parser.add_argument('-d', '--ec2_down', help="Stop the EC2 instance", action='store_true')

            args = parser.parse_args()
            self.aws_access_key = args.aws_access_key
            self.aws_secret_key = args.aws_secret_key
            self.aws_region = args.aws_region
            self.ec2_tag_name = args.ec2_tag
            self.instance_id = None

            if args.aws_access_key is None or \
                    args.aws_secret_key is None or \
                    args.aws_region is None or \
                    args.ec2_tag is None:
                print("Please have a valid input, please look for help -h")
                sys.exit(1)
            if args.ec2_up:
                self.start_ec2()
            elif args.ec2_down:
                self.stop_ec2()
            else:
                print("Missing argument! Type '-h' for available arguments.")
        except Exception as e:
            print("Exception while paring input arguments, Exception for your reference : " + str(e))
            sys.exit(1)

    def establish_session_using_boto3(self):
        """ Create the client connection using boto3"""
        try:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region)
            service_client = session.client('ec2')
            return service_client
        except Exception as e:
            print("Exception while creating the session, Exception for your reference : " + str(e))
            sys.exit(1)

    def get_instance_id(self):
        client_conn = self.establish_session_using_boto3()
        custom_filter = [{'Name': 'tag:Name', 'Values': [self.ec2_tag_name]}]
        describe_instance = client_conn.describe_instances(Filters=custom_filter)
        return describe_instance['Reservations'][0]['Instances'][0]['InstanceId']

    def start_ec2(self):
        """
        Do a dryrun first to verify permissions.
        Try to start the EC2 instance.
        """
        print("-" * 30)
        print("Try to start the EC2 instance.")
        print("-" * 30)
        ec2 = self.establish_session_using_boto3()
        instance_id = self.get_instance_id()
        try:
            print("Start dry run...")
            ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, run start_instances without dryrun
        try:
            print("Start instance without dry run...")
            response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
            self.fetch_public_ip(instance_id)
        except ClientError as e:
            print(e)

    def stop_ec2(self):
        """
        Do a dryrun first to verify permissions.
        Try to stop the EC2 instance.
        """
        ec2 = self.establish_session_using_boto3()
        instance_id = self.get_instance_id()
        print("-" * 30)
        print("Try to stop the EC2 instance.")
        print("-" * 30)

        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def fetch_public_ip(self, instance_id):
        """
        Fetch the public IP that has been assigned to the EC2 instance.
        :return: Print the public IP to the console.
        """
        ec2 = boto3.resource('ec2',
                             aws_access_key_id=self.aws_access_key,
                             aws_secret_access_key=self.aws_secret_key,
                             region_name=self.aws_region)
        instance = ec2.Instance(id=instance_id)
        print("Waiting for Instance to start...")
        instance.wait_until_running()
        sess = self.establish_session_using_boto3()
        describe_instance = sess.describe_instances(InstanceIds=[instance_id])
        publicIpAddress = str(describe_instance["Reservations"][0]["Instances"][0]["PublicIpAddress"])
        print("Public IPv4 address of the EC2 instance: {0}".format(publicIpAddress))


if __name__ == '__main__':
    aws_ec2()
