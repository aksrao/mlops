import boto3
import pandas as pd
import io

sts_client = boto3.client('sts')