#!/usr/bin/python
""" Interact with the STM32 chip and return responses

For more details:
    ./stm32api.py --help
"""

import sys, getopt, uuid, json
import datetime, math, random, time # not required in production

_DEBUG = False
_API_VERSION = 0.1

def main(argv):
  action = 'CONNECT'
  connection = None
  jsonFormat = False
  debug = _DEBUG
  version = _API_VERSION
  options = {}
  quiet = False

  try:
    # example input: ./stm32api.py --connection=set_0001 --action=SET --key=B1 --value=abc --property=size --json
    opts, args = getopt.getopt(argv, "c:a:i:p:v:jhdq", ["connection=", "action=", "key=", "property=", "value=", "json", "help", "version", "debug", "quiet"])
    
    # parse 
    for opt, arg in opts:
      if opt in ("-c", "--connection"):
        connection = arg
      elif opt in ("-j", "--json"):
        jsonFormat = True
      elif opt in ("-d", "--debug"):
        debug = True
      elif opt in ("-a", "--action"):
        action = arg
      elif opt in ("-q", "--quiet"):
        quiet = True
      elif opt in ("-k", "--key"):
        options['key'] = arg
      elif opt in ("-v", "--value"):
        options['value'] = arg
      elif opt in ("-p", "--property"):
        options['property'] = arg
      elif opt in ("-h", "--help"):
        raise getopt.GetoptError('', 100)
      elif opt in ("--version"):
        action = 'VERSION'

    if connection is not None:
      options['success'] = True




      if action == 'LIST':
        # todo: get list of values. (TBC)
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





      elif action == 'GET':
        # todo: get the value from the chip and set key/value to options['data']
        message = 'Value of property returned'
        options['data'] = [{ 'key':options['key'], options['property']: "%s" % datetime.datetime.now() }]
        # fake delay to simulate time taken to do the sampling
        time.sleep(1.2)



      elif action == 'SET':
        # todo: set the value on the chip and set options['success'] to True if successful
        if (True) :
          message = 'Setting value successful'
          options['success'] = True
          options['data'] = []
        else :
          message = 'Nothing changed'
          options['success'] = False
          options['data'] = []
        
        # fake delay to simulate time taken to do the sampling
        time.sleep(1.2)





      elif action == 'SAMPLE':
        # todo: sample the given port
        message = 'Sample collected'
        
        # fake data from random numbers
        # 14 data points between 0 and 1 following a sin() curve with added random numbers
        sample = []
        for i in range(0, 14):
            radians = i + random.random()
            sample.append((i, math.sin(radians)))

        # fake delay to simulate time taken to do the sampling
        time.sleep(2)

        options['data'] = [sample]
    
    

      else:
        # todo standardise error codes
        # return error when action not in above list
        options['success'] = False
        raise getopt.GetoptError('Unrecognized action. Bad Request', 400)

      options['message'] = message
      options['connection'] = connection

    else:
      # no unique connection id given. return one with error message
      connection = uuid.uuid1()
      if action == 'CONNECT':
        options['message'] = 'Get new connection ID'
        # todo: negotiate with STM32 for unique ID to prevent mixing responses
        options['data'] = { 'id': connection.__str__() }
      else:
        options['success'] = False
        options['message'] = 'no connection given'
        options['connection'] = "%s" % connection

    if action == 'VERSION':
      # todo: get STM32 chip version or api version ? (TBC)
      message = 'v%s' % version
      print message
      sys.exit(2)

    options['action'] = action

    if (not quiet):
      # DEBUG CONNECTION ID
      if (debug == True) :
        print ''
        print '______DEBUG_______'
        print 'JSON output: %s' % (jsonFormat == True)
        print 'connection: "%s"' % connection
        print 'action:     "%s"' % action
        print 'options:     %s' % options
        print 'args:        %s' % ', '.join(str(x) for x in args)
        print ''
        print '______OUTPUT_______:'
        print ''

      # output json version of data
      if (jsonFormat) :
        print json.dumps(options)
      else:
        if (options['action'] == 'CONNECT') :
          print '%s' % connection
        else :
          print ' %s' % '\n '.join((str(key)+" = "+str(value)) for key,value in options.items())

      if (debug == True) :
        print ""
        print "______END_______"

  except getopt.GetoptError as e:
    if (not jsonFormat) :
      print e
      print "EmonCMS STM32 API. Version: v%s" % version
      print """
  Arguments:
    -c [--connection=]  unique identifier for request. Required.
    -p [--property=]    key property to get or set
    -d [--value=]       key's property value to set
    -a [--action=]      action to perform
    -k [--key=]         unique id of input/output item to work with
    -j [--json]         return output as JSON. All responses have {success: bool, message: string, data: mixed}
                        Returned values held in "data" property.
    -d [--debug]        return version number
    -q [--quiet]        supress output
    -h [--help]         show this help
    --version           return version number

  Actions:
    GET  - request variable
    SET  - set variable
    LIST  - set variable
    VERSION - get version

  Examples:
    Get the value of the property "power" of item "CT2". Return results as "JSON" data. Identified as "AAAA"
        ./stm32api.py -cAAAA --action=GET --key=CT2 --property=power --json

    Set the value of the property "burdon" of item "VT1" to "20". Return results as "JSON" data. Identified as "user_0001"
        ./stm32api.py --connection=user_0001 --action=SET --key=VT1 --value=20 --property=burdon --json
        
    Get a list of all properties. Response tagged with id "1234"
        ./stm32api.py -c 1234 --action=LIST

    Show this Help
        ./stm32api.py --help

    Show the version number
        ./stm32api.py --version
"""
    else:
      options['message'] = e[0]
      print json.dumps(options)

    sys.exit(2)

if __name__ == "__main__":
  main(sys.argv[1:])
