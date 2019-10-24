"""
PUBLISH TO A MQTT TOPIC

simpler example:
    import paho.mqtt.publish as publish
    publish.single("paho/test/single", "payload", hostname="iot.eclipse.org")

"""
import serial, sys, logging, time, traceback, getopt
import paho.mqtt.client as mqtt

def main(mqtt_config, topic, payload):
    # setup the MQTT Client
    client = None

    try:
        client = MQTTClient(mqtt_config['clientId'], topic, payload)
        client.on_publish = on_publish
        client.username_pw_set(username= mqtt_config['user'], password= mqtt_config['password'])
        client.connect(mqtt_config['broker'], mqtt_config['port'])
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
    if userdata.topic : 
        logger.debug(userdata.topic)
        # example of what the stm32 would respond with
        # message = "1:G:VT1:V:244"
        client.publish(userdata.topic, payload)
        client.loop_forever()
    else :
        logger.debug("no topic")
        # client.disconnect()
        raise Exception("MQTT topic not supplied")

def on_publish(client, userdata, mid):
    logger.warn("MQTT message published")
    logger.debug("MQTT on_publish(): message id " + str(mid))
    client.connected_flag=True
    client.disconnect_flag=False
    # send data if ready
    if topic : 
        logger.info('Message Sent')
        logger.debug('message id = %s' % mid)
        client.loop_stop()
        client.disconnect()
    else :
        logger.debug("no topic")
        # client.disconnect()
        raise Exception("MQTT topic not supplied")















class MQTTClient(mqtt.Client):
    ## return instance of itself when initialised
    def __init__(self,cname,topic,payload,**kwargs):
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
        # self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        logger.warn("MQTT broker connected")
        logger.debug("MQTT on_connect():" + str(flags) + "result code " + str(rc))
        client.connected_flag=True
        client.disconnect_flag=False

    def on_publish(self, client, userdata, mid):
        logger.warn("MQTT message published")
        logger.debug("MQTT on_publish():" + "result code " + str(mid))
        logger.debug("disconnecting...")
        client.loop_stop()
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


logger = logging_init('MQTT_PUBLISH')

if __name__ == "__main__":
    # mqtt settings

    mqtt_settings = {
        'broker': 'localhost',
        'base_topic': 'stm32config/',
        'port': 1883,
        'clientId': 'alone',
        'client': None,
        'user': 'emonpi',
        'password': 'emonpimqtt2016'
    }
    topic = mqtt_settings['base_topic'] + 'response/88'
    payload = 'response payload'
    logger.debug("Using module default settings for MQTT connections")

    main(mqtt_settings, topic, payload)