#!/usr/bin/env python3
""" 
Thread based version to allow simultaneous connections to the serial port and MQTT server
"""

import serial, paho.mqtt.client as mqtt, threading, time, sys, logging

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class SerialConnect():
    def __init__(self, port):
        self.ser = False
        self.port = port
        self.name = 'Serial Connection'
        self.baud = 9600

        try:
            self.ser = serial.Serial(
                port = self.port,
                baudrate = self.baud,
                timeout = 1
            )

        except serial.serialutil.SerialTimeoutException:
            logging.debug ('%s: Serial connection timed out', self.name)
            pass

        except serial.serialutil.SerialException:
            logging.debug ('%s: Serial connection problem', self.name)
            pass

    def isConnected (self) :
        if (not self.ser) :
            logging.debug ('%s: Not connected to: %s', self.name, self.port)
            return False
        else :
            logging.debug ('%s: Serial connected...', self.name)
            return self.ser.write(b'hello')

class SerialWrite():
    def __init__(self, serial, message=''):
        self.name = 'Serial Write'
        self.serial = serial
        self.writeline(message)

    def writeline(self, message):
        self.serial.write(message)
        logging.debug ('%s: serial data sent', self.name)

class SerialRead(threading.Thread):
    def __init__(self, threadID, name, baseTopic, serialConnection, mqttClient):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

        self.buf = bytearray()
        self.serial = serialConnection
        self.baseTopic = baseTopic
        self.mqttClient = mqttClient

    def readline(self):
        logging.debug ('%s: Waiting for serial data...', self.name)
        line = []
        started = False # wait for first new line character
        ended = False # wait for last new line character
        
        while not ended:
            for byte in self.serial.read():
                if byte == '\n':
                    if(started):
                        ended = True
                    else:
                        line = []
                        started = True
                else:
                    line.append(byte)

        return ''.join(line)

    def test_response(self, data):
        if len(data) == 5:
            return True
        else :
            return False

    def mqttPub(self, topic, message) :
        MqttPub(self.mqttClient, topic, message)

    def run (self):
        try:
            is_ok = True
            while is_ok:
                # time.sleep(.2)
                # listen for serial data
                try:
                    data = self.readline().strip().split(':')
                    is_ok = False
                    # check for specific data pattern
                    try:
                        logging.debug ('%s: Received %s', self.name,data)
                        if self.test_response(data):
                            # publish response to mqtt
                            try:
                                # todo: pick up the original request id from the serial response
                                request_id = "1"
                                topic = self.baseTopic + 'response/' + request_id
                                logging.info ("%s: publishing to %s...", self.name, topic)
                                newCommand = ':'.join(data)
                                self.mqttPub(topic, newCommand)
                                # time.sleep(2)
                                is_ok = True
                            except Exception as err:
                                logging.info ("%s: Error in MQTT Publish", self.name)
                                logging.error ("%s: %s", self.name, err)
                                is_ok = False
                                pass
                        else:
                            raise ValueError('Serial data format not correct')

                    except Exception as err:
                        logging.info ('%s: Error during testing serial response', self.name)
                        logging.error ('%s: %s', self.name, err)
                        is_ok = True

                except Exception as err:
                    logging.info ("%s: Error in serial read", self.name)
                    logging.error ("%s: %s", self.name, err)
                    is_ok = False

        except Exception as err:
            logging.info ("%s: Serial Read Error" % self.name)
            logging.error ("%s: %s", self.name, err)
            pass

class MqttSubscribe(threading.Thread):
    def __init__(self, threadID, name,
        baseTopic,
        serialConnection,
        mqttClient
    ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
        self.topic = baseTopic + 'request/#'
        self.serial = serialConnection
        self.mqttClient = mqttClient
        self.mqttClient.subscribe(self.topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        try:
            command = str(msg.payload)
            
            # append request id to command
            command_parts = command.split(':')
            topic_parts = str(msg.topic).split('/')
            # the topic name is the request id
            request_id = topic_parts[len(topic_parts) - 1]
            command_parts.insert(0, request_id)
            command_with_id = ":".join(command_parts)
            logging.debug ("%s: MQTT request: %s", self.name, command_with_id)

            # send command to serial
            SerialWrite(self.serial, command_with_id)

        except Exception as err:
            logging.debug ('%s: Error sending command to serial', self.name)
            logging.debug ("%s: %s", self.name, err)

    def run (self):
        try:
            logging.debug ("%s: MQTT Sub run()", self.name)
            self.mqttClient.on_message = self.on_message
            self.mqttClient.loop_start()

        except Exception as err:
            logging.debug ("%s: MQTT Subscribe Error", self.name)
            logging.debug ("%s: %s", self.name, err)
            self.mqttClient.disconnect()

class MqttPub():
    def __init__(self, client, topic, message, host='localhost', port=1883, keepalive=60):
        self.name = "MQTT Pub"
        self.host = host
        self.port = port
        self.topic = topic
        self.message = message
        self.keepalive = keepalive
        self.client = client
        self.client.publish(self.topic, self.message)
        logging.debug ("%s: MQTT Publishing...", self.name)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            logging.debug ("%s: connected OK Returned code=%s", self.name, rc)
            self.client.publish(self.topic, self.message)
            self.client.disconnect()

        else:
            logging.debug ("%s: Bad connection Returned code=%s", self.name, rc)

    def on_disconnect(self, client, userdata,rc=0):
        self.client.loop_stop()



MQTT_BASE_TOPIC = 'emoncms/stm32/'
MQTT_HOST = 'localhost'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
TTY_PORT = '/dev/ttyACM0'
TTY_PORT = '/dev/pts/7'

# MQTT CALLBACK FUNCTIONS
def on_connect(client, userdata, flags, rc):
    if rc==0:
        logging.debug ("Connected OK Returned code = %s", rc)
    else:
        logging.debug ("Bad connection Returned code = %s", rc)

def on_disconnect(self, client, userdata,rc=0):
    logging.debug("%s: MQTT Pub - Disconnected result code %s", self.name, str(rc))
    client.loop_stop()

serialConnection = SerialConnect(TTY_PORT)

if(serialConnection.isConnected()) :

    # reuse the same mqtt client for all publish requests
    mqtt_publish_client = mqtt.Client()
    mqtt_publish_client.on_connect = on_connect
    mqtt_publish_client.on_disconnect = on_disconnect
    mqtt_publish_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)

    # reuse the same mqtt client for all subscribe requests
    mqtt_subscribe_client = mqtt.Client()
    mqtt_subscribe_client.on_connect = on_connect
    mqtt_subscribe_client.on_disconnect = on_disconnect
    mqtt_subscribe_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)

    # # create and label threads
    responses = SerialRead(2, 'Serial Responses', 
        baseTopic = MQTT_BASE_TOPIC,
        serialConnection = serialConnection.ser,
        mqttClient = mqtt_publish_client)

    requests = MqttSubscribe(3, 'MQTT Request Commands', 
        baseTopic = MQTT_BASE_TOPIC, 
        serialConnection = serialConnection.ser,
        mqttClient = mqtt_publish_client)
    
    # start in daemon mode
    responses.daemon = True
    requests.daemon = True

    # start threads
    responses.start() # not able to stop with CTRL+C
    requests.start() # able to keyboardInterrupt

    # wait for both threads to end
    responses.join()
    requests.join()
    
    try:
        # keep main thread alive
        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        print ('\n! Received keyboard interrupt, quitting threads.\n')
        pass

    logging.debug("Multi Threading Finished")
    # end
