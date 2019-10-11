"""
PUBLISH TO A MQTT TOPIC

simpler example:
    import paho.mqtt.publish as publish
    publish.single("paho/test/single", "payload", hostname="iot.eclipse.org")

"""
import serial, sys, logging, time, traceback, getopt
import paho.mqtt.client as mqtt

broker = 'localhost'
port = 1883
topic = 'stm32config/response/888'
clientId = 'testing4321'
client = None

def main():
    # setup the MQTT Client
    client = None

    try:
        logger.debug ("------ MQTT PUBLISH -------")

        client = MQTTClient(clientId, topic)
        client.on_connect = on_connect
        client.on_disconnect = client.on_disconnect
        client.on_publish = client.on_publish
        client.connect(broker,port)
        try:
            client.loop_forever()
        except:
            raise

    except KeyboardInterrupt:
        logger.info ("Shutdown requested...exiting")
    except Exception as err:
        logger.info (err)
        traceback.print_exc(file=sys.stdout)

    if client: 
        client.disconnect()

    logger.debug ("------ EXIT ------------------")
    sys.exit(0)


def on_connect(client, userdata, flags, rc):
    logger.warn("MQTT broker connected")
    logger.debug("MQTT on_connect():" + str(flags) + "result code " + str(rc))
    client.connected_flag=True
    client.disconnect_flag=False
    # send data if ready
    if client.topic : 
        logger.debug(client.topic)
        # example of what the stm32 would respond with
        message = "1:G:VT1:V:244"
        client.publish(client.topic, message)
    else :
        logger.debug("no topic")
        # client.disconnect()
        raise Exception("MQTT topic not supplied")















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

    def on_publish(self, client, userdata, mid):
        logger.warn("MQTT message published")
        logger.debug("MQTT on_publish():" + "result code " + str(mid))
        logger.debug("disconnecting...")
        client.disconnect()

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
            allowedLogLevels = 'DEBUG,INFO,WARNING,ERROR,CRITICAL'.split(',')
            if any(arg in s for s in allowedLogLevels):
                LOGLEVEL = getattr(logging, arg.upper(), logging.WARNING)

    logging.basicConfig(stream=sys.stderr, level=LOGLEVEL)
    return logging.getLogger(name)


logger = logging_init('PUB')

if __name__ == "__main__":
    main()