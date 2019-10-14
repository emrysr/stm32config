"""
SUBSCRIBE TO AN MQTT TOPIC
SUPPLY CUSTOM on_message() FUNCTION TO HANDLE RESPONSES

"""
import serial, sys, logging, time, traceback, getopt
import paho.mqtt.client as mqtt
import serial_write as write

def main(serial_port, mqtt_config):
    # setup the MQTT Client
    client = None

    try:
        logger.debug ("------ MQTT SUBSCRIBE ------")
        topic = 'request/#'
        client = MQTTClient(mqtt_config['clientId'], mqtt_config['base_topic'] + topic)
        client.on_message = on_message
        client.user_data_set(serial_port)
        client.connect(mqtt_config['broker'], mqtt_config['port'])
        try:
            client.loop_forever()
        except KeyboardInterrupt as err:
            logger.info('User Quit...')
            traceback.print_exc(file=sys.stdout)

    except KeyboardInterrupt:
        logger.info ("Shutdown requested...exiting")
    except Exception as err:
        logger.info (err)
        traceback.print_exc(file=sys.stdout)

    if client: 
        client.disconnect()

    logger.debug ("------ EXIT ------")
    sys.exit(0)


def on_message(client, serial_port, message):
    """
    MQTT on_message event handler
        client: mqtt client instance for this callback
        userdata: as set in user_data_set()
        message: topic,payload,qos and retain properties
    """
    logger.info('Received: "%s"', message.payload.decode('utf-8'))
    logger.debug('topic: %s"', message.topic)
    processInput(message,serial_port)


def processInput(message, serial_connection):
    """
    Check if received data is in correct format...
    Write result to serial port as STM32 command. eg:
        G:VT1:V:  "get VT1 voltage"
        S:T1:C:-11 "set T1 (Temperature Sensor 1) calibration offset to -11"
        L:SYS:I: "list all system inputs"
    """
    try :
        # collect mqtt request data
        action, key, prop, value = message.payload.decode("utf-8").strip().split(':')
        requestId = message.topic

        # the recieved command must be in 4 parts eg. 1[G]:2[VT1]:3[V]:4[None]
        # the topic name is the request id
        topic_parts = str(message.topic).split('/')
        requestId = topic_parts[len(topic_parts) - 1]

    except ValueError as err:
        length = len(message.payload.decode('utf-8').split(':'))
        logger.error("Input data not in correct format. Expecting 4 parts, %s given", length)
        logger.debug(message.payload)

    try:
        # map values to command properties
        request = {
            'requestId': requestId,
            'action': action,
            'key': key,
            'prop': prop,
            'value': value
        }
        command = ':'.join(request.values())
        
    except UnboundLocalError as err:
        logger.error("Serial data not in correct format")
        logger.debug(err)

    try:
        # write request to serial
        logger.info ('Sending: "%s"', serial_connection.port)

        if serial_connection.is_open:
            serial_command = str.encode(command + "\n")
            logger.debug("Written %s bytes" % serial_connection.write(serial_command))
            logger.debug('SENT:  %s', command)
        else:
            logger.debug("NOT CONNECTED to: %s", serial_connection.port)

    except Exception as err:
        logger.error('Error writing to serial')
        logger.debug(err)






class MQTTClient(mqtt.Client):
    ## return instance of itself when initialised
    def __init__(self,cname,topic,**kwargs):
        super(MQTTClient, self).__init__(cname,topic,**kwargs)
        self.last_pub_time=time.time()
        self.topic_ack=[]
        self.run_flag=True
        self.subscribe_flag=False
        self.bad_connection_flag=False
        self.connected_flag=False
        self.disconnect_flag=True
        self.disconnect_time=0.0
        self.pub_msg_count=0
        self.devices=[]
        self.enable_logger()
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        logger.warn("MQTT broker connected")
        logger.debug("MQTT on_connect():" + str(flags) + "result code " + str(rc))
        client.connected_flag=True
        client.disconnect_flag=False
        if self.topic : 
            client.subscribe(self.topic, 1)
        else :
            client.disconnect()
            raise Exception("MQTT topic not supplied")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info("MQTT topic subscribed")
        logger.debug("MQTT on_subscribe():" + "result code " + str(mid))

    def on_message(self, client, userdata, message):
        logger.warn("MQTT message received")
        logger.debug("MQTT on_message():" + "result code " + str(message))

    def on_unsubscribe(self, client, userdata, mid):
        logger.info("MQTT topic un-subscribed")
        logger.debug("MQTT on_unsubscribe():" + "mid " + str(mid))

    def on_disconnect(self, client, userdata, rc):
        logger.warn("MQTT broker disconnected")
        logger.debug("MQTT on_disconnect():" + "result code " + str(rc))
        client.connected_flag=False
        client.disconnect_flag=True
        client.loop_stop()


# take loglevel as command line option eg: --log=WARN
def logging_init(name):
    LOGLEVEL = logging.WARN
    try:
        opts, args = getopt.getopt(sys.argv[1:],"l:",["log="])
    except getopt.GetoptError:
        print ('mqtt.subscribe.py --log=<LOGLEVEL>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-l", "--log"):
            arg = arg.upper()
            allowedLogLevels = 'DEBUG,INFO,WARNING,ERROR,CRITICAL'.split(',')
            if any(arg in s for s in allowedLogLevels):
                LOGLEVEL = getattr(logging, arg, logging.WARNING)

    logging.basicConfig(stream=sys.stderr, level=LOGLEVEL)
    return logging.getLogger(name)


logger = logging_init('MQTT_Sub')

if __name__ == "__main__":
    # serial settings
    serial_port = serial.Serial()
    serial_port.baudrate = 9600
    serial_port.port = '/dev/ttyUSB0'
    serial_port.timeout = 60

    # mqtt settings

    mqtt_settings = {
        'broker': 'localhost',
        'base_topic': 'stm32config/',
        'port': 1883,
        'clientId': 'alone',
        'client': None
    }
    
    logger.info("Using module default settings for Serial and MQTT connections")

    main(serial_port, mqtt_settings)