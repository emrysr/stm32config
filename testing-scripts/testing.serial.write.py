#!/usr/bin/env python3
import serial
import ports

serial_ports = ports.serial_ports()
serial_port = serial.Serial(serial_ports[0],9600)
serial_port.write(str("{['G:SYS:NAME']}\n\r")) 
