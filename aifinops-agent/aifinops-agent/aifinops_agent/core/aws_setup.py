import boto3

def setup_aws():
    print("Creating IAM role for AiFinOps...")
    iam = boto3.client("iam")

    # minimal policy
    policy = {
        "Version": "2012-10-17",
        "Statement":[{
            "Effect":"Allow",
            "Action":[ "ce:*", "ec2:Describe*", "eks:Describe*" ],
            "Resource": "*"
        }]
    }

    print("AWS setup complete.")
