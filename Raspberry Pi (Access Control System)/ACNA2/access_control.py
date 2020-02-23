import RPi.GPIO as GPIO
import MFRC522
import signal
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
from boto3.dynamodb.conditions import Key, Attr
import botocore
import sys

from utility.thread_face_upload import uploadImage

from time import sleep
import logging

from twilio.rest import Client
from configparser import SafeConfigParser

configurationFile = SafeConfigParser()
configurationFile.read('acna2_configuration.ini')

#Twilio information
account_sid = str(configurationFile['twilio']['account_sid'])
auth_token = str(configurationFile['twilio']['auth_token'])
client = Client(account_sid, auth_token)
my_hp = str(configurationFile['twilio']['my_hp'])
twilio_hp = str(configurationFile['twilio']['twilio_hp'])

# AWS MQTT 
mqtt_host = str(configurationFile["dynamoDB_configuration"]["host"])
mqtt_rootCAPath = str(configurationFile["dynamoDB_configuration"]["rootCAPath"])
mqtt_certificatePath = str(configurationFile["dynamoDB_configuration"]["certificatePath"])
mqtt_privateKeyPath = str(configurationFile["dynamoDB_configuration"]["privateKeyPath"])
mqtt_PubSub = str(configurationFile["dynamoDB_configuration"]["Pub-Sub"])

my_rpi = AWSIoTMQTTClient(mqtt_PubSub)
my_rpi.configureEndpoint(mqtt_host, 8883)
my_rpi.configureCredentials(mqtt_rootCAPath, mqtt_privateKeyPath, mqtt_certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

card_uid = None
prev_card_uid = None 
continue_reading = True
scanner_location = "" # Main, Datacenter, or Office
access_location = "" # To check the user's access rights for the locations above (0 = denied, 1 = allowed); accessMain, accessDatacenter, or accessOffice

# Connection to DynamoDB.
try:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    user_table = dynamodb.Table("user")
    access_logs_table = dynamodb.Table("access_logs")
    scanner_table = dynamodb.Table("scanner")
    print("Conncted to DynamoDB.")

except Exception as e:
    print(e)

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    #lcd.clear()
    GPIO.cleanup()
    sys.exit()

def getScannerLocation():
    try:
        print("Current scanner location:")

        response = scanner_table.query(
            KeyConditionExpression=Key('scanner_id').eq('1') # should only fetch scanner ID #1
        )

        scanner_location = response['Items'][0]['location']

        print(scanner_location)

        access_location = "access" + scanner_location
        print("You may scan the Access Card now.")

        return scanner_location, access_location
    
    except Exception as e:
        print(e)

# Main
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()

print("Press Ctrl+C to terminate program.")
print("Access Control system is running...")

# Start thread to upload image every 10 seconds for facial recognition service in Lambda.
print("PiCamera will upload image every 10 seconds.")
uploadImage = uploadImage()

logging.basicConfig()
my_rpi.connect()
scanner_location, access_location = getScannerLocation() # Get the location the scanner is set to

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
            try: 
                card_uid_string = str(card_uid)
                response = user_table.scan()
                card_exists = False
                for i in response['Items']:
                    if (i['card_uid'] == card_uid_string):
                        username = i['username']
                        access_check = i[access_location]
                        card_exists = True
                        break

                if card_exists == False:
                    print("Card not found in database. Please try again...")
                    prev_card_uid = "xxx" # Reset card uid for next scan.
                    continue

                if access_check == 1:
                    print("Access Granted! Logging entry to database...")
                    msg = "Success"
                    
                else:
                    print("Access Denied! Logging entry to database...")
                    msg = "Failure"

                sendToDoor = {}
                sendToDoor["source"] = "cardAccessAttempt"
                sendToDoor["user_name"] = username
                sendToDoor["message"] = msg
                sendToDoor["scanner_location"] = scanner_location
                sleep(3)
                my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(sendToDoor), 1)

                scanner_location, access_location = getScannerLocation() # Get location of scanner again just in case it has been changed through the Web UI
                prev_card_uid = "xxx" # reset card uid for next scan
                continue
            except Exception as e:
                print(e)