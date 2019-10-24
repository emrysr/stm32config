import serial, sys, logging, time, traceback, getopt


def send(serial_port, message):
    # rpi gpio 5 is the reset line
    try:
        logger.debug (" ------- WRITE TO SERIAL -------")
        if ser.is_open: 
            logger.debug("CONNECTED on: %s", serial_port.port)
            response = b'88:01:VT1:V:240\n'
            bytesWritten = ser.write(response)
            logger.info("Written %s bytes" % bytesWritten)
            logger.debug('SENT:  %s', response)
        else:
            logger.debug("NOT CONNECTED to: %s", serial_port.port)
    except NameError:
        logger.error('no serial port passed')
        traceback.print_exc(file=sys.stdout)


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
    logger.info("Module used to write serial data. Call write() with Serial object and message")
    logger.debug("Using this module as standalone. default settings applied.")
    
    # serial settings
    serial_port = serial.Serial()
    serial_port.baudrate = 9600
    serial_port.port = '/dev/ttyUSB0'
    serial_port.timeout = 60
    message = "G:SYS:HELLO"
    send(serial_port, message)