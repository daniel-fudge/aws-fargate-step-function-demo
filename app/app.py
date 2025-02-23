from boto3 import client
from json import dumps
from time import sleep, time


s3 = client('s3')

def lambda_handler(event, _):

    job_id = event["job_id"]
    duration = event["duration"]
    bucket = event["bucket"]

    start = time()
    for _ in range(duration):
        sleep(1)

    body = dumps({"duration": round(time() - start, 1)})

    s3.put_object(
        Body=body,
        Bucket=bucket,
        Key=f'test-{job_id}.json'
    )

    return {
        'statusCode': 200,
        'body': body
    }
