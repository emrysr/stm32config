import sys, traceback, getopt, logging, serial, json
import mqtt_publish

def main(serial_port, mqtt_settings):
    try:
        ser = serial_port
    except NameError:
        logger.error('no serial port passed')
        traceback.print_exc(file=sys.stdout)

    if ser.isOpen(): ser.close()
    try:
        ser.open()
    except serial.SerialException as err:
        logger.debug("Serial Connection error: %s", err)

    if ser.is_open:
        logger.debug("Listening...")
        try:
            while True:
                line = ser.readline()
                try :
                    if (line) :
                        processInput(line, mqtt_settings)
                        line = None
                except KeyboardInterrupt:
                    logger.debug("Disconnecting...")
                    traceback.print_exc(file=sys.stdout)
                except TypeError as err:
                    logger.debug(err)
                    traceback.print_exc(file=sys.stdout)

        except KeyboardInterrupt:
            logger.debug("Disconnecting...")
            traceback.print_exc(file=sys.stdout)

    else:
        raise serial.SerialException('Serial connection is not open')
    
    ser.close()
    print ("------------------------ END ------------------------")
    sys.exit(0)


def processInput(line, mqtt_settings) :
    """ take line of serial input and check validity before publishing response via mqtt
    """
    is_response = True

    logger.info("Received: %s", line)
    response = None

    try :
        # collect serial response data
        requestId, errorCode, key, prop, value = line.decode("utf-8").strip().split(':')
    except ValueError as err:
        logger.error("Error parsing serial data")
        # logger.debug(err)
    
    try :
        errorCode = int(errorCode)
    except ValueError as err:
        is_response = False
        logger.debug("Serial line is not stm32 response")
    try:
        response = {
            'requestId': requestId,
            'errorCode': errorCode,
            'key': key,
            'prop': prop,
            'value': value
        }
    except UnboundLocalError as err:
        logger.error("Serial data not in correct format")
        # logger.debug(err)

# try :
    if(is_response) :
    # publish response to mqtt
        topic = mqtt_settings['base_topic'] + "response/" + requestId
        payload = json.dumps(response)

        logger.info("Publishing to: %s", topic)
        logger.debug("payload: %s", payload)

        mqtt_publish.main(mqtt_settings, topic, payload)
    else :
        logger.debug("Serial data not response")

# except Exception as err:
#     logger.error ("Cannot publish to MQTT")
#     logger.debug (err)


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


logger = logging_init(__name__)

if __name__ == "__main__":
    serial_port = serial.Serial()
    serial_port.baudrate = 9600
    serial_port.port = '/dev/ttyACM0'
    serial_port.timeout = 60

    mqtt_settings = {
        'broker': 'localhost',
        'base_topic': 'stm32config/',
        'port': 1883,
        'clientId': 'alone',
        'client': None
    }
    logger.info("Using module default settings for Serial and MQTT connections")

    main(serial_port, mqtt_settings)