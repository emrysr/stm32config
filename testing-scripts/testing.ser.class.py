import serial,time

class Connection:
    def __init__(self, port):
        self.serial = serial.Serial(port, 9600, timeout=2)
        print("connected %s" % self.serial.write(10))
        
class SerialWrite:
    def __init__(self, serial):
        self.serial = serial

    def send(self, text):
        print("sending '%s'..." % text)
        return self.serial.write(b'A')
    
class SerialRead:
    def __init__(self, serial):
        self.serial = serial

    def read(self):
        print('reading...')
        return self.serial.read()

 try:
    #serialConnection = Connection()
    serialConnection = Connection('/dev/ttyACM0').serial
    w = SerialWrite(serialConnection)
    r = SerialRead(serialConnection)

    msg = 'abc'
    print("sending success? %s" % w.send(msg))
    print("reading success? %s" % r.read())

    time.sleep(0.1)
    serialConnection.close()

except serial.serialutil.SerialException:
    print ('Serial connection problem')
    print (serial)
    
except serial.serialutil.SerialTimeoutException:
    print ('Serial connection timed out')

finally:
    print ('closed')