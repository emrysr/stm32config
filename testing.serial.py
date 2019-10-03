"""
simple testing of reading and parsing serial data
"""

import serial
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
buf = bytearray()

while True:
    index = max(1, min(2048, ser.in_waiting))
    data = ser.read(index)
    index = data.find(b"\n")
    if index >= 0:
        r = buf + data[:index+1]
        buf[0:] = data[index+1:]
        try:
          print (r.decode().strip().split(':'))
        except: 
          pass
    else:
        buf.extend(data)