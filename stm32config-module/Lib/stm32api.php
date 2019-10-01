<?php
namespace Emoncms;

class Stm32api
{
    public function __construct()
    {
        $this->connected = false;
        $this->ready = true;
        $this->connection = false;
// @todo: this will need to be set somewhere??
        $this->api = realpath('../stm32config/stm32api.py');
        $this->python = 'python2';
        $this->connect();
    }
    /**
     * get connection id
     *
     * @return void
     */
    private function connect()
    {
        // connect to STM32 return connection id
        $this->connection = trim(`$this->python $this->api --action=CONNECT`);
        return $this->connection;
    }

    /**
     * get list of data
     *
     * @return void
     */
    public function list()
    {
        if(!$this->connection) {
            $this->connect();
        }
        // @todo: while loop to test for connection until connected

        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=LIST --json
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

    public function set($params) {
        
        if(!$this->connection) {
            $this->connect();
        }
        // todo: while loop to test for connection until connected

        // todo: santize inputs
        $id = $params['id'];
        $properties = $params['properties'];
        $values = $params['values'];

        // @todo loop through multiple set requests as single requests;
        $property = $properties;
        $value = $values;
        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=SET --property=$property --id=$id --value=$value --json
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
        $id = $params['id'];
        $properties = $params['properties'];

        // @todo loop through multiple set requests as single requests;
        $property = $properties;
        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=GET --property=$property --id=$id --json
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
        $id = $params['id'];
        $properties = $params['properties'];

        // @todo loop through multiple set requests as single requests;
        $property = $properties;
        $command = <<<eot
$this->python $this->api --connection=$this->connection --action=SAMPLE --id=$id --json
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
