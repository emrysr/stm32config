<?php
namespace Emoncms;
/*
 All Emoncms code is released under the GNU Affero General Public License.
 See COPYRIGHT.txt and LICENSE.txt.
 
 ---------------------------------------------------------------------
 Emoncms - open source energy visualisation
 Part of the OpenEnergyMonitor project:
 http://openenergymonitor.org
*/

// no direct access
defined('EMONCMS_EXEC') or die('Restricted access');

use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\UriInterface;
interface RequestFactoryInterface
{
    /**
     * Create a new request.
     *
     * @param string $method The HTTP method associated with the request.
     * @param UriInterface|string $uri The URI associated with the request.
     * 
     * @ignore not used because the API used does not respond to HTTP requests
     */
    public function createRequest(string $method, $uri): RequestInterface;
}

/**
 * STM32 Config Methods
 */
class Stm32Config
{
    /**
     * test to ensure all is ready
     */
    public function __construct()
    {
        $this->ready = true; // once all loaded this is set to true
        $this->stm32api = null; // api class instance to be used by all the methods
        $this->returnCommand = true; // see the system command executed by the api
        $this->returnResponseText = true; // see the unaltered text returned by the api
    }

    /**
     * list all items for list page
     * 
     * @return array
     */
    public function getAll()
    {
        require "Modules/stm32config/Lib/stm32api.php";
        $this->stm32api = new Stm32api();
        $api_responseText = $this->stm32api->list();
        $api_response = json_decode($api_responseText, true); // get list of values from SMT32 via python api
        if ($api_response) {
            $response = array();
            $response['success'] = $api_response['success'];
            $response['data'] = $api_response['data'];
            $response['action'] = $api_response['action'];
            $response['message'] = $api_response['message'];
            $response['connection'] = $api_response['connection'];

            if($this->returnCommand) {
                $response['command'] = $api_response['command'];
            }
            if($this->returnResponseText) {
                $response['responseText'] = $api_responseText;
            }
            return $response;

        } else {
            return array(
                'message' => 'API response not in correct format',
                'success' => false,
                'responseText' => $api_responseText
            );
        }
    }

    /**
     * get the property values of an item by id
     *
     * @param object $params {properties,id}
     * @return void
     */
    public function get($params)
    {
        global $route;
        require "Modules/stm32config/Lib/stm32api.php";
        $this->stm32api = new Stm32api();

        $req = array(
            'controller' => $route->controller,
            'action' => $route->action,
            'params' => $params,
        );
        // @todo : multi property set
        $api_responseText = $this->stm32api->get($params);
        
        // parse response as JSON. returns null on error
        $api_response = json_decode($api_responseText, true);

        if($api_response) {
            $res = array();
            if($this->returnCommand) {
                $res['command'] = $api_response['command'];
            }
            if($this->returnResponseText) {
                $res['responseText'] = $api_responseText;
            }
            $res['message'] = $api_response['message'];
            
            $response = array();

            if($api_response['success']) {
                $res["property"] = $api_response['property'];
                $res["id"] = $api_response['id'];
                $res["connection"] = $api_response['connection'];

                $response['data'] = $api_response['data'];
            }

            $response['success'] = $api_response['success'];
            $response['req'] = $req;
            $response['res'] = $res;

            return $response;

        } else {
            return array(
                'message' => 'API response not in correct format',
                'success' => false,
                'responseText' => $api_responseText
            );
        }

    }
    
    /**
     * set the property values of an item by id
     *
     * @param object $params {properties,values,id}
     * @return void
     */
    public function set($params)
    {
        global $route;
        require "Modules/stm32config/Lib/stm32api.php";
        $this->stm32api = new Stm32api();

        $req = array(
            'controller' => $route->controller,
            'action' => $route->action,
            'params' => $params,
        );
        // @todo : multi property set
        $api_responseText = $this->stm32api->set($params);
        
        // parse response as JSON. returns null on error
        $api_response = json_decode($api_responseText, true);

        if($api_response) {
            $res = array();
            if($this->returnCommand) {
                $res['command'] = $api_response['command'];
            }
            if($this->returnResponseText) {
                $res['responseText'] = $api_responseText;
            }
            $res['message'] = $api_response['message'];
            
            $response = array();

            if($api_response['success']) {
                $res["property"] = $api_response['property'];
                $res["value"] = $api_response['value'];
                $res["id"] = $api_response['id'];
                $res["connection"] = $api_response['connection'];

                $response['data'] = $api_response['data'];
            }

            $response['success'] = $api_response['success'];
            $response['req'] = $req;
            $response['res'] = $res;

            return $response;
            
        } else {
            return array(
                'message' => 'API response not in correct format',
                'success' => false,
                'responseText' => $api_responseText
            );
        }
    }
    
    /**
     * get the property values of an item by id
     *
     * @param object $params {properties,id}
     * @return void
     */
    public function sample($params)
    {
        global $route;
        require "Modules/stm32config/Lib/stm32api.php";
        $this->stm32api = new Stm32api();

        $req = array(
            'controller' => $route->controller,
            'action' => $route->action,
            'params' => $params,
        );
        // @todo : multi property set
        $api_responseText = $this->stm32api->sample($params);
        
        // parse response as JSON. returns null on error
        $api_response = json_decode($api_responseText, true);

        if($api_response) {
            $res = array();
            if($this->returnCommand) {
                $res['command'] = $api_response['command'];
            }
            if($this->returnResponseText) {
                $res['responseText'] = $api_responseText;
            }
            $res['message'] = $api_response['message'];
            
            $response = array();

            if($api_response['success']) {
                $res["id"] = $api_response['id'];
                $res["connection"] = $api_response['connection'];

                $response['data'] = $api_response['data'];
            }

            $response['success'] = $api_response['success'];
            $response['req'] = $req;
            $response['res'] = $res;

            return $response;

        } else {
            return array(
                'message' => 'API response not in correct format',
                'success' => false,
                'responseText' => $api_responseText
            );
        }

    }

}
