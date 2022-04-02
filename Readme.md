## Launch EC2 instance using boto3

# Introduction
This Script launches ec2 instance using native boto3.

# Pre-requisites 
* Ensure you install the latest version of python and requests package.
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
* We need IAM user access key and secret key to run this script. Please refer AWS documents to create the same (or) follow below steps.
  * Open the IAM console at https://console.aws.amazon.com/iam/.
  * On the navigation menu, choose Users.
  * Choose your IAM user name (not the check box).
  * Open the Security credentials tab, and then choose Create access key.
  * To see the new access key, choose Show. Your credentials resemble the following:
    * Access key ID: AKIAIOSFODNN7EXAMPLE
    * Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    
# To run script

* Execute the below command which will create the ec2 instance at the particular aws region.
```
./createInstance.py -k <AWS_ACCESS_KEY> -s <AWS_SECRET_KEY> --aws_region <AWS_REGION> -t <AWS_INSTANCE_TYPE> -i <AWS_AMI_ID> -n <AWS_TAG_NAME>
```
Example:
```
./createInstance.py -k XXXXXXXX -s XXXXX --aws_region ap-south-1 -t t2.micro -i ami-04505e74c0741db8d -n test_aws
```

Notes:
* The script contains two classes :
  * aws_ec2 -> Which will create the key pair, security group which opens 22(SSH) port, and launch the instance in the respective region.
  * install_application -> Which will connect to respective instance and execute the commands `sudo apt update`
  
# Security:

* The security group has only  22 port.
* AWS key and secret key are not stored anywhere in the script,it is taken from the command line.

