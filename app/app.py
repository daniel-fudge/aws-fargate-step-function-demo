from boto3 import client
from json import dumps
from time import sleep, time


s3 = client('s3')


# The business logic to be called from either Lambda or Fargate
def timer(job_id: str, duration: int, bucket: str):
    start = time()
    for _ in range(duration):
        sleep(1)

    body = dumps({"duration": round(time() - start, 1)})

    s3.put_object(Body=body, Bucket=bucket, Key=f'test-{job_id}.json')

    return {'statusCode': 200, 'body': body}


# The normal Lambda handler
def lambda_handler(event, _):
    return timer(job_id=event["job_id"], duration=event["duration"], 
                 bucket=event["bucket"])


# This can be used from Fargate by overriding CMD in the Docker image with:
#    'command': ['app.py', '--job_id', id, '--duration': duration, '--bucket': bucket]
 
if __name__ == '__main__':

    import argparse

    
    parser = argparse.ArgumentParser(description='Simple demo timer function.')
    parser.add_argument('-j', '--job_id', type=str, required=True, help='The job id.')
    parser.add_argument('-d', '--duration', type=int, required=True, help='Duration in seconds.')
    parser.add_argument('-b', '--bucket', type=str, required=True, help='Bucket to write file.')
    args = vars(parser.parse_args())

    print(args)

    timer(job_id=args["job_id"], duration=args["duration"], bucket=args["bucket"])
