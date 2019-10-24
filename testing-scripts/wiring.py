#!/usr/bin/env python3
import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',9600)
wiringpi.serialPuts(serial,'RES:[{"name":"Dave"}]\n\r')
