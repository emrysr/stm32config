import serial, sys, logging, time, traceback, getopt

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
    logging_init()
    
    port = '/dev/pts/1'
    s = serial.Serial(port)

    print ("-------------- SIMULATED STM32 RESPONSES ---------------")

    if s.isOpen(): s.close()
    s.open()

    if s.is_open:
        logging.debug("CONNECTED on: %s", port)
        try:
            while True:
                line = s.readline()
                try :
                    if (line) :
                        requestId, errorCode, key, prop, value = line.strip().split(':')
                        response = {
                            'requestId': requestId,
                            'errorCode': errorCode,
                            'key': key,
                            'prop': prop,
                            'value': value
                        }
                        logging.debug("RECEIVED: %s", response)
                        line = None
                except Exception as err:
                    print (err)
                    pass

        except KeyboardInterrupt:
            logging.debug("Disconnecting...")

        except Exception:
            traceback.print_exc(file=sys.stdout)
    else:
        logging.debug("NOT CONNECTED to: %s", port)
        
    s.close()
    print ("------------------------ END ------------------------")
    sys.exit(0)




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