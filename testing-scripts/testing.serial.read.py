#!/usr/bin/env python3
"""
simple testing of reading and parsing serial data split by ":"
"""

import serial
def main(port) :
    if not port: 
        port = "/dev/ttyAMA0"

    ser = serial.Serial(port, 9600, timeout=None)
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

if __name__ == "__main__" :
    main('/dev/ttyUSB1')
