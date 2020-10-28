#!/usr/bin/env python
import cayenne.client
import time
import logging
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "a6de5eb0-08c6-11eb-b767-3f1a8f1211ba"
MQTT_PASSWORD  = "9ba17c84b394cfa422832d135ae454c1fc05265f"
MQTT_CLIENT_ID = "e87cb7f0-090b-11eb-8779-7d56e82df461"


# The callback for when a message is received from Cayenne.
def on_message(message):
    print("message received: " + str(message))
    # If there is an error processing the message return an error string, otherwise return nothing.
    
client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, loglevel=logging.INFO)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

GPIO.setmode(GPIO.BOARD)
DHT_SENSOR = Adafruit_DHT.DHT22
delayt = .1 
value = 0 # this variable will be used to store the ldr value
ldr = 7 #ldr is connected with pin number 7
dht = 4 #pin 4 for dht22
timestamp = 0
temp_in = 24
temp_out = 17
umid = 63
lux = 840
movimento = 0
porta = 1
tankL = 77
lamp_out = 0

def rc_time (ldr):
    count = 0
 
    #Output on the pin for
    GPIO.setup(ldr, GPIO.OUT)
    GPIO.output(ldr, False)
    time.sleep(delayt)
 
    #Change the pin back to input
    GPIO.setup(ldr, GPIO.IN)
 
    #Count until the pin goes high
    while (GPIO.input(ldr) == 0):
        count += 1
 
    return count



while True:
    client.loop()
        
    lux = rc_time(ldr)
    umid, temp = Adafruit_DHT.read_retry(DHT_SENSOR, dht)
    print(lux)
    if ( lux > 7000 ):
            lamp_out = 1
                
    if (lux <= 7000):
            lamp_out = 0
    
    if (time.time() > timestamp + 10):
        client.celsiusWrite(1, temp)
        client.luxWrite(2, lux)
        client.celsiusWrite(3, temp_out)
        client.umidWrite(5, umid)
        client.digitalWrite(6, movimento)
        client.digitalWrite(7, porta)
        client.tankWrite(8, tankL)
        client.digitalWrite(10, lamp_out)
        timestamp = time.time()
