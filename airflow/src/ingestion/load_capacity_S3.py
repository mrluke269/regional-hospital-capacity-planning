import boto3
import json
from datetime import datetime

s3_client = boto3.client('s3')
bucket_name = "hospital-planning-raw-luke"

def load_capacity_S3(data):
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"hospital_capacity_{today}.json"
    
    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(data),
    )
    print(f"Data uploaded to s3://{bucket_name}/{key}")
    return key

if __name__ == "__main__":
    import extract_hospital_capacity
    data = extract_hospital_capacity.extract_hospital_capacity(max_records=2)
    load_capacity_S3(data)
    print("Upload complete.")
        