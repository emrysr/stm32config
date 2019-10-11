""" class based version of testing.serial.py"""

import serial

class ReadLine:
    def __init__(self, ser):
        self.buf = bytearray()
        self.ser = ser

    def readline(self):
        index = self.buf.find(b"\n")
        if index >= 0:
            partial = self.buf[:index+1]
            self.buf = self.buf[index+1:]
            return partial + b':ERROR'
        while True:
            index = max(1, min(2048, self.ser.in_waiting))
            data = self.ser.read(index)
            index = data.find(b"\n")
            if index >= 0:
                r = self.buf + data[:index+1]
                self.buf[0:] = data[index+1:]
                return r
            else:
                self.buf.extend(data)

ser = serial.Serial('/dev/ttyACM0', 9600)
rl = ReadLine(ser)

while True:
    print(rl.readline().decode('utf-8').strip().split(':'))

