import boto3
import botocore
import pandas as pd
import io

# Make sure that the boto3 and botocore are in same version
print("boto3 version:", boto3.__version__)
print("botocore version:", botocore.__version__)


# Assume mlops role
sts_client = boto3.client('sts')

assumed_role = sts_client.assume_role(
    RoleArn= "arn:aws:iam::<aws_account_id>:role/mlops",
    RoleSessionName="S3ReadAccess"
)

# Get credentials
credentials = assumed_role['Credentials']

# Set the creentials for s3 client to fetch the object/file
s3 = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key= credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

# Setup bucket name, file path in bucket and the local path to store
bucket_name = "<put bucket name>"
file_key = "<file path in bucket>"
local_file_path = "<local path>/artifacts/Hotel_Reservations.csv"

# Fetch the file
response = s3.download_file(bucket_name, file_key, local_file_path)

# Use pandas to read the CSV content
df = pd.read_csv(local_file_path)

print(df.head())

