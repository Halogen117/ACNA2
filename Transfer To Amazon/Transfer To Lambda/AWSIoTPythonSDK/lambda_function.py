import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
from boto3.dynamodb.conditions import Key, Attr
scanner_location = "" # Main, Datacenter, or Office
access_location = "" # To check the user's access rights for the locations above (0 = denied, 1 = allowed); accessMain, accessDatacenter, or accessOffice# Connection to DynamoDB.
msg = "" # Success or Failed
# Connection to DynamoDB.
try:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    user_table = dynamodb.Table("user")
    access_logs_table = dynamodb.Table("access_logs")
    scanner_table = dynamodb.Table("scanner")
    print("Conncted to DynamoDB.")

except Exception as e:
    print(e)
    
def getScannerLocation():
    try:
        print("Current scanner location:")

        response = scanner_table.query(
            KeyConditionExpression=Key('scanner_id').eq('1') # should only fetch scanner ID #1
        )

        scanner_location = response['Items'][0]['location']

        print(scanner_location)

        access_location = "access" + scanner_location

        return scanner_location, access_location
    
    except Exception as e:
        print(e)

def check_access_rights(username):
    msg_return = ""
    scanner_location, access_location = getScannerLocation() # Get the location the scanner is set to
    response = user_table.scan()
    for i in response['Items']:
        if (i['username'] == username):
            access_check = i[access_location]
            break
    
    if access_check == 1:
        print("Access Granted! Logging entry to database...")
        msg_return = "Success"
                    
    else:
        print("Access Denied! Logging entry to database...")
        msg_return = "Failure"
    return msg_return, scanner_location

# To insert code to publish username and msg(Success/Failure) in MQTT.


def lambda_handler(event, context):
    print(event["responsePayload"])
    print('Loading function')
    
    response_from_lambda = event["responsePayload"]
    host = "aXXXXXXXXX-ats.iot.us-east-1.amazonaws.com" # Change this value to your AWS Thing endpoint
    rootCAPath = "ACNA2-rootca.pem"
    certificatePath = "ACNA2-certificate.pem.crt"
    privateKeyPath = "ACNA2-private.pem.key"
    
    my_rpi = AWSIoTMQTTClient("PubSub-p1726765")
    my_rpi.configureEndpoint(host, 8883)
    my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
    my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
    my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
    my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
    
    
    my_rpi.connect()

    message_to_send = {}
    message_to_send["source"] = "rekog"
    """
    if response_from_lambda == "right_directory_no_match":
        message_to_send["message"] = "right_directory_no_match"
        my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(message_to_send), 1)
        print("It went to the right directory but no faces matched!")

    elif response_from_lambda == "tmp_was_not":
        message_to_send["message"] = "tmp_was_not_face"
        my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(message_to_send), 1)
        print("The temporary image was not a face!")
        
    elif response_from_lambda == "wrong_directory_right_face":
        message_to_send["message"] = "user_face_right_face"
        my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(message_to_send), 1)
        print("The face added was a face and saved in the directory!")
        
    elif response_from_lambda == "wrong_directory_not_face":
        message_to_send["message"] = "user_face_not_face"
        my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(message_to_send), 1)
        print("The face was not added as a face and not saved in the directory!")
    """
        
    response_from_lambda = response_from_lambda.replace("user_faces/","")
    response_from_lambda = response_from_lambda.replace(".jpg","")
    msg, scanner_location = check_access_rights(response_from_lambda)
    message_to_send["user_name"] = response_from_lambda
    message_to_send["message"] = msg
    message_to_send["scanner_location"] = scanner_location
    my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(message_to_send), 1)
    print("Temporary match was valid and matched with someone!")
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
