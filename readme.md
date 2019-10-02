# STM32 Config
Emoncms configuration module for raspberry pi based installations of emoncms with an stm32 based emonBase

![module outline](outline.png)

## install


clone this repo:
```
git clone git@github.com:emoncms/stm32config.git
```

create a link to the `stm32config-module` directory in the `emoncms` Modules directory.
```
sudo ln -s [/path/to/this/repo/]stm32config-module /var/www/emoncms/Modules/stm32config
```

click the `STM32Config` link in the emoncms sidebar to see the list


## Returned Data Structures
The different parts of this system return different data structures.

![module outline](stm32config-api-uart.png)

The `vue.js` template requires `JSON` data with the following structure:
```json
{
    "success": true,
    "message": "Value received",
    "data": [
        {
            "property" : "voltage",
            "key" : "VT1",
            "value" : 244.12
        }
    ]
}
```


## Instructions

Current list of actions:

| Instruction  | Description                  |
|--------------|------------------------------|
| GET          | Get a Key's value            |
| SET          | Set a Key's value            |
| LIST         | List all Keys                |
| SAMPLE       | Get sequence of Key's values |
| DUMP         | Get the standard output      |
| BACKUP       | Get the config settings      |
| RESTORE      | Set the config settings      |


## Keys

Inputs, Outputs or additional items are referred to as Keys:

| Example | TYPE    |
|---------|---------|
| CT1-9   | INPUT   |
| VT1-5   | INPUT   |
| SYS     | SYSTEM  |
| LED1    | OUTPUT  |


## Properties

Keys will have different properties dependant on their type:

| Property    | Related Key |
|-------------|-------------|
| Voltage     | VT1         |
| RealPower   | CT1         |
| Current     | CT1         |
| PowerFactor | CT1         |
| On          | LED1        |
| Version     | SYS         |

## Values

All the key properties can return or save a value.

eg:
```
GET -> CT1 -> REAL POWER  =  201
```