""" class based version of testing.serial.py"""

import serial, paho.mqtt.client as mqtt, threading

class SerialRead(threading.Thread):
    def __init__(self, *iterables, baud=9600, port='/dev/ttyACM0'):
      threading.Thread.__init__(self)
      self.threadID = iterables[0]
      self.name = iterables[1]

      self.buf = bytearray()
      self.ser = None
      self.baud = baud
      self.port = port

    def readline(self):
        index = self.buf.find(b"\n")
        if index >= 0:
            partial = self.buf[:index+1]
            self.buf = self.buf[index+1:]
            return partial + b':ERROR'
        while True:
            index = max(1, min(2048, self.ser.in_waiting))
            data = self.ser.read(index)
            index = data.find(b"\n")
            if index >= 0:
                r = self.buf + data[:index+1]
                self.buf[0:] = data[index+1:]
                return r
            else:
                self.buf.extend(data)

    def run (self):
        self.ser = serial.Serial(self.port, self.baud)
        while True:
           print(self.readline().decode('utf-8').strip().split(':'))


class MqttSub(threading.Thread):
    
    def __init__(self, *iterables, host='localhost', port=1883, topic='', keepalive=60):
        threading.Thread.__init__(self)
        self.threadID = iterables[0]
        self.name = iterables[1]

        self.client = None
        self.host = host
        self.port = port
        self.topic = topic
        self.keepalive = keepalive

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        #print("Connected with result code "+str(rc))
        client.subscribe(self.topic)

    def on_disconnect(self, client, userdata,rc=0):
        #print("Disconnected result code "+str(rc))
        client.loop_stop()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        # todo respond to payload

    def run (self):
        print ("MQTT Sub run()")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_forever()

# create and label threads




"""
Run mutliple concurrent threads
-------------------------------
alter the parameters for these two instances of the Threading class
  parameters :-
    1st is thread id
    2nd is thread name

  named :-
  SerialRead() defaults: port='', baud=9600
  MqttSub() defaults: host='localhost', port=1883, topic=''

"""
t1 = SerialRead(1, 'Serial Read', port='/dev/ttyACM0')
t2 =    MqttSub(2, 'MQTT Sub',    topic='emoncms/stm32/request/#')

# start threads
t1.start()
t2.start()

# wait for both threads to end
t1.join()
t2.join()

print("Multi Threading Finished")
# end
