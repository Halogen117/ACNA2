from __future__ import print_function
import boto3
import botocore
from decimal import Decimal
import json
import urllib

print('Loading function')

rekognition = boto3.client('rekognition',"us-east-1")
s3 = boto3.resource('s3')


def detect_A_Face(bucket,face_name,region="us-east-1"):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": face_name}},Attributes=['ALL'])
    if len(response['FaceDetails']) <= 0:
        return "not_face"
    else:
        """
        for faceDetail in response['FaceDetails']:
            print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
                + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        """
        return "a_Face"
    
    
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        my_bucket = s3.Bucket(bucket)
        if  "user_faces/" not in str(key):
            print("Found outside user_face directory! Checking your face")
    
            if detect_A_Face(bucket,key) == "not_face":
                print("False due to not being a face!")
                obj = s3.Object(bucket, key)
                obj.delete()
                print("Sucess in deleting")
                return "tmp_was_not"
        
            # Finds the images that are inside the user_faces
            # Need to grant access to dynamoDB
            for item in my_bucket.objects.all():
                if  "user_faces/" in str(item.key) and ".jpg" in str(item.key):
                    print("The face to analyse is "+str(item.key))
                    response = rekognition.compare_faces(
                                SourceImage={
                                    "S3Object" :{
                                        "Bucket" : bucket,
                                        "Name" : key
                                    }
                                },
                                TargetImage={
                                    "S3Object" :{
                                        "Bucket" : bucket,
                                        "Name" : item.key
                                    }
                                },
                                SimilarityThreshold=80
                    )
                    for record in (response['FaceMatches']):
                        face = record
                        confidence = face["Face"]
                        print("Matched with {} Similarity".format(face['Similarity']))
                        print("Matched with {} Confidence".format(confidence['Confidence'])) 
                        print("We have a match! It's "+str(item.key))
                        # Lambda will send back a message to Gideon's raspberry pi indicating success
                        obj = s3.Object(bucket, key)
                        obj.delete()
                        return item.key
            
            print("IF you got this far, it means that there were no matches present!")
            # Unfortunately, if it got sent here, then it wil fail
            obj = s3.Object(bucket, key)
            obj.delete()
            return "right_directory_no_match"
        
        else:
            print("Found in the directory!")
            if detect_A_Face(bucket,key) == "not_face":
                # Delete the image from the face of existance
                obj = s3.Object(bucket, key)
                obj.delete()
                print("Sucess in deleting")
                return "wrong_directory_not_face"
            else:
                print("Success in saving")
             # If nothing else send back success in storing image!
                return "wrong_directory_right_face"

    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

