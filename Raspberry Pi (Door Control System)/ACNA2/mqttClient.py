from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime, time
from time import sleep
from gpiozero import MCP3008
from gpiozero import Buzzer
from rpi_lcd import LCD
import boto3
from boto3.dynamodb.conditions import Key, Attr
from twilio.rest import Client
from configparser import SafeConfigParser
import logging
import json
import uuid
configurationFile = SafeConfigParser()
configurationFile.read('acna2_configuration.ini')

#Twilio information
account_sid = str(configurationFile['twilio']['account_sid'])
auth_token = str(configurationFile['twilio']['auth_token'])
client = Client(account_sid, auth_token)
my_hp = str(configurationFile['twilio']['my_hp'])
twilio_hp = str(configurationFile['twilio']['twilio_hp'])

today = date.today()
current_date = today.strftime("%Y-%m-%d") # Get today's date
start_work = time(9, 0, 0) # Start work at 9:00 AM.
end_day = time(23, 59, 59) # Day ends at 11:59:59 PM.
# I will need gideon to run his publisher
# Custom MQTT message callback

def logEntry(username, msg, scanner_location):
    try:
        first_signin = True
        response = access_logs_table.scan()
        for i in response['Items']:
            if (i['username'] == username and i['date'] == current_date): # Check whether it's the first sign-in of the day for that user
                first_signin = False

        now = datetime.now()
        nowToTime = now.time()

        # Check if the staff clocked in late. If they did, send an SMS via Twilio.
        # 1. Check whether the sign-in was done between 9:00 AM - 11:59:59 PM.
        # 2. Check whether it is the user's first sign-in of the day.
        if(start_work < nowToTime <= end_day and first_signin == True):
            print("You are late!")
            sms = "{0} is late for work. First sign-in of the day at: {1}.".format(username, now)
            client.messages.create(to=my_hp, from_=twilio_hp, body=sms)
            print("Alert sent to {}.".format(my_hp))

        current_time = now.strftime("%H:%M:%S")
        log_id = str(uuid.uuid1())

        response = access_logs_table.put_item(
            Item = {
                'log_id': log_id,
                'username': username,
                'date': current_date,
                'time': current_time,
                'result': msg,
                'area_accessed': scanner_location
            }
        )

        print("Logging successful.")

    except Exception as e:
        print("Logging failed.")
        print(e)

def displayDefaultMsg():
    response = lcd_display_table.query(
        KeyConditionExpression = Key('display_id').eq('1')
    )
    line_1 = response['Items'][0]['line_1']
    line_2 = response['Items'][0]['line_2']

    lcd.text("" + line_1,1)
    lcd.text("" + line_2,2)

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    message_from_lambda = json.loads(message.payload)
    if message_from_lambda["source"] == "rekog" or message_from_lambda["source"] == "cardAccessAttempt":
        if message_from_lambda["message"] == 'Success':
            # Buzz the buzzer
            bz.on()
            sleep(1)
            bz.off()

            lcd.text("Access Granted!",1)
            lcd.text("Welcome " + str(message_from_lambda["user_name"]),2)

        elif message_from_lambda["message"] == 'Failure':

            # Buzz the buzzer
            bz.on()
            sleep(2)
            bz.off()

            lcd.text("Access Denied!",1)
            lcd.text("" ,2)

        sleep(5)
        logEntry(message_from_lambda["user_name"], message_from_lambda["message"], message_from_lambda["scanner_location"])
        displayDefaultMsg()


        """
        # This is for checking if the upload was successful
        elif message_from_lambda["message"] == "user_face_right_face":
            print("Upload to user_faces was complete!")

        elif message_from_lambda["message"] == "user_face_not_face":
            print("The upload to user_faces was not complete as it was not registered as a face!")
            
        elif message_from_lambda["message"] == "tmp_was_not_face":
            print("The temporary image uploaded to verify was not an image!")

        else:
            # Buzz the buzzer
            bz.on()
            sleep(2)
            bz.off()

            lcd.text("Access Denied!",1)
            lcd.text("" ,2)
        """

    elif message_from_lambda["source"] == "changeLCD":
        line_1_MQTT = message_from_lambda["line_1"]
        line_2_MQTT = message_from_lambda["line_2"]
        lcd.text("" + line_1_MQTT,1)
        lcd.text("" + line_2_MQTT,2)

    
    elif message_from_lambda["source"] == "clearLCD":
        lcd.clear()


# Connection to DynamoDB.
print("Turning on the door")
try:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    user_table = dynamodb.Table("user")
    access_logs_table = dynamodb.Table("access_logs")
    scanner_table = dynamodb.Table("scanner")
    lcd_display_table = dynamodb.Table('lcd_display')
    print("Connected to DynamoDB.")
except Exception as e:
    print(e)


bz = Buzzer(5)
# LCD display grants access
lcd = LCD()
displayDefaultMsg()

host = str(configurationFile["dynamoDB_configuration"]["host"])
rootCAPath = str(configurationFile["dynamoDB_configuration"]["rootCAPath"])
certificatePath = str(configurationFile["dynamoDB_configuration"]["certificatePath"])
privateKeyPath = str(configurationFile["dynamoDB_configuration"]["privateKeyPath"])
try:
    my_rpi = AWSIoTMQTTClient(str(configurationFile["dynamoDB_configuration"]["Pub-Sub"]))
    my_rpi.configureEndpoint(host, int(configurationFile["dynamoDB_configuration"]["port"]))
    my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
    my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
    my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    my_rpi.connect()
    my_rpi.subscribe("ACNA2/MQTT_subscription", 1, customCallback)
except Exception as e:
    print(e)
    print("Unable to connect AWS! Exiting code!")
    exit()

logging.basicConfig()
print("Successfully connected! Now subscribing to services")
while True:

    sleep(1)
    




