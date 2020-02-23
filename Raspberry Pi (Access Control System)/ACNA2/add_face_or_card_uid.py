import RPi.GPIO as GPIO
import MFRC522
import signal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import botocore
import sys

from configparser import SafeConfigParser
from time import sleep
from picamera import PiCamera

configurationFile = SafeConfigParser()
configurationFile.read('acna2_configuration.ini')
s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition',"us-east-1")

continue_reading = True
enter_update_choice = True
image_path = "/home/pi/Desktop/upload_staff_face.jpg"

camera = PiCamera()

# Connection to DynamoDB.
try:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    user_table = dynamodb.Table("user")
    print("Conncted to DynamoDB.")

except Exception as e:
    print(e)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    sys.exit()

# Lists existing users in database and returns user_id for user the user to be updated.
def prompt_username():
    print("Listing users...\n")
    response = user_table.scan()
    
    print("<Username> : <Card UID>")
    for i in response['Items']:
        print(i['username'] + " : " + i['card_uid'])

    enter_username = True
    while enter_username:
        username = raw_input("\nFirst, enter the Username of the user to be updated: ")
            # TO implement check if user exists in database or not.
        for i in response['Items']:
            if (i['username'] == username):
                print("You are updating Username: {}".format(username))
                enter_username = False
                return username
        print("User does not exist in database! Please try again.")

def update_card_uid():
    global continue_reading
    card_uid = None
    prev_card_uid = None 
    username = prompt_username()
    
    print("You may scan the Access Card now.")
    # This loop keeps checking for chips.
    # If one is near it will get the UID

    while continue_reading:
        
        # Scan for cards    
        (status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

        # If a card is found
        if status == mfrc522.MI_OK:
            # Get the UID of the card
            (status,card_uid) = mfrc522.MFRC522_Anticoll()
            if card_uid!=prev_card_uid:
                prev_card_uid = card_uid
                print("Access Card detected! UID of card is {}".format(card_uid))
                confirmation = raw_input("Add to database? Press Y to add, N to scan again. ")
                if confirmation == 'Y':
                    card_uid_string = str(card_uid) # Convert to string first
                    card_exists = False
                    try:
                        response = user_table.scan()
                        for i in response['Items']:
                            if (i['card_uid'] == card_uid_string):
                                prev_card_uid = "xxx" # reset card uid
                                card_exists = True
                            
                        if (card_exists == False):
                            response = user_table.update_item(
                                Key={
                                    'username': username
                                },
                                UpdateExpression= " set card_uid = :c",
                                ExpressionAttributeValues={
                                    ':c': card_uid_string,
                                }
                            )

                            print("Added")
                            continue_reading = False
                            GPIO.cleanup()
                        
                        else:
                            print("Card UID already exists in database! Please try another card.") 
                            print("Starting another scan...")
                            print("You may scan the Access Card now.")
                            continue
                        
                    except Exception as e:
                        GPIO.cleanup()
                        print(e)
                else:
                    prev_card_uid = "xxx" # reset card uid
                    print("Starting another scan...")
                    print("You may scan the Access Card now.")
                    continue

def update_faces():
    username = prompt_username()
    print("Taking photo now...")
    take_photo_with_PiCam()
    fp = open(image_path, 'rb')
    image_string = fp.read()
    checkFace = detect_face(image_string)
    if checkFace == True:
        print("Face detected! Uploading to S3...")
        s3.Object(bucket, "user_faces/{}.jpg".format(username)).put(Body=open(image_path, 'rb'))
        print("Image uploaded for Username {}".format(username))
    else:
        print("Face not detected. Please try again.")
        update_faces()

def take_photo_with_PiCam():
    sleep(3)
    camera.capture(image_path)
    sleep(3)

def detect_face(image_string):
    response = rekognition.detect_faces(Image={"Bytes": image_string,},Attributes=['ALL'])
    if len(response['FaceDetails']) <= 0:
        return False
    else: 
        return True

# Main
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()

print("Welcome to ACNA 2.0. This program is used to add/update Faces and RFID Card UIDs to existing users.")
print("Press Ctrl+C to terminate program.")
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

while enter_update_choice:
    print("Would you like to add/update Face or Card UID details? Enter 1 or 2.")
    print("1. Face")
    print("2. Card UID")
    user_request = raw_input(">")
    if user_request == '1':
        print("Updating: Face.")
        enter_update_choice = False
        update_faces()
    elif user_request == '2':
        print("Updating: Card UID.")
        enter_update_choice = False
        update_card_uid()
    else:
        print("Input not recognized, please try again.")

