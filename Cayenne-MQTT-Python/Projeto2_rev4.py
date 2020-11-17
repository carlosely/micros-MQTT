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

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 5
timestamp = 0
delayt = .1 
value = 0 # this variable will be used to store the ldr value
ldr = 7 #ldr is connected with pin number 7
lampadaJardim = 11 #led is connected with pin number 11
lampadaCorredor = 12    # pin12 --- led
stsJardim = 0
stsCorredor = 0
stsPresenca = 0
sensorPresenca = 18    # pin12 --- button
contTemp = 50
contLux = 5
contMovimento = 5
temp_out = 17
temperature = 0
humidity = 0
porta = 1
tankL = 77

GPIO.setmode(GPIO.BOARD)
GPIO.setup(lampadaCorredor, GPIO.OUT)   # Pino de led como saída
GPIO.setup(sensorPresenca, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)    # Pino do botão como saída e aciona o pull-up
GPIO.output(lampadaCorredor, GPIO.LOW) # Desliga o led
GPIO.setup(lampadaJardim, GPIO.OUT) # as led is an output device so that’s why we set it to output.
GPIO.output(lampadaJardim, False) # keep led off by default 

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
 
#Catch when script is interrupted, cleanup correctly
try:
    # 

    while True:
        client.loop()
        
        contTemp += 1
        contLux += 1
        contMovimento += 1
        
        
        #------------SENSOR TEMPERATURA--------------------------------------
        #if(contTemp > 60):
         #   humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
          #  print("Temperatura={0:0.1f}*C  Umidade={1:0.1f}%".format(temperature, humidity))
           # contTemp = 0
            
           
        
        #------------SENSOR PRESENÇA--------------------------------------
        if(contMovimento > 10):
            if GPIO.input(sensorPresenca) == GPIO.HIGH:
                print('Luz PORTÃO ligada...')
                GPIO.output(lampadaCorredor, 1)
                stsCorredor = 1
                stsPresenca = 1
            else:
                print('Luz PORTÃO desligada...')
                GPIO.output(lampadaCorredor, 0)
                stsCorredor = 0
                stsPresenca = 0
            
            contMovimento = 0
            
           
        #--------------SENSOR LUMUNOSIDADE--------------------------------
        if(contLux > 10):
            value = rc_time(ldr)
            print("Ldr Value: ", value)
            if ( value <= 5000 ):
                #está ao contrário pq o módulo relé funciona ao contrário
                    print("Luz JARDIM desligada")
                    GPIO.output(lampadaJardim, False)
                    stsJardim = 0
            if (value > 20000):
                #está ao contrário pq o módulo relé funciona ao contrário
                    print("Luz JARDIM ligada")
                    GPIO.output(lampadaJardim, True)
                    stsJardim = 1
            contLux = 0
        
       
                
        #----------------------ENVIO DADOS CAYENNE------------------------
        temperature = round(temperature, 2)
        humidity = round(humidity, 2)
                
        if (time.time() > timestamp + 1):
            client.celsiusWrite(1, temperature)
            client.luxWrite(2, value)
            #client.celsiusWrite(3, temp_out)
            client.umidWrite(5, humidity)
            client.digitalWrite(6, stsPresenca)
            #client.digitalWrite(7, porta)
            #client.tankWrite(8, tankL)
            client.digitalWrite(10, stsJardim)
            client.digitalWrite(11, stsCorredor)
            timestamp = time.time()
            
            
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
        
