import serial
import sys
import time
import paho.mqtt.client as mqttClient
import json
from kafka import KafkaConsumer

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
        client.subscribe("17_20")
    else:
 
        print("Connection failed")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
 
Connected = False   #global variable for the state of the connection
 
 
client = mqttClient.Client("Python1")               #create new instance
client.username_pw_set("JWT","eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1OTE2Mjk2OTEsImlzcyI6ImlvdHBsYXRmb3JtIiwic3ViIjoiMTdfMjAifQ.R2imy6o4Nzc8W4pMNBZVZz77nx1mw5ck1LulIfzm68pEyBIEkCmvO5MOjqN1wBI6psXJ0amSEHZF3GfhwHq4pbHRcreK8LWEn1eIXaN879z4I1f9XYWTMJv4tF9LXiTXoFL7vox4teydsw0FxF0IGErgw7x-MhH3Wp1HZpJHDTWhOC-JV6k5rTKHCo1OkG7vd4cTL1lzsGDXMfTkjIpKy8rCOnbbmxwG34EOH2HJdM9RlHpeHdY1J7CbESDKGzkrxUi35dHweE_dMcxXVPrskS4eVzWHrcPSA1bRQW9zabZfb-13PxDAGMUnczetEto_ddP7vqH40dLvEhBXhszWwV29FoSgSU7LEkGsADqZejdqeMPZmXZqDDdRAK_17xL7afD8w35xT2HezP4-Q6U8xrchYgmtN_dXAMGYZdMfpxnTr18r0lspULc5XbsG6J4DxWDmxEsw23DBWHUw-tDe6udrC7Ltz7oq_vGIn7lhtco9ROiGzvqjElbFOlA0YlxJcefbrTiIlrXpWerWEUI6otHTRsvH6BDeFdBgihH-lrBpERFj5JCJqkoonIzvbSlSi0iP9quZGKw5bN5ocVLA7vkDVroL7H6zToN4XqY45l5KXi_iogqOoYm8h_t0BdcRFajwT3nLIEDqpwkmJA2o_04YThEYo53Sj5JmV71sHFo")
client.on_connect = on_connect  
client.on_message = on_message                    #attach function to callback
client.connect("131.159.35.132", 1883, 60)          #connect to broker
#client.connect("127.0.0.1", 1883, 60)   
 
client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)

if len(sys.argv) == 1:
	print("Error: serial port not specified.")
	sys.exit()

if len(sys.argv) > 3:
	print("Error: too many arguments")
	sys.exit()

portName = sys.argv[1]
port = serial.Serial(portName, 115200, timeout=1)
l = port.readline()
if l.decode("utf-8").strip():
	print(">>>", l.decode("utf-8"), end = '')


def processFile(fileName, port):
	file1 = open(fileName, 'r') 
	Lines = file1.readlines() 
	tstr = "0:0:" + str(int(Lines[0][0:10]) - 30)
	port.write(tstr.encode("utf-8"))
	port.readline()
	for line in Lines: 
		port.write(line.encode("utf-8"))
		row = port.readline()
		myline = row.decode("utf-8")
		if myline.strip():
			print(">>>", myline, end = '')
			if myline.startswith("<"):
				payload2 = {
				"username": "group14",
 				"number": int(myline[18:myline.index(":", 18)]),
 				"device_id": 20,
				"timestamp": int(myline[7:17])*1000
					}
				y = json.dumps(payload2)
				client.publish("17_20", y)



def getDataFromKafka(port):
	topic_name = '01_06_020'
	consumer = KafkaConsumer(
    topic_name, 
    auto_offset_reset='earliest',
    bootstrap_servers=['138.246.232.197:9092'], 
    api_version=(0, 10)) 
    #consumer_timeout_ms=1000)

	for msg in consumer:
		port.write(msg.value)
		print(msg.value.decode("utf-8"))
		row = port.readline()
		myline = row.decode("utf-8")
		if myline.strip():
			print(">>>", myline, end = '')
			if myline.startswith("<"):
				payload2 = {
				"username": "group14",
 				"number": int(myline[18:myline.index(":", 18)]),
 				"device_id": 20,
				"timestamp": int(myline[7:17])*1000
					}
				y = json.dumps(payload2)
				client.publish("17_20", y)
				
				
    
def interactive(port):

	while True:
		inp = input()
		port.write(inp.encode("utf-8"))
		line = port.readline()
		myline = line.decode("utf-8")
		if myline.strip():
			print(">>>", myline, end = '')
			if myline.startswith("<"):
				payload2 = {
				"username": "group14",
 				"number": int(myline[18:myline.index(":",18)]),
 				"device_id": 20,
				"timestamp": int(myline[7:17])*1000
					}
				y = json.dumps(payload2)
				client.publish("17_20", y)


def sendCurrentTime(port):
	timeString = "0:0:" + str(int(time.time()))
	port.write(timeString.encode("utf-8"))
	port.read(100)



if len(sys.argv) == 3:
	if sys.argv[2] == "kafka":
		sendCurrentTime(port)
		getDataFromKafka(port)
	else:
		fileName = sys.argv[2]
		processFile(fileName, port)
	
else:
	sendCurrentTime(port)
	interactive(port)

while True:
	port.write(b'')
	line = port.readline()
	myline = line.decode("utf-8")
	if myline.strip():
		print(">>>", myline, end = '')
		if myline.startswith("<"):
				payload2 = {
				"username": "group14",
 				"number": int(myline[18:myline.index(":",18)]),
 				"device_id": 20,
				"timestamp": int(myline[7:17])*1000
					}
				y = json.dumps(payload2)
				client.publish("17_20", y)

client.disconnect()
client.loop_stop()

	


