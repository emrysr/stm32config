"""
SUBSCRIBE TO AN MQTT TOPIC
SUPPLY CUSTOM on_message() FUNCTION TO HANDLE RESPONSES

"""
import serial, sys, logging, time, traceback, getopt
import paho.mqtt.client as mqtt

broker = 'localhost'
port = 1883
topic = 'stm32config/request/#'
clientId = 'testing4321'
client = None

def main():
    # setup the logging scripts
    logging_init()
    # setup the MQTT Client
    client = None

    try:
        logging.debug ("------ MQTT SUBSCRIBE -------")

        client = MQTTClient(clientId, topic)
        client.on_message = on_message
        client.on_connect = client.on_connect
        client.on_disconnect = client.on_disconnect
        client.on_subscribe = client.on_subscribe
        client.on_unsubscribe = client.on_unsubscribe
        client.connect(broker,port)
        try:
            client.loop_forever()
        except:
            raise

    except KeyboardInterrupt:
        logging.info ("Shutdown requested...exiting")
    except Exception as err:
        logging.info (err)
        traceback.print_exc(file=sys.stdout)

    if client: 
        client.disconnect()

    logging.debug ("------ EXIT ------------------")
    sys.exit(0)


def on_message(client, userdata, message):
    """
    Edit this function to react to incomming messages on the subscribed topic
    """

    logging.info("MQTT message received")
    logging.debug("MQTT on_message():" + "result code " + str(message.payload))
    logging.debug ("------ START -----")
    # test incoming command format
    # todo: test input command pattern
    command = str(message.payload)
    # append request id to command
    command_parts = command.split(':')
    topic_parts = str(message.topic).split('/')

    # the topic name is the request id
    request_id = topic_parts[len(topic_parts) - 1]
    command_parts.insert(0, request_id)
    command_with_id = ":".join(command_parts)
    logging.warn ("MQTT message: %s", command_with_id)

    logging.debug ("------ END -------")















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
        logging.warn("MQTT broker connected")
        logging.debug("MQTT on_connect():" + str(flags) + "result code " + str(rc))
        client.connected_flag=True
        client.disconnect_flag=False
        if self.topic : 
            client.subscribe(self.topic, 1)
        else :
            client.disconnect()
            raise Exception("MQTT topic not supplied")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info("MQTT topic subscribed")
        logging.debug("MQTT on_subscribe():" + "result code " + str(mid))

    def on_message(self, client, userdata, message):
        logging.warn("MQTT message received")
        logging.debug("MQTT on_message():" + "result code " + str(message))

    def on_unsubscribe(self, client, userdata, mid):
        logging.info("MQTT topic un-subscribed")
        logging.debug("MQTT on_unsubscribe():" + "mid " + str(mid))

    def on_disconnect(self, client, userdata, rc):
        logging.warn("MQTT broker disconnected")
        logging.debug("MQTT on_disconnect():" + "result code " + str(rc))
        client.connected_flag=False
        client.disconnect_flag=True
        client.loop_stop()


# take loglevel as command line option eg: --log=WARN
def logging_init():
    LOGLEVEL = logging.WARN
    try:
        opts, args = getopt.getopt(sys.argv[1:],"l:",["log="])
    except getopt.GetoptError:
        print ('mqtt.subscribe.py --log=<LOGLEVEL>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-l", "--log"):
            allowedLogLevels = 'DEBUG,INFO,WARNING,ERROR,CRITICAL'.split(',')
            if any(arg in s for s in allowedLogLevels):
                LOGLEVEL = getattr(logging, arg.upper(), logging.WARNING)

    logging.basicConfig(stream=sys.stderr, level=LOGLEVEL)

if __name__ == "__main__":
    main()
