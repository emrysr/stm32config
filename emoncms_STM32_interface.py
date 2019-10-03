""" MQTT CONNECTION """
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe("emoncms/stm32/request/#")

def on_disconnect(client, userdata,rc=0):
    #print("Disconnected result code "+str(rc))
    client.loop_stop()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()






""" SERIAL CONNECTION """

import serial


import serial
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
buf = bytearray()

while True:
    index = max(1, min(2048, ser.in_waiting))
    data = ser.read(index)
    index = data.find(b"\n")
    if index >= 0:
        r = buf + data[:index+1]
        buf[0:] = data[index+1:]
        try:
          print (r.decode().strip().split(':'))
        except: 
          pass
    else:
        buf.extend(data)


"""
@todo: fix thread priorites

mqtt and pyserial cant loop the thread continually. multi threading is required
"""

