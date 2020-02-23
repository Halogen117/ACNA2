## ST0324 Internet of Things CA2 Step-by-step Tutorial
## SCHOOL OF COMPUTING (SOC)

# IOT CA2 ACNA2
# Step-by-step Tutorial

### DIPLOMA IN INFOCOMM SECURITY MANAGEMENT
### ST0324 Internet of Things (IOT)
### 2019/2020 Semester 1

#### Date of Submission :
23rd February 2020

#### Prepared for : 
Dora Chua Heok Hoon

#### Class:
DISM/FT/3A/41

#### Submitted By : 
| Student ID | Name                  |
| ---------- | --------------------- |
| 1726880    | Gideon Soon Yang Jing |
| 1726765    | Russel Tan Jun Hong   |

---

## Table of Contents
1. Overview of ACNA 2.0
  * Where we have uploaded our tutorial
  * What is the application about?
  * How does the final RPI set-up looks like?
  * How does the web application look like?
  * System architecture of ACNA 2.0
  * Evidence that we have met basic requirements
  * Bonus features on top of basic requirements
  * Quick-start guide (Readme first)
2. Hardware requirements
  * Hardware checklist
  * Hardware setup instructions
  * Fritzing Diagram
3. Software Requirements
  * Software checklist
  * Software setup instructions
  * Creating a Thing (AWS)	
  * Creating a Policy (AWS)	
  * Attaching the policy to the certificate and thing (AWS)	
  * Configuring the AWS IOT role (AWS)	
  * Creating the DynamoDB tables (AWS)	
  * Creating the S3 Bucket (AWS)	
  * Configuring the role for Lambda (AWS)	
  * Creating the 'Rekog' Lambda function (AWS)	
  * Creating the 'Publishing' Lambda function (AWS)	
  * Triggering the 'Rekog' Lambda function to run the 'Publishing' Lambda function (AWS)	
  * Access Control System	
  * Door Control System	
4. Expected Results  

## Section 1 : Overview of project
This section will cover about the overview of the entirety of the project, which includes what is it about and the requirements needed to fulfill.

### Where we have uploaded our tutorial
The table below provides the public tutorial link and the YouTube link where the video of the demonstration has been uploaded to.
|                         | Link                                        |
| ----------------------- | ------------------------------------------- |
| YouTube                 | https://www.youtube.com/watch?v=xVEgjQvqfps |
| Public tutorial link    | https://github.com/Halogen117/ACNA2         |

### What is ACNA 2.0 about
Before talking about ACNA 2.0, one must first be familiar with the original project, ACNA. The Access Control N Attendance (ACNA) System project was originally created to control the areas where each staff is allowed to access, as well as to track the time when they enter and leave their respective areas in order to bolster the purpose of auditing and monitoring. The application is intended for organisations looking to enforce physical security in order to protect its assets and keep track of staff attendance.

Now, from the team The 24th - Acaroduh Legion, which consists of team members Gideon Soon and Russel Tan, this Internet Of Things (IOT) project was initiated to expand the functionalities of the original ACNA System, with the addition of new features and MQ Telemetry Transport (MQTT) Protocol to make it scalable and improve the user experience.

There are two important components of the ACNA 2.0, represented by their own individual Raspberry Pi. The first is the Access Control System which contains the hardware and software for receiving and processing sensor data. The second component is the Door Control System which contains the hardware and software for processing and outputting data through its actuators.


### How does the final RPI set-up looks like?

#### Figure 1: Access Control System
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/real_access_control.jpg "Real RPI Access Control")
 
#### Figure 2: Door Control System
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/real_door_control.jpg "Real RPI Door Control")
 
### How does the web application look like?

#### Figure 3: Login Page
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/01_login_page.png "Login Page")

#### Figure 4: Dashboard Page
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02_dashboard.png "Dashboard Page")

#### Figure 5: Real-time Access Logs (Dashboard)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02a_access_logs_(real-time_values_from_sensor).png "Access logs")

#### Figure 6: Historical Attendance Graph (Dashboard)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02b_attendance_(historical_values_from_sensor).png "Attendance Graph")

#### Figure 7: LCD Display Settings (Dashboard)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02c_lcd_display_settings_(control_state_of_actuator).png "lcd settings")

#### Figure 8: Navigation Sidebar (Normal user view)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02d_nav_sidebar_(normal_user_view).png "Nav side Normal User")

#### Figure 9: Navigation Sidebar (Administrator user view)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02e_nav_sidebar_(admin_user_view).png "Nav sidebar Admin User")

#### Figure 10: Navigation sidebar (Manager user view)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/02f_nav_sidebar_(manager_view).png "Nav sidebar Manager User")

#### Figure 11: User Management Page (Only accessible by Admin)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/03_user_management_(admin_only).png "User management")

#### Figure 12: Update User Page (Only accessible by Admin)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/04_update_user_(admin_only).png "User Page update")

#### Figure 13: Create New User Page (Only accessible by Admin)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/04a_create_account_(admin_only).png "User Page update")

#### Figure 14: Scanner Management Page (Only accessible by Admin)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/06_scanner_management.png "Scanner management")

#### Figure 15: User Profile Page
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/07_user_profile.png "User profile page")

#### Figure 16: Apply for Leave Page (#1)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/08a_apply_for_leave.png "Applying for leave page")

#### Figure 17: Apply for Leave Page (#2 – Date range selector displayed)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/08b_apply_for_leave_(with_date_range_selector).png "Applying for leave with date range selector")

#### Figure 18: Approval of Leave Page (Only accessible by Manager)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/09_approval_of_leaves_(manager_only).png "Applying for leave page")

#### Figure 19: Twilio alert to notify when staff are late
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/twilio_alert_when_staff_are_late.jpg
 "Twilio late alert")
 
#### Figure 20: Twilio alert to indicate staff who are absent (#1 - when no one has signed in yet)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/twilio_poll_for_absent_staff_(1).jpg
 "Twilio alert to indicate staff who are absent")

#### Figure 21: Twilio alert to indicate staff who are absent (#2 - when some staff have already signed in)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/website_images/twilio_poll_for_absent_staff_(2).jpg
 "Twilio alert to indicate staff who are absent")

### System architecture of ACNA 2.0

The images below, labelled figures 22-28, describes the overall system architecture of ACNA 2.0.

#### Figure 22: Technologies Used
For our system, we have two Raspberry Pi, with one representing the Access Control System and one representing the Door Control System. 

We used Flask to serve our Web Server and render the Web UI, AWS MQTT IoT Client as the platform to enable our MQTT communication, DynamoDB for our cloud database, and we also have several cloud services AWS S3 Bucket, Lambda and Rekognition API. We also have a built-in alert system running on Twilio.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/0_technologies_used.png "Technologies used")

#### Figure 23: Card Access Control Workflow
The Door Control System subscribes to the AWS MQTT broker and the topic 'ACNA2/MQTT_subscription' (which will be used for all of our MQTT communications). When the user scans their card, the Access Control System will check if the user has access rights to the location they are trying to access by retrieving their access rights from the database. It will then publish the result of whether the user has been granted or denied access to the MQTT broker, who will then send the result to the Door Control System. After which, the Door Control System will then display "Access Granted" or "Access Denied", based on the received result. Lastly, it will log the access attempt to the DynamoDB database, including the name of the user, the location they are trying to access, whether they have been granted or denied access, and the date and time of the attempt.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/1_card_access_control.png "Card Access control")

#### Figure 24: Face Access Control Workflow
The Access Control System will use the PiCamera to take a picture and upload the face to AWS S3 Bucket if it detects a face in the picture captured. Once the picture is uploaded, an AWS Lambda function is automatically triggered to retrieve the stored user faces from S3 and call the AWS Rekognition API to detect if the face captured from the Access Control System matches any of the stored user faces in S3. If it does, the Lambda function will retrieve the identified user's access rights from the database and then check if the user is allowed to access the location they are trying to access, then publish the result of whether they have been granted or denied access to the MQTT broker. The result is then sent to the Door Control System, which will display "Access Granted" or "Access Denied", based on the received result. Afterwards, it will also log the access attempt to the DynamoDB database, like the “Card Access Control” feature.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/2_face_access_control.png "Face access")

#### Figure 25: Website User Interface Workflow
The Flask Web server will retrieve user information, access logs and any other necessary information from the DynamoDB database to be displayed to the user. For example, Flask retrieves the access logs generated by the Door Control System from the database and displays them to the user in the form of a table in real-time using AJAX and Google Visualization. Flask also retrieves the historical attendance values for each date and displays them in the form of a bar graph using ChartJS. Additionally, whenever a user makes any updates to the database, such as creating a new user account or applying for leave, it will also store these updates into the database.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/3_Web_UI.png "Website User Interface")

#### Figure 26: Control LCD Message Workflow 
Once the Door Control System boots up, it will retrieve the message from the database to be displayed by default. However, from the Web UI, the user may change the default message. This is done by submitting a form containing the updated message to Flask, which will publish the new default message to the MQTT broker, who will then send the message to the Door Control System, which will then display the new default message immediately. The user may also clear the LCD display message, which follows a similar procedure.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/4_control_LCD_message.png "Control LCD")

#### Figure 27: Twilio Alerts Workflow
Lastly, there is a built-in alert system based on Twilio, which will send alerts in the form of an SMS to my mobile phone. There are two alerts that Twilio handles. Firstly, when the Door Control System detects that a user has signed in to work late (i.e. after 9:00 AM), it will automatically send an alert to my phone to inform me which user was late. As a bonus feature, through the Web UI, the user can also poll the database to examine who are on leave that day and who have not arrived to work yet, which will be sent as an SMS to my phone.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/5_twilio_alerts.png "Twilio alert")

#### Figure 28: Full System Architecture
And this is the complete system architecture.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/architecture_images/6_full_system_arch.png "Full system architecture")
 
### Figure 29: Evidence that we met the basic requirements
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/evidence.png "Basic Requirements met")

### Bonus features on top of basic requirements
1)	We have an ‘Apply For Leave’ system where staff can apply for leave and managers can approve their leave through the Web UI. This also led to a modification of the existing ‘Poll Database for Absent Staff’ feature, which previously only checked for staff who has not arrived. Now, it checks for staff who are on leave today. It then sends the data in the form of an SMS via Twilio. 
This feature is considered ‘Advanced’.

2)	We have a ‘User Profile’ feature where staff can view information about themselves through the Web UI, including the profile picture retrieved from an S3 bucket. 
This feature is considered ‘Intermediate’.

3)	We implemented three out of the two required cloud services in our system, specifically storing images in AWS S3 Bucket, image recognition via AWS Rekognition, and serverless computing via AWS Lambda. 
This feature is considered ‘Advanced.’

### Quick-start guide (Readme first)
1)	On the Access Control System and Door Control System, edit the ACNA2-configuration.ini files to suit the needs of the user. The ACNA2-configuration.ini are located in the **Raspberry Pi (Access Control System)\ACNA2** and the **Raspberry Pi (Door Control System)\ACNA2** folders respectively.
2) On the Access Control System and Door Control System, download the requirements.txt file and their dependencies by running the command:  *pip install -r “requirements.txt”*. The requirements.txt files are located in the **Raspberry Pi (Access Control System)\ACNA2** and the **Raspberry Pi (Door Control System)\ACNA2** folders respectively.
3)	On the Access Control System and Door Control System, ensure that the AWS credentials (~/.aws/credentials) are updated for both Raspberry Pi.
4)	On the Door Control System, launch the mqttClient.py by running the following command: *“python mqttClient.py”*. The mqttClient.py program is located in the **Raspberry Pi (Door Control System)\ACNA2** folder.
5)	On the Access Control System, launch the access_control.py program to start the access control system by running the command: *“python access_control.py”*. The access_control.py program is located in the **Raspberry Pi (Access Control System)\ACNA2** folder.
6)	On the Access Control System, launch server.py to start the webserver by running the command:  *“python server.py”*. The server.py program is located in the **Raspberry Pi (Access Control System)\ACNA2** folder.
7)	When navigating to the Website User Interface, open a Web browser and enter "IP address of the Access Control System":5000 in the address bar. For example: http://127.0.0.1:5000.
8)	On the Access Control System, whenever the user wants to add or update his face or RFID card to the database , launch the add_face_or_card_uid.py program by running the command: *“python add_face_or_card_uid.py”*. The add_face_or_card_uid.py program is located in the **Raspberry Pi (Access Control System)\ACNA2** folder.

## Section 2 : Hardware requirements
This section will cover the hardware that is required to activate ACNA 2.0. This will include images and details about how the individual hardware components connect to the Raspberry Pi and how they contribute to the functionality of ACNA 2.0.

### Hardware checklist
ACNA 2.0 comes with a host of raspberry pi tools that gives it the ability to function. They are all elaborated below.

#### Access Control System Raspberry Pi
The main Raspberry Pi where users are able to verify their identities either through RFID card or facial recognition in order to gain access to the facility.

##### Overall Table of Hardware (Main Raspberry Pi)
| S/N | Hardware                                  | Quantity  |
| --- | ----------------------------------------- | --------- |
| 1   | RFID MFRC522 Card Reader                  | 1         |
| 2   | Raspberry Pi Camera                       | 1         |
| 3   | RFID Access Cards                         | 6         |
| 4   | Male-to-Female Cables                     | 7         |
| 6   | Breadboard with T-Cobbler for Rasberry Pi | 1         |
| 7   | Ribbon Cable                              | 1         |

##### 1 Raspberry Pi Camera
The Raspberry Pi camera is an extension of the Raspberry Pi motherboard which takes images of the user whenever required. The Raspberry Pi camera is utilized to take an image of the user and uploads said face into the Amazon Web Service (AWS) rekognition service to be authorized.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/RPI_camera.jpg "Raspberry Pi Camera")

##### 1 RFID MFRC522 Card Reader
The Radio Frequency Identification (RFID) MFRC522 Card Reader is responsible for scanning the RFID access cards to discern the identity of the user.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/MFRC522.jpg "RFID MFRC522 Card Reader")
 
##### 6 RFID Access Cards
The Radio Frequency Identification (RFID) Access Cards contain a unique signature which allows it to identify the user with the card in hand. The cards are utilized by the user to gain access into the facility by scanning it on the Card Reader.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/RFID_cards.jpg "RFID Access Cards")
 
##### 7 Male-to-Female Cables
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/male_to_female.jpg "Male-To-Female cables")

#### Door Control System Rasberry Pi
This Raspberry Pi simulates a door which is designed to receive data from the MQTT protocol and determine whether the users are allowed to access the facility. It will control whether to open the door or remain closed, depending on the results received.

##### Overall Table of Hardware (Door Raspberry Pi)
| S/N | Hardware                                  | Quantity  |
| --- | ----------------------------------------- | --------- |
| 1   | Buzzer                                    | 1         |
| 2   | 2x16 Characters i2c LCD Display           | 1         |
| 3   | Male-to-Female Cables                     | 4         |
| 4   | Male-to-Male Cables                       | 2         |
| 5   | Breadboard with T-Cobbler for Rasberry Pi | 1         |
| 6   | Ribbon Cable                              | 1         |

##### 1 Buzzer
The buzzer, when activated, produces a loud beeping sound. In ACNA 2.0, the buzzer will sound to let the user know that the Door Control System has received the results from the Access Control System. If access was granted, it will sound for 1 second. If access was denied, it will sound for 2 seconds. 

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/buzzer.jpg "Buzzer")
 
##### 1 2x16 Characters i2c LCD Display
The LCD displays short messages or information for users to read from the Raspberry Pi. By default, it will display a default message as set by the user. When it receives a new access attempt, it will display the result of whether the user has been granted or denied access into the facility.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/lcd_display.jpg "LCD Display")
 
##### 4 Male-to-Female Cables
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/male_to_female.jpg "Male-To-Female cables")

##### 2 Male-to-Male Cables
 ![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/male_to_male.jpg "Male-To-Male cables")

### Hardware setup instructions (Access Control System)

#### Access Control System
1)	If it has not already been done so, attach the T-Cobbler for Raspberry Pi to the breadboard.
2)	Connect the breadboard (with T-Cobbler attached) to the Raspberry Pi, using a ribbon cable.
3)	Connect each of the following components to the setup:

##### RFID MFRC522 Card Reader
On the breadboard, connect each MFRC522 pin with the corresponding RPi pin with a colored jumper cable as shown in the table below.
| Jumper color | MFRC522 Pin | RPi Pin        |
| ------------ | ----------- | -------------- |
| Yellow       | SDA         | CE0            |
| Orange       | SCK         | SCLK           |
| Green        | MOSI        | MOSI           |
| Blue         | MISO        | MISO           |
| Black        | GND         | GND            |
| White        | RST         | GPIO25         |
| Red          | 3.3V        | 3.3V           |

##### PiCamera
1)	Connect the PiCamera to the CSI Port of the Raspberry Pi, which is the long thin port adjacent to the HDMI socket.
2)	Lift the collar on top of the CSI port and slide the ribbon cable of the camera module into the port with the blue side facing the Ethernet port.
3)	Once the cable is in the port, press the collar back down to lock the cable in place.

#### Door Control System
1.	If it has not already been done so, attach the T-Cobbler for Raspberry Pi to the breadboard.
2.	Connect the breadboard (with T-Cobbler attached) to the Raspberry Pi, using a ribbon cable.
3.	Connect each of the following components to the setup:

##### 2x16 Characters i2c LCD Display
On the breadboard, connect each LCD pin with the corresponding RPi pin with a colored jumper cable as shown in the table below.
| Jumper color | LCD Pin | RPi Pin        |
| ------------ | ------- | -------------- |
| Yellow       | SDA     | SDA            |
| Black        | SCK     | GND            |
| White        | MOSI    | SCL            |
| Red          | VCC     | 5.0V           |

##### Buzzer 
On the breadboard, connect each Buzzer pin with the corresponding RPi pin with a coloured jumper cable as shown in the table below.
| Jumper color | LCD Pin  | RPi Pin         |
| ------------ | -------- | --------------- |
| Black        | GND      | GND             |
| Red          | VOUT     | GPIO5           |

### Figure 30: Fritzing Diagram (Access Control System) 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/access_control_system.png "Fritzing Diagram Access Control System")

### Figure 31: Fritzing Diagram (Door Control System) 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/door_control_system.PNG "Fritzing Diagram Door Control System")

## Section 3 : Software Requirements
This section will cover the software requirements needed to run ACNA 2.0, which includes the dependencies needed to run the Python programs and creating the Amazon Web Service (AWS) software needed to achieve MQTT, facial recognition and other AWS features in ACNA 2.0.

### Software checklist
These are the packages and dependencies that are needed to run ACNA 2.0.

#### Access Control System 
 - AWSIoTPythonSDK
 - boto3
 - configparser
 - datetime
 - flask
 - gevent
 - MFRC522
 - numpy
 - picamera
 - twilio
 - uuid
 
#### Door Control System
 - AWSIoTPythonSDK
  - boto3
 - configparser
 - gpiozero
 - rpi_lcd
 - twilio
 - uuid

### Software setup instructions
These are the steps needed to be undertake to setup the Amazon Web Service, Access Control System and Door Control System.

#### Amazon Web Service
Before setting up the software of the raspberry pi, one must conduct the creation of the AWS in order to establish the MQTT protocol.
##### Creating a Thing
1) After logging into AWS, under the search tab, navigate to the service that is called "IoT Core"
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_1.PNG "Creating a thing")

2) Under the IoT Core navigational tab, select the "Manage" keyword. Under the "Manage" tab select the "Things" keyword. 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_2.PNG "Navigate Creating a thing")

3) It is likely that the page that you are redirected to does not have a thing configured.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_3.PNG "Initalizzing  to create a thing")

4) In the same page, we will want to create our Thing. This can be accomplished by selecting the "Create" tab.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_4.PNG "Start to create a thing")

5) The next step is to select "Create a Single Thing" tab. 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_5.PNG "Select Single thing ")
6) Enter a name for the thing, for example ACNA2_setup. Do note that this field is compulsory for creating the thing.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_6.PNG "Entering name thing ")

7) Skip the rest of the other prompts and select the "next" tab located below on the same page.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_7.PNG "Moving on to the next step")

8) The page is redirected to the next step, in which a new certificate must bre created. Select the tab "Create certificate".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_8.PNG "Moving on to the next step")

9) If done correctly, AWS should display a pop-up message that the thing and certificate have been successfully created. The next step is to save the certificates to be utilized in ACNA 2.0. Download the certificates by clicking on the corresponding download buttons.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_9.PNG "Success creation and certificate download")

10) There is one more obscure certificate required (the root CA), which is the Amazon Root RSA certificate. To download this certificate, select the "download" tab below, under the “You also need to download a root CA for AWS IoT:” 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_10.PNG "Download Root RSA")

11) It will redirect you to a page where you are able to download the root CA certificate. Select the "Amazon Root CA 1".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_11.PNG "Download Root RSA")

12) The page is once again redirected to the contents of the Root RSA. Save the file into your computer.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_12.PNG "Saving Root RSA")

13) After obtaining the files, rename them accordingly from:
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_13.PNG "Original file names")

To

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_14.PNG "New file names")

14) After completing the renaming of the files, navigate back to activate the certificate. You should see a notification which indicates the success. Select the done button to continue to the next step.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_15.PNG "Activate the certificate")

15) Finally, save the newly set certificates into the directories **Raspberry Pi (Access Control System)\ACNA2\certificates**, **Raspberry Pi (Door Control System)\ACNA2\certificates** and **Transfer To Amazon\Transfer To Lambda\AWSIoTPythonSDK**.
##### Creating a Policy
1) We will have to create a policy in order to direct our thing to perform certain actions. Back to the IoT Core main page, select the "Secure" keyword and then select the "Policies" keyword.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_16.PNG "Nativagating to policy tab")

2) Select the "Create" tab to create a new policy.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_17.PNG "Creatng a new policy")

3) The page is redirected to the step to fill in the rules for the policy to dictate the ACNA2_setup thing. Fill in the section with the corresponding values in the picture below, then click the create button.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_18.PNG "Filling values with new policy")

4) You should see a green notification indicating the success in creating the policy.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_19.PNG "Notifying the success")

##### Attaching the policy to the certificate and the thing
1) With the certificate, things and policy created, we will combine them together to form the basis of the MQTT protocol. To start, navigate to the IoT Core main page, select the "Secure" keyword and then select the "Certificate" keyword.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_20.PNG "Navigating to certificates")

2) Find the certificate that was created originally, select the 3 dots on the option and select the "Attach policy".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_21.PNG "Attaching policy")

3) Choose the policy that was created earlier, (in this scenario it is named "ACNA2_setup_policy") and select the attach tab to complete the procedure. If done correctly, a notification will appear to indicate the success.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_22.PNG "Attachment completed")

4) Like in the 2nd step, select the three dots on the certificate and select the "Attach thing" option
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_23.PNG "Attaching thing")

5) Choose the thing that was created earlier, in this scenario is named "ACNA2_setup" and select the attach tab to complete the procedure. If done correctly, a notification will appear to indicate the success.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_24.PNG "Attachment completed")

#### Configuring the AWS role (iot)
This next section will cover the steps in order to configure the AWS role so that the AWS services utilized are able to communicate with each other. There are two roles that have to be created.

1) Going back to the AWS Management Console page, search for the service "IAM" and select the option.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_25.PNG "IAM console")

2) Under the navigational tab of the IAM roles, under the Access management tab, select the "roles" tab.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_26.PNG "IAM navigational")

3) Next, select the "Create role" tab to create the new role.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_27.PNG "IAM creation")

4) Click “Create Role” and on the next page, choose “AWS service”, then “IOT”
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_28.PNG "AWS service")
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_29.PNG "AWS service")

5) Under “Select your use case”, select IoT and click the "Next: Permission" and "Next: Tags". These two pages do not require and configuration
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_30.PNG "AWS service")

6) When you do reach the "create role" page, ensure that the policies match the ones that you are setting. The Role name and descriptions can be renamed under the user's discretion. In this scenario, the role name will be called the ACNA2_iot_rule. After finishing setting the roles, click on the Create Role tab below.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_31.PNG "New AWS role created")

#### Creating the DynamoDB tables
There are 5 database tables that are used in ACNA 2.0. This section has to be repeated 5 times, once for each table, to create all the tables.
1) In the AWS management console, search for the "DynamoDB" service.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_32.PNG "Navigate to DynamoDB")

2) Inside DynamoDB navigational tab, select the "dashboard" tab and select the "Create table option"
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_33.PNG "Navigate to DynamoDB")

3) The next step is to fill in the values to create the database. The highlighted black portions are where the vaulues should be edited where necessary. 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_34.PNG "Create table")

Fill in the values accordingly, as stated in the table below.

| Table Name   | Primary Key | Primary Key Datatype     | Sort Key   | Sort Key Datatype |
| ------------ | ----------- | ------------------------ | ---------- | ----------------- |
| access_logs  | log_id      | String                   | username   | String            |
| lcd_display  | display_id  | String                   |            |                   |
| leave        | username    | String                   | start_date | String            |
| scanner      | scanner_id  | String                   |            |                   |
| user         | username    | String                   |            |                   |

Once the table has been created, click on the “Create” tab to create the table.

4) This is how the access_logs table looks like when populated.
Figure 32 : access_logs DynaomoDB Table
Note: For this application, it is recommended to add at least one admin account manually into DynamoDB so that you may use it to login to the Web UI later.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/database_images/access_logs.JPG "access_log DB")

5) This is how the lcd_display table looks like when populated.
Figure 33 : lcd_display DynamoDB Table
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/database_images/lcd_display.JPG "lcd_display DB") 

6) This is how the leave table looks like when populated.
Figure 34 : leave DynamoDB Table
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/database_images/leave.JPG "leave DB")

7) This is how the scanner table looks like when populated.
Figure 35 : scanner DynamoDB Table
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/database_images/scanner.JPG "scanner DB")

8) This is how the user table looks like when populated.
Figure 36 : user DynamoDB Database
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/database_images/user.JPG "user DB")

#### Creating the S3 bucket
The next section will cover the steps to setting up the S3 bucket to store the images for ACNA 2.0.

1) Back to the AWS management console, search for the "S3" service.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_35.PNG "Search s3")

2) Select the "Create bucket" option on the newly opened window. 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_36.PNG "create bucket")

3) Fill in the name of the bucket and location constraint of the bucket. In this instance, the bucket is named "s3-acna2.0-bucket" and the location constraint is "US East (N. Virginia)". After keying in the values, click on the create button below the window.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_37.PNG "Select values")

4) The new bucket should be created as specified in the S3 bucket window


#### Configuring the role for Lambda
Before setting up Lambda, we will have to create the role to accomodate the permissions which Lambda can access.

1) Going back to the AWS Management Console page, search for the service "IAM" and select the option.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_25.PNG "IAM console")

2) In the navigation sidebar, under the Access Management tab, select “Roles”.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_26.PNG "IAM navigational")

3) Next, select the "Create role" tab to create the new role.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_27.PNG "IAM creation")

4) Click “Create Role” and on the next page, choose “AWS service”, then “Lambda”
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_28.PNG "lambda service")
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_38.PNG "lambda service")

5) Under “Select your use case”, select Lambda and click the "Next: Permissions".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_39.PNG "Next Permissions")

6) In the "Next: Permissions" page, search for the following policies defined in the table below using the filter search bar. When you find the policy, check it by clicking on the square box on the left of the policy.

| Policies to filter          |
| --------------------------- |
| AWSLambdaFullAccess         |
| AmazonS3FullAccess          |
| CloudWatchFullAccess        |
| AmazonDynamoDBFullAccess    |
| AmazonRekognitionFullAccess |

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_39.PNG "Next Permissions")
After all the permissions have been selected, click on the "Next : Tags". Skip the page and proceed to the "Next : Review" page.

7) In the "Next : Review" page, ensure that the role name has been filled. In this scenario, the name is defined as "ACNA2_connect_s3_lambda_rekog_role". After all the variables have been filled and policies specified in step 6 fulfilled, create the role by clicking "create role".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_40.PNG "Review Role")

#### Creating the 'Rekog' Lambda function
There are two AWS Lambda functions that must be created. The first being the function that contains the AWS rekognition service and its ability to obtain the image from the bucket needed to compare faces. This section will elaborate on the set-up procedures of the first function.

1) Change the value of the location restriction (second argument) when necessary in the **Transfer To Amazon\acna2_s3_to_rekog.py** file 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_66.PNG "Commander cody, the time has come")

2) Going back to the AWS MAnagement Console page, search for the service "Lambda" and select the option.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_41.PNG "Lambda console")

3) In the Lambda navigation sidebar, select "Functions".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_42.PNG "Lambda Functions")

4) Proceed to create a new lambda function by selecting the "Create function" button.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_43.PNG "Create function")

5) Inside the create function page, click on the option that specifies "Use a blueprint"
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_44.PNG "Use a blueprint")

6) Using the add filter search tab, filter for the "rekognition-python" blueprint. Select the option by clicking on the bullet. After selecting it, click on the "Configure" button to continue.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_45.PNG "Configure Rekog")

7) Fill up the configuration blueprint page with the following values according to the tables below.

**Basic Information**
| Variable              | Value                              |
| --------------------- | ---------------------------------- |
| Function name         | acna2_s3_to_rekog_to_s3_function   |
| Use an exisiting role | *Click on the bullet point*        |
| Existing role         | ACNA2_connect_s3_lambda_rekog_role |

Note that the role "ACNA2_connect_s3_lambda_rekog_role" was created under the section "Configuring the role for Lambda"

**S3-Trigger**
| Variable                  | Value                              |
| ------------------------- | ---------------------------------- |
| Bucket                    | s3-acna2.0-bucket                  |
| Event type                | All object created events          |
| Prefix - optional         | *Leave it blank*                   |
| suffix - optional         | .jpg                               |
| Enable trigger            | *tick the checkbox*                |

Ensure that the trigger is enabled!

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_46.PNG "Configure Lambda Func 1")
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_47.PNG "Configure Lambda Func 2")

8) After finishing the configuration settings, click on the create function button at the bottom of the page
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_48.PNG "Create function")

9) A notification should pop out which shows you have successfully created the new function.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_49.PNG "Notification")

10) Scroll down to find this section of the code. Replace the entirety of **lambda_function.py** in the AWS Lambda function text with the **\Transfer To Amazon\acna2_s3_to_rekog.py** program.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_50.PNG "Before Replace text")

11) Once the file has been changed, the change should not take place yet as one needs to save the option. Before doing so however, you will have to set the timeout. To do so, scroll down the webpage until you find the Basic Settings. Click on the edit button.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_57.PNG "Basic Settings")

12) Change the timeout from 3 seconds to 1 minute and save the change by clicking the "save" button.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_58.PNG "Change the Basic Settings")

13) Save the changes. 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_59.PNG "Save all changes")

#### Creating the 'Publishing' Lambda function
After finishing the configuration of AWS, the next step is to configure the software for the two Raspberry Pi that will communicate with the AWS services.  

1) Change the variables where necessary in **Transfer To Amazon\Transfer To Lambda\AWSIoTPythonSDK\lambda_function.py**
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_61.PNG "A new file structure")

| Variable        | Definition                             |
| --------------- | -------------------------------------  |
| Host            | The REST API endpoint of the IoT Thing |
| rootCAPath      | Filename of root CA                    |
| certificatePath | Filename of certificate file           |
| privateKeyPath  | Filename of private key file           | 

2) Going back to the AWS Management Console page, search for the service "Lambda" and select the option.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_41.PNG "Lambda console")

3) In the Lambda navigation sidebar, select the "Functions" tab.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_42.PNG "Lambda Functions")

4) Proceed to create a new Lambda function by selecting the "Create function" button.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_43.PNG "Create function")

5) Inside the create function page, ensure that the option "Author from scratch" is selected by clicking on the bullet point.  
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_51.PNG "Create function")

6) The next step is to fill in the basic information configurations

**Basic Information**
| Variable              | Value                               |
| --------------------- | ----------------------------------- |
| Function name         | get_result_from_lambda_publish_iot  |
| Runtime               | Python 2.7                          |
| Use an exisiting role | *Click on the bullet point*         |
| Existing role         | ACNA2_connect_s3_lambda_rekog_role  |

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_52.PNG "Create function")

7) After filling in the basic information configuration, click on the button "Create function" to finialize the creation of the new function.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_43.PNG "Create function")

8) You should get a notification that resembles the image below.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_53.PNG "Create function")

9) Due to the limitations of AWS Lamba, external imports are unable to be pip installed. Hence, the alternative is to externally bring the exports to to the function. To start off, find the folder “AWSIoTPythonSDK” in the **Transfer To Amazon/Transfer To Lambda/** folder. It contains the files needed to be imported for the new Lambda function (in this case, the get_result_from_lambda_publish_iot) to work.

10) The certificates created to communicate with your IOT thing should be placed in the same directory as where the lambda_function.py file is located. Add the previously generated certificates into this folder, then zip the AWSIoTPythonSDK folder.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_54.PNG "Where are you now")

11) Transfer the zip file. Inside the get_result_from_lambda_publish_iot Lambda function, select the option "Upload a .zip file".
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_55.PNG "Upload option")

12) Upload the zip file.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_56.PNG "Click me!")

13) Once the folder has been uploaded, the change should not take place yet as one needs to save the option. However, before doing so, you will have to set the timeout. To do so, scroll down the webpage until you find the Basic Settings. Click on the edit button.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_57.PNG "Basic Settings")

14) Change the timeout from 3 seconds to 1 minute and save the changes by clicking the "save" button.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_58.PNG "Change the Basic Settings")

15) Save the changes. 
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_59.PNG "Save all changes")

16) After the changes have reloaded, change the file structure to resemble the image below.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_60.PNG "A new file structure")

#### Triggering the 'Rekog' Lambda function to run the 'Publishing' Lambda function
The Rekognition API has to pass imperative values to the Publishing Lambda function in order to successfully perform the MQTT function.
This section will explain how it is done.

1) In the AWS Management Console, search for the service "Lambda" and select the option.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_41.PNG "Lambda console")

2) In the Lambda navigational section, select the "Functions" tab.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_42.PNG "Lambda Functions")

3) Access the Rekog function by double clicking it. In this scenario it will be the acna2_s3_to_rekog_to_s3 function.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_62.PNG "Lambda Functions Rekog")

4) Select the "Add Destination option" after being redirected into the function.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_63.PNG "Add destination")

5) Edit the variables to fit the values into.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_64.PNG "Change values")

**Destination Configuration**
| Variable              | Value                              |
| --------------------- | ---------------------------------- |
| Source                | Asynchronous invocation            |
| Condition             | On Success                         |
| Destination type      | Lambda function                    |
| Destination           | get_result_from_lambda_publish_iot |

Note that the destination will be morphed into a REST API endpoint pointing to the selected function.

After the configurations are set, save the file.

6) The new diagram should be pointing to the new function.
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/Amazon_web_service/create_a_thing_65.PNG "The end")

With that, the AWS setup is complete.

#### Access Control System 
Note that the requirements.txt is located in the **Raspberry Pi (Access Control System)\ACNA2** folder.

Navigate to the folder where the requirements.txt file is located, then run the command:

```
pip install -r requirements.txt
```

If AWSIoTPythonSDK is installed in your Raspberry Pi image, there are no additional libraries you need to install. However, if not, these are the steps to follow.

```
sudo pip install --upgrade --force-reinstall pip==9.0.3
sudo pip install AWSIoTPythonSDK --upgrade --disable-pip-version-check
sudo pip install --upgrade pip

```

If you are using the given Raspberry Pi image, you may skip this section on how to enable the usage of the MFRC522 Card Reader. However, if not, you should follow the following instructions:

1) Enable SPI:
```
sudo rasp-config
```
Interfacing Options > Enable SPI.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/config_SPI_1.png "Configuring SPI")

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/config_SPI_2.png "Configuring SPI 2")

2) Modify /boot/config.txt to enable SPI:
```
sudo nano /boot/config.txt
```
Ensure that the following lines are included:
```
device_tree_param=spi=on
dtoverlay=spi-bcm2835
```

3) Install python-dev:
```
sudo apt-get install python-dev
```

4) Install SPI-Py Library:
```
cd ~ 
git clone https://github.com/lthiery/SPI-Py.git
cd ~/SPI-Py
sudo python setup.py install
```

Ensure that the PiCamera has been enabled in the Raspberry Pi by going through the following steps:

1) Open the Raspberry Pi Configuration Tool from the main menu.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/picam1.png "Picam 1")

2) Enable the camera software and reboot your Raspberry Pi.

![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/picam2.png "Picam 2")

Ensure that the **Raspberry Pi (Access Control System)\ACNA2\acna2_configuration.ini** file is edited to fit the user needs. The table below elaborates on the different variables and their definitions.

a. twilio

| Variable Name | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| account_sid   | Account SID for Twilio notification                           |
| auth_token    | Authentication token for Twilio notification                  |
| my_hp         | User’s telephone number to send for Twilio notifications      |
| twilio_hp     | Configured Twilio number which sends the notification to user |

b. aws_configuration

| Variable Name | Description                                      |
| ------------- | ------------------------------------------------ |
| bucket_name   | The name of the AWS S3 bucket to be used.        |

c. dynamoDB_configuration

| Variable Name   | Description                                                                  |                                                
| --------------- | ---------------------------------------------------------------------------- | 
| host            | Rest API Endpoint of the AWS IOT thing                                       | 
| rootCAPath      | The path which leads to the root Certificate Authority of the AWS IOT Thing  |
| certificatePath | The path which leads to the certificate of the AWS IOT Thing                 |  
| privateKeyPath  | The path which leads to the private Key of the AWS IOT Thing                 |                            
| Pub-Sub         | The key utilized by the AWSIoTPythonSDK                                      |                                   
| Port            | Port utilized for MQTT communication                                         |                                    

#### Door Control System 
Note that the requirements.txt is located in the **Raspberry Pi (Door Control System)\ACNA2** folder.

Navigate to the folder where the requirements.txt file is located, then run the command:

```
pip install -r requirements.txt
```

If AWSIoTPythonSDK is installed in your Raspberry Pi image, there are no additional libraries you need to install. However, if not, these are the steps to follow.

```
sudo pip install --upgrade --force-reinstall pip==9.0.3
sudo pip install AWSIoTPythonSDK --upgrade --disable-pip-version-check
sudo pip install --upgrade pip
```

In the mqttClient.py file, if you wish to, you may customise the time the company starts work (default: 9:00 AM) in the start_work variable to any value you want. end_day is recommended to be left as 11:59:59 PM.
(This will control the time range when Twilio sends an alert for staff who have arrived late.)
![alt text](https://github.com/Halogen117/ACNA2/blob/master/README_Images/start_work_hours.png "Start_work and end_day variables")

Ensure that the **Raspberry Pi (Door Control System)\ACNA2\acna2_configuration.ini** file is edited to fit the user needs. The table below elaborates on the different variables and their definitions.

a. twilio

| Variable Name | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| account_sid   | Account SID for Twilio notification                           |
| auth_token    | Authentication token for Twilio notification                  |
| my_hp         | User’s telephone number to send for Twilio notifications      |
| twilio_hp     | Configured Twilio number which sends the notification to user |

b. aws_configuration

| Variable Name | Description                                      |
| ------------- | ------------------------------------------------ |
| bucket_name   | The name of the AWS S3 bucket to be used.        |

c. dynamoDB_configuration

| Variable Name   | Description                                                                  |                                                
| --------------- | ---------------------------------------------------------------------------- | 
| host            | Rest API Endpoint of the AWS IOT thing                                       | 
| rootCAPath      | The path which leads to the root Certificate Authority of the AWS IOT Thing  |
| certificatePath | The path which leads to the certificate of the AWS IOT Thing                 |  
| privateKeyPath  | The path which leads to the private Key of the AWS IOT Thing                 |                            
| Pub-Sub         | The key utilized by the AWSIoTPythonSDK                                      |                                   
| Port            | Port utilized for MQTT communication                                         |   

## Section 4 : Expected Results
To test if the program works, follow all the steps as stated in section 2 and 3. The following is the link to the video demonstration of what the application should look like. https://www.youtube.com/watch?v=xVEgjQvqfps

The Raspberry Pi of the Access Control System should be able to access the S3 bucket and DynamoDB database and await for the next user to either scan his card with the MFRC522 Card Scanner or use the Pi Camera to take an image of his or her face and upload it into the S3 bucket.

When started, the program server.py hosted inside the Raspberry Pi of the Access Control System should be able to render webpages at "IP Address of Access Control System":5000. In the Web UI, you should be able to login with an admin account you manually created earlier, view access logs and attendance values, create new users, etc.

When started, the program access_control.py hosted inside the Raspberry Pi of the Access Control System should be ready to receive and process data from the MFRC522 RFID Card Reader when a user scans their access card. It should also capture a picture every 10 seconds and upload to S3 if it detects a face in the images captured.

The program add_face_or_card_uid.py hosted inside the Raspberry Pi of the Access Control System should be able to allow users to add / update their face and RFID card to S3 and DynamoDB respectively.

When started, the program mqttClient.py hosted inside the Raspberry Pi of the Door Control System should be able to subscribe to the ACNA2/MQTT_subscription subscription topic to receive messages from the Access Control System in order to either allow access or deny user entries into the database. When a user is trying to access the location via face recognition, the program should be able to receive a confirmation from AWS Lambda to check if the user matched with any face in the s3 bucket database. It should also be able to access the DynamoDB database to obtain values from the AWS Broker. The LCD hooked onto the system should immediately display the default message set by the user by default, and display the "Access Granted" or "Access Denied" whenever a user attempts to access a location. The buzzer should sound an alert in the event of an attempted access.



```
End of ACNA 2.0 Github Documentation
```
