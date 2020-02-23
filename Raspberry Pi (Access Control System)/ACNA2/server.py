import mysql.connector
import json
import numpy
import datetime
from datetime import date
import decimal

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

from twilio.rest import Client
from configparser import SafeConfigParser

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

from flask import Flask, request, Response, render_template, redirect, url_for, session, jsonify

today = date.today()
current_date = today.strftime("%Y-%m-%d") # Get today's date

configurationFile = SafeConfigParser()
configurationFile.read('acna2_configuration.ini')
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

#Twilio information
account_sid = str(configurationFile['twilio']['account_sid'])
auth_token = str(configurationFile['twilio']['auth_token'])
client = Client(account_sid, auth_token)
my_hp = str(configurationFile['twilio']['my_hp'])
twilio_hp = str(configurationFile['twilio']['twilio_hp'])

# AWS MQTT 
logging.basicConfig()
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

my_rpi.connect()

# Connection to DynamoDB.
try:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    user_table = dynamodb.Table("user")
    access_logs_table = dynamodb.Table("access_logs")
    scanner_table = dynamodb.Table("scanner")
    lcd_display_table = dynamodb.Table("lcd_display")
    leave_table = dynamodb.Table("leave")
    print("Conncted to DynamoDB.")

except Exception as e:
    print(e)

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

class GenericEncoder(json.JSONEncoder):
    
    def default(self, obj):  
        if isinstance(obj, numpy.generic):
            return numpy.asscalar(obj) 
        elif isinstance(obj, datetime.timedelta):  
            return str(obj)
        elif isinstance(obj, datetime.date):   
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:  
            return json.JSONEncoder.default(self, obj) 

def data_to_json(data):
    json_data = json.dumps(data,cls=GenericEncoder)
    return json_data

def fetch_fromdb_as_json(response):    
    try:
        data = []
        for i in response['Items']:
            data.append(dict(i))

        data = {'data':data}

        return data_to_json(data)

    except Exception as e:
        print(e)
        return None

def getCurrentTime():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

app = Flask(__name__)

app.secret_key = 'p1726880 Gideon IOT CA1'

@app.route("/")
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('login'))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    else: 
        if request.method == 'POST':
            try:
                username = request.form.get('username')
                password = request.form.get('pass')
                response = user_table.scan()
                login_success = False
                
                for i in response['Items']:
                    if (i['username'] == username and i['password'] == password):
                        login_success = True
                        session['logged_in'] = True
                        session['username'] = username
                        session['role'] = i['role']
                        return redirect(url_for('index'))

                if login_success == False:
                    return render_template('login.html', login_success=login_success)
            except Exception as e:
                print(e)

        return render_template('login.html')

@app.route("/createAccount", methods = ['GET', 'POST'])
def createAccount():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            if request.method == 'POST':
                try:
                    username = request.form.get('username')
                    password = request.form.get('pass')
                    confirm_pass = request.form.get('confirm_pass')
                    role = request.form.get('role')
                    if request.form.get("accessMain"):
                        accessMain = 1
                    else: 
                        accessMain = 0
                    if request.form.get("accessDatacenter"):
                        accessDatacenter = 1
                    else: 
                        accessDatacenter = 0
                    if request.form.get("accessOffice"):
                        accessOffice = 1
                    else: 
                        accessOffice = 0
                    createAcc_success = True

                    # Check if Password and Confirm Password fields match.
                    if (password != confirm_pass):
                        createAcc_success = False
                        msg = "Passwords do not match."
                        return render_template('create_account.html', createAcc_success=createAcc_success, msg=msg)

                    response = user_table.scan()

                    # Check if username exists in database.
                    for i in response['Items']:
                        if (i['username'] == username):
                            createAcc_success = False
                            msg = "Username already exists in database."
                            return render_template('create_account.html', createAcc_success=createAcc_success, msg=msg)

                    if createAcc_success == True:
                        response = user_table.put_item(
                            Item = {
                                'username': username,
                                'password': password,
                                'role': role,
                                'card_uid': 'xxx',
                                'accessMain': accessMain,
                                'accessOffice': accessOffice,
                                'accessDatacenter': accessDatacenter
                            }
                        )
                        return redirect(url_for('viewUsers'))
                
                except Exception as e:
                    print(e)

            else:
                return render_template('create_account.html')
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('role', None)
    return redirect(url_for('login'))

@app.route("/dashboard")
def dashboard():
    if 'logged_in' in session:
        try:
            # get LCD display default message
            response = lcd_display_table.query(
                KeyConditionExpression=Key('display_id').eq('1') # should only fetch display ID #1
            )
            line_1 = response['Items'][0]['line_1']
            line_2 = response['Items'][0]['line_2']

            response = access_logs_table.scan()
            dates = []
            attendanceData = []

            # Get all dates when at least one person had signed in.
            for i in response['Items']:
                if (i['date'] not in dates):
                    dates.append(i['date'])
            
            dates.sort()

            # Get attendance count per date (grouped by date)
            for date in dates:
                row = []
                username_temp = []
                attendance_count = 0
                for i in response['Items']:
                    if (date == i['date'] and i['username'] not in username_temp):
                        attendance_count += 1
                        username_temp.append(i['username'])
                row.append(attendance_count)
                row.append(date)
                attendanceData.append(row)

            return render_template('dashboard.html', line_1=line_1, line_2=line_2, attendanceData=attendanceData)

        except Exception as e:
            print(e)
    else:
        return redirect(url_for('login'))

@app.route("/getAccessLogs", methods=['POST'])
def getAccessLogs():
    if request.method == 'POST':
        try:
            al_response = access_logs_table.scan()
            sorted_response_by_date = dict(al_response)
            sorted_response_by_date['Items'] = sorted(al_response['Items'], key=lambda x : (x['date'], x['time']), reverse=True) 
            access_logs_json = fetch_fromdb_as_json(sorted_response_by_date)
            loaded_r = json.loads(access_logs_json)

            u_response = user_table.scan()
            total_staff = float(u_response['Count'])

            num_present_staff = 0
            username_temp = []
            for i in al_response['Items']:
                if (i['username'] not in username_temp and i['date'] == current_date):
                    num_present_staff += 1
                    username_temp.append(i['username'])

            attendance = num_present_staff / total_staff * 100 # express total attendance as percentage
            attendance = round(attendance, 2)

            data = {'accesslogs_data': loaded_r, 'current_date': current_date, 'num_present_staff': num_present_staff, 'total_staff': total_staff, 'attendance': attendance}

            return jsonify(data)
        except Exception as e:
            print(e)

@app.route("/userManagement")
def viewUsers():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            try:
                response = user_table.scan()
                all_users = []
                for i in response['Items']:
                    user = []
                    user.append(i['username'])
                    user.append(i['card_uid'])
                    user.append(i['role'])
                    user.append(i['accessMain'])
                    user.append(i['accessDatacenter'])
                    user.append(i['accessOffice'])
                    all_users.append(user)

            except Exception as e:
                print(e)
            return render_template('user_management.html', users=all_users)
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/updateUser", methods = ['GET', 'POST'])
def updateUser():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            if request.method == 'GET':
                try:
                    username = request.args.get('username')
                    response = user_table.query(
                        KeyConditionExpression = Key('username').eq(username)
                    )

                    user = []

                    user.append(response['Items'][0]['username'])
                    user.append(response['Items'][0]['password'])
                    user.append(response['Items'][0]['card_uid'])
                    user.append(response['Items'][0]['role'])
                    user.append(response['Items'][0]['accessMain'])
                    user.append(response['Items'][0]['accessDatacenter'])
                    user.append(response['Items'][0]['accessOffice'])

                    return render_template('update_user.html', username=username, user=user)

                except Exception as e:
                    print(e)

            elif request.method == 'POST':
                try:
                    username = request.form['username']
                    password = request.form['password']
                    confirm_pass = request.form['confirm_pass']
                    role = request.form['role']
                    if request.form.get("accessMain"):
                        accessMain = 1
                    else: 
                        accessMain = 0
                    if request.form.get("accessDatacenter"):
                        accessDatacenter = 1
                    else: 
                        accessDatacenter = 0
                    if request.form.get("accessOffice"):
                        accessOffice = 1
                    else: 
                        accessOffice = 0

                    if (password != confirm_pass):
                        msg = "Passwords do not match."
                        response = user_table.query(
                            KeyConditionExpression = Key('username').eq(username)
                        )

                        user = []

                        user.append(response['Items'][0]['username'])
                        user.append(response['Items'][0]['password'])
                        user.append(response['Items'][0]['card_uid'])
                        user.append(response['Items'][0]['role'])
                        user.append(response['Items'][0]['accessMain'])
                        user.append(response['Items'][0]['accessDatacenter'])
                        user.append(response['Items'][0]['accessOffice'])

                        return render_template('update_user.html', username=username, user=user, updateUser_success=False, msg=msg)

                    else:
                        response = user_table.update_item(
                            Key={
                                'username': username
                            },
                            UpdateExpression = " set password = :p, #role = :r, accessMain = :am, accessDatacenter = :ad, accessOffice = :ao",
                            ExpressionAttributeValues = {
                                ':p': password,
                                ':r': role,
                                ':am': accessMain,
                                ':ad': accessDatacenter,
                                ':ao': accessOffice,
                            },
                            ExpressionAttributeNames = {
                                '#role': 'role'
                            }
                        )
                        return redirect(url_for('viewUsers'))

                except Exception as e:
                    print(e)
        else: 
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/removeUser")
def removeUser():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            try:
                username = request.args.get('username')
                response = user_table.delete_item(
                    Key={
                        'username': username
                    }
                )
            except Exception as e:
                print(e)

            return redirect(url_for('viewUsers'))
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/resetCardUID")
def resetCardUID():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            try:
                username = request.args.get('username')
                response = user_table.update_item(
                    Key={
                        'username': username
                    },
                    UpdateExpression = " set card_uid = :c",
                    ExpressionAttributeValues = {
                        ':c': "xxx"
                    }
                )

            except Exception as e:
                print(e)

            return redirect(url_for('viewUsers'))
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/scannerManagement")
def viewScanners():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            try:
                response = scanner_table.query(
                    KeyConditionExpression=Key('scanner_id').eq('1') # should only fetch display ID #1
                )
                current_location = response['Items'][0]['location']
            except Exception as e:
                print(e)
            return render_template('scanner_management.html', current_location=current_location)
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/updateScanner", methods = ['POST'])
def updateScanner():
    if 'logged_in' in session:
        if session['role'] == 'admin':
            if request.method == 'POST':
                try:
                    scanner_id = request.form.get('scanner_id')
                    location = request.form.get('location')
                    response = scanner_table.update_item(
                        Key={
                            'scanner_id': scanner_id
                        },
                        UpdateExpression = "set #location = :l",
                        ExpressionAttributeValues = {
                            ':l': location
                        },
                        ExpressionAttributeNames = {
                            '#location': 'location'
                        }
                    )
                    
                except Exception as e:
                    print(e)
                
            return redirect(url_for('viewScanners'))
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/updateDefaultMsg", methods = ['POST'])
def updateDefaultMsg():
    if 'logged_in' in session:
        if request.method == 'POST':
            try:
                display_id = request.form.get('display_id')
                line_1 = request.form.get('line_1')
                line_2 = request.form.get('line_2')
                response = lcd_display_table.update_item(
                    Key={
                        'display_id': display_id
                    },
                    UpdateExpression = "set line_1 = :l1, line_2 = :l2",
                    ExpressionAttributeValues = {
                        ':l1': line_1,
                        ':l2': line_2
                    }
                )

                update_LCD_lines = {}
                update_LCD_lines["source"] = "changeLCD"
                update_LCD_lines["line_1"] = line_1
                update_LCD_lines["line_2"] = line_2

                my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(update_LCD_lines), 1)

                #lcd.text("" + line_1, 1)
                #lcd.text("" + line_2, 2)

            except Exception as e:
                print(e)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/clearLCD")
def clearLCD():
    if 'logged_in' in session:
        clear_LCD = {}
        clear_LCD["source"] = "clearLCD"
        my_rpi.publish("ACNA2/MQTT_subscription", json.dumps(clear_LCD), 1)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/pollAbsentStaff")
def pollAbsentStaff():
    if 'logged_in' in session:
        try:
            # Get all staff first and store in absent_staff.
            u_response = user_table.scan()
            absent_staff = []
            for i in u_response['Items']:
                absent_staff.append(i['username'])

            # Retrieve staff who are on leave today.
            l_response = leave_table.scan()
            staff_on_leave_today = []
            for i in l_response['Items']:
                if (i['start_date'] <= current_date <= i['end_date'] and i['approved'] == "true"):
                    staff_on_leave_today.append(i['username'])

                    # Staff on leave are not considered absent, so remove them from absent_staff.
                    if (i['username'] in absent_staff):
                        absent_staff.remove(i['username'])
            
            # Remove staff who have already arrived today from absent_staff.
            al_response = access_logs_table.scan()
            for i in al_response['Items']:
                if (i['date'] == current_date and i['username'] in absent_staff):
                    absent_staff.remove(i['username'])
            
            sms = "{}\nThe following employees are on leave today:\n".format(current_date)
            for username in staff_on_leave_today:
                sms += "-{}\n".format(username)

            current_time = getCurrentTime()
            sms += "\nThe following employees have not arrived as of {}:\n(staff on leave are excluded)\n".format(current_time)
            for username in absent_staff:
                sms += "-{}\n".format(username)

            client.messages.create(to=my_hp, from_=twilio_hp, body=sms)

        except Exception as e:
            print(e)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/applyLeave", methods = ['GET', 'POST'])
def applyLeave():
    if 'logged_in' in session:
        if request.method == 'GET':
            try:
                response = leave_table.query(
                    KeyConditionExpression=Key('username').eq(session['username']) 
                )

                applied_leaves = []
                for i in response['Items']:
                    leave = []
                    leave.append(i['start_date'])
                    leave.append(i['end_date'])
                    leave.append(i['reasons'])
                    leave.append(i['approved'])
                    applied_leaves.append(leave)

                return render_template("apply_for_leave.html", applied_leaves = applied_leaves)

            except Exception as e:
                print(e)

        elif request.method == 'POST':
            try:
                username = request.form.get('username')
                leave_dates = request.form.get('leave_dates')
                leave_start_date = datetime.datetime.strptime(leave_dates[0:10], "%m/%d/%Y").strftime("%Y-%m-%d")
                leave_end_date = datetime.datetime.strptime(leave_dates[-10:], "%m/%d/%Y").strftime("%Y-%m-%d")
                leave_reasons = request.form.get('reasons')

                response = leave_table.put_item(
                    Item = {
                        'username': username,
                        'start_date': leave_start_date,
                        'end_date': leave_end_date,
                        'reasons': leave_reasons,
                        'approved': "false"
                    }
                )

            except Exception as e:
                print(e)
            
            return redirect(url_for('applyLeave'))
    else:
        return redirect(url_for('login'))

@app.route("/approveLeave")
def approveLeave():
    if 'logged_in' in session:
        if session['role'] == "manager":
            try:
                response = leave_table.scan()
                approved_leaves = []
                unapproved_leaves = []
                for i in response['Items']:
                    leave = []
                    leave.append(i['username'])
                    leave.append(i['start_date'])
                    leave.append(i['end_date'])
                    leave.append(i['reasons'])
                    if (i['approved'] == "true"):
                        approved_leaves.append(leave)
                    else:
                        unapproved_leaves.append(leave)

                return render_template("approve_leave.html", approved_leaves = approved_leaves, unapproved_leaves = unapproved_leaves)

            except Exception as e:
                print(e)
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/changeApproval")
def changeApproval():
    if 'logged_in' in session:
        if session['role'] == "manager":
            try:
                username = request.args.get('username')
                start_date = request.args.get('start_date')
                approve = request.args.get('approve')
                response = leave_table.update_item(
                    Key={
                        'username': username,
                        'start_date': start_date
                    },
                    UpdateExpression = " set approved = :a",
                    ExpressionAttributeValues = {
                        ':a': approve,
                    }
                )

                return redirect(url_for('approveLeave'))

            except Exception as e:
                print(e)
        else:
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/profile")
def userProfile():
    if 'logged_in' in session:
        try:
            # Get profile picture URL from S3
            pfp_url = s3_client.generate_presigned_url('get_object',
                                                Params = {
                                                    'Bucket': bucket,
                                                    'Key': 'user_faces/' + session['username'] + '.jpg',
                                                },
                                                ExpiresIn=3600)

            response = user_table.query(
                KeyConditionExpression=Key('username').eq(session['username']) 
            )

            user_details = []
            user_details.append(response['Items'][0]['accessMain'])
            user_details.append(response['Items'][0]['accessDatacenter'])
            user_details.append(response['Items'][0]['accessOffice'])

            return render_template("user_profile.html", user_details = user_details, pfp_url = pfp_url)

        except Exception as e:
            print(e)

    else:
        return redirect(url_for('login'))
    
    
if __name__ == '__main__':
   try:
       http_server = WSGIServer(('0.0.0.0', 5000), app)
       print("Server is listening on port 5000")
       app.debug = True
       http_server.serve_forever()

   except Exception as e:
        print(e)
