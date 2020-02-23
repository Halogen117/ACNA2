from threading import Thread
from time import sleep
from picamera import PiCamera
from configparser import SafeConfigParser
import boto3
import botocore

configurationFile = SafeConfigParser()
configurationFile.read('acna2_configuration.ini')

rekognition = boto3.client('rekognition',"us-east-1")
s3 = boto3.resource('s3')
camera = PiCamera()
image_path = "/home/pi/Desktop/tmp.jpg"

# Connection to Amazon S3 Bucket
print("Locating Amazon S3 Bucket...")

bucket = str(configurationFile['aws_configuration']['bucket_name'])
print(bucket)

bucket_exists = True
try:
    s3.meta.client.head_bucket(Bucket=bucket)

except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        bucket_exists = False

if bucket_exists == False:
    print("Bucket not found. Creating...")
    s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
else:
    print("S3 Bucket found.")

class uploadImage(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    # To run the thread that uploads image from PiCam every 10 seconds
    def run(self):
        while True:
            sleep(10)
            try:
                print("Taking photo now...")
                camera.capture(image_path)
                sleep(3)
                fp = open(image_path, 'rb')
                image_string = fp.read()
                response = rekognition.detect_faces(Image={"Bytes": image_string,},Attributes=['ALL'])
                if len(response['FaceDetails']) <= 0: # Not face.
                    print("Face not detected.") 
                else: 
                    print("Face detected! Uploading to S3...")
                    s3.Object(bucket, "tmp.jpg").put(Body=open(image_path, 'rb'))
                    sleep(3)
                    print("Photo uploaded to S3.")
            except Exception as e:
                print(e)
