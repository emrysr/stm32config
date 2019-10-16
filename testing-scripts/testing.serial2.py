""" class based version of testing.serial.py"""

import serial, json

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

ser = serial.Serial('/dev/pts/12', 9600)
print('\nConnected to %s\n' % ser.port)
rl = ReadLine(ser)
while True:
    if(rl is not None) :
        options = {}
        command = rl.readline().decode('utf-8').strip()
        try :
            id,action,key,prop,value = command.split(':')
            if(action == 'G' and key == 'SYS' and prop == 'LIST') :
                message = 'List all'
                if (True) :
                    options['data'] = {
                        "ct": [
                            {"id":1,"key":"CT1","name":"CT1","type":"SCT013","phase":"v1","power":"200W","realPower":True,"actualPower":False,"current":False},
                            {"id":2,"key":"CT2","name":"CT2","type":"SCT013","phase":"v3","power":"100W","realPower":False,"actualPower":True,"current":False},
                            {"id":3,"key":"CT3","name":"CT3","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":False,"current":True},
                            {"id":4,"key":"CT4","name":"CT4","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":False,"current":False},
                            {"id":5,"key":"CT5","name":"CT5","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":True,"current":False},
                            {"id":6,"key":"CT6","name":"CT6","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":True,"current":False},
                            {"id":7,"key":"CT7","name":"CT7","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":False,"current":False},
                            {"id":8,"key":"CT8","name":"CT8","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":False,"current":False},
                            {"id":9,"key":"CT9","name":"CT9","type":"SCT013","phase":None,"power":"30W","realPower":False,"actualPower":False,"current":False},
                        ],
                        "vt": [
                            {"id":2,"key":"VT2","name":"VT2","vrms":True,"offset": 0},
                            {"id":3,"key":"VT3","name":"VT2","vrms":False,"offset": 0},
                            {"id":1,"key":"VT1","name":"VT1","vrms":True,"offset": 0},
                        ]
                    }
                    options['success'] = True
                else :
                    options['data'] = None
                    options['success'] = False

                # print ("%s:%s:%s:%s:%s" % (id,action,key,prop,json.dumps(options)))
                status = 1
                print ("%s:%s:%s:%s:%s" % (id,status,key,prop,json.dumps({'name':'emrys'})))

        except Exception as err:
            print ('{success:false,message:"%s"}' % err)

        rl = None
