import serial, sys, logging, traceback, getopt, threading, time, os
from multiprocessing import Process

import mqtt_subscribe as sub

def main(serial_port, mqtt_config):
    # close already open port
    if serial_port.isOpen(): serial_port.close()
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
        # p1 = Process(target=sub.main, args=(serial_port, mqtt_config,))
        # p1.start()
        # p1.join()
        sub.main(serial_port, mqtt_config)
    except KeyboardInterrupt:
        logger.debug("Disconnecting...")
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)
    # serial_port.close()



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


logger = logging_init('MQTT_LISTEN')

if __name__ == "__main__":

    # serial settings
    serial_port = serial.Serial()
    serial_port.baudrate = 9600
    serial_port.port = '/dev/ttyACM0'
    serial_port.timeout = 60

    # mqtt settings
    mqtt_settings = {
        'broker': 'localhost',
        'base_topic': 'stm32config/',
        'port': 1883,
        'clientId': 'alone',
        'client': None
    }
    
    logger.info("Using default settings for Serial and MQTT connections")

    main(serial_port, mqtt_settings)