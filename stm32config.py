import serial, sys, logging, traceback, getopt, time, os

# from multiprocessing import Process
from threading import Thread

import paho.mqtt.client as mqtt
import stm32config_mqtt_listen as listen_mqtt
import stm32config_serial_listen as listen_serial

def main():
    """
    create serial connection
    create mqtt connection
    start process to handle listening on serial connection
    start process to handle listening on mqtt connection
    """

    # serial settings
    serial_port = serial.Serial()
    serial_port.baudrate = 9600
    serial_port.port = '/dev/ttyACM1'
    serial_port.timeout = 60

    # mqtt settings
    mqtt_broker_settings = {
        'broker': 'localhost',
        'base_topic': 'stm32config/',
        'port': 1883,
        'clientId': 'alone',
        'client': None,
        'user': 'emonpi',
        'password': 'emonpimqtt2016'
    }
    
    try:
        serial_port.open()
    except serial.SerialException as err:
        logger.error("Serial Connection error:\n\t%s", err)
        serial_port.close()
        logger.debug ("------- END -------")
        sys.exit(1)

    logger.debug("CONNECTED on: %s", serial_port.port)
    
    # begin thread for the serial read
    try:
        s = Thread(target=listen_serial.main, args=(serial_port, mqtt_broker_settings,))
        s.start()
        s.join()

        m = Thread(target=listen_mqtt.main, args=(serial_port, mqtt_broker_settings,))
        m.start()
        m.join()

    except KeyboardInterrupt:
        logger.debug("Disconnecting...")
        traceback.print_exc(file=sys.stdout)
        serial_port.close()
        sys.exit(0)



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


logger = logging_init(__name__)

if __name__ == "__main__":
    main()