#!/usr/bin/env python3
"""
Return a list of port names for connected serial devices

Thanks to Thomas: https://stackoverflow.com/a/14224477/5447015
"""
import sys
import glob
import serial

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    ports = glob.glob('/dev/tty[A-Za-z]*')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

if __name__ == '__main__':
    print('List of serial ports with connected devices:')
    print(serial_ports())
