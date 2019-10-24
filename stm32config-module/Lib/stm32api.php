<?php
namespace Emoncms;
/**
 * You can send serial commands to the stm32 chip via MQTT
 *   - commands are sent to a 'request/[id]' topic
 *   - the stm32 chip responds by posting to the 'response/[id]' topic
 * 
 * this class will simplify the MQTT opperations into methods
 * the methods will pair up to this module's api endpoints in the controller
 * eg:
 *  Requesting the enpoint "stm32config/list.json" calls a model function :
 *  Emoncms\Stm32config\getAll() then calls the api function : 
 *  $this->stm32api->list();
 */

class Stm32api
{
    public function __construct($mqtt_broker_settings)
    {
        $this->mqtt = $mqtt_broker_settings;
    }

    /**
     * Return list of data from mqtt response topic
     * 
     * send request command to mqtt
     * subscribe to response topic
     * return the next message on that topic
     *
     * @return void
     */
    public function list()
    {
        $id = uniqid();
        $response = new \Mosquitto\Client('list response '. $id);
        $request = new \Mosquitto\Client('list request '. $id);
        // $request->onLog('var_dump');
        // $response->onLog('var_dump');
        $base_topic = 'stm32config/';
        $command = 'G:SYS:LIST:';
        $keepalive = 50;
        $mid = 0;
        $connected = false;

        $request->onConnect(function($rc, $message) use(&$request, $base_topic, $id, $command, &$mid, &$connected) {
            if($rc===0) {
                $connected = true;
                $topic = $base_topic . 'request/' . $id;
                $payload = $command;
                $mid = $request->publish($topic, $payload);
            } else {
                echo $message;
            }
            $request->disconnect();
        });

        $response->onConnect(function($rc, $message) use(&$response, $base_topic, $id) {
            echo 'response connected';
            $topic = $base_topic .'request/'.$id;
            if($rc===0) {
                $response->subscribe($topic, 1);
            }
        });

        $response->onMessage(function(\Mosquitto\Message $message) use(&$response) {
            $response->disconnect();
            echo 'on response message';
            return $message->payload;
        });

        $request->setCredentials($this->mqtt['user'],$this->mqtt['password']);
        $response->setCredentials($this->mqtt['user'],$this->mqtt['password']);

        $request->connect($this->mqtt['host'], $this->mqtt['port'], $keepalive);
        $response->connect($this->mqtt['host'], $this->mqtt['port'], $keepalive);
        
        $start = time();
        while((time()-$start)<5.0) {
            if($connected) {
                $response->loop(10); 
                if ((time()-$start)>=3.0) {
                    $response->disconnect();
                }
            }
            usleep(50000);
        }

        $request->loopForever();
    }

    public function set($params) {
        
        if(!$this->connection) {
            $this->connect();
        }
        // todo: while loop to test for connection until connected

        // todo: santize inputs
        $key = $params['key'];
        $properties = $params['properties'];
        $values = $params['values'];

        // @todo loop through multiple set requests as single requests;
        $property = $properties;
        $value = $values;
        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=SET --key=$key --property=$property --value=$value --json
eot;
        $response = `$command`;
        
        // not required in production
        $tmp = json_decode($response, true);
        $tmp['command'] = $command;
        $response = json_encode($tmp);

        return $response;
    }

    public function get($params) {
        
        if(!$this->connection) {
            $this->connect();
        }
        // todo: while loop to test for connection until connected
        
        // todo: santize inputs
        $key = $params['key'];
        $properties = $params['properties'];

        // @todo loop through multiple set requests as single requests;
        $property = $properties;
        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=GET --key=$key --property=$property --json
eot;
        $response = `$command`;
        
        if($response) {
            $tmp = json_decode($response, true);
            $tmp['command'] = $command;
            $response = json_encode($tmp);
        
            return $response;

        } else {
            return json_encode(array(
                'message' => 'API call unsuccessful',
                'success' => false,
                'command' => $command
            ));
        }
    }


    public function sample($params) {
        
        if(!$this->connection) {
            $this->connect();
        }
        // todo: while loop to test for connection until connected
        
        // todo: santize inputs
        $key = $params['key'];
        $properties = $params['properties'];

        // @todo loop through multiple set requests as single requests;
        $property = $properties;
        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=SAMPLE --key=$key --json
eot;
        $response = `$command`;
        
        if($response) {
            $tmp = json_decode($response, true);
            $tmp['command'] = $command;
            $response = json_encode($tmp);
        
            return $response;

        } else {
            return json_encode(array(
                'message' => 'API call unsuccessful',
                'success' => false,
                'command' => $command
            ));
        }
    }
}
