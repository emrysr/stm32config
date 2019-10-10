import serial, sys, logging, time, traceback, getopt

def main():
    logging_init()

    port = '/dev/pts/2'
    ser = serial.Serial(port)
    # rpi gpio 5 is the reset line

    print ("---------- WRITE TO SERIAL ---------------")
    if ser.is_open: 
        logging.debug("CONNECTED on: %s", port)
        response = b'88:01:VT1:V:240\n'
        bytesWritten = ser.write(response)
        logging.info("Written %s bytes" % bytesWritten)
        logging.debug('SENT:  %s', response)
    else:
        logging.debug("NOT CONNECTED to: %s", port)
    
    ser.close()
    print ("--------------- END --------------------")

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