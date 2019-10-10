import serial, sys, logging, traceback, getopt, threading

import serial_write as write 
import serial_read as read
import mqtt_publish as pub 
import mqtt_subscribe as sub 

def main():
    logging_init()
    serial_port = serial.Serial()
    serial_port.baudrate = 9600
    serial_port.port = '/dev/pts/2'
    serial_port.timeout = 60
    # close already open port
    if serial_port.isOpen(): serial_port.close()
    serial_port.open()
    logging.debug("CONNECTED on: %s", serial_port.port)

    # begin thread for the serial read
    t1 = threading.Thread(name="READING",target=read, args=(serial_port,))
    t1.start()
    serial_port.close()


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