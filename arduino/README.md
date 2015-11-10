## Arduino code for poepalBOT

### Serial Motor Controller
Monitors serial communications for motor commands, passes motor commands to DC motors via Adafruit Motor Shield. This module also handles some low level driving logic such as line following and line finding. By extensions this means that line following sensors must be attached to the arduino.
####Commands
| Command | Arguments | Function                                              |
|---------|-----------|-------------------------------------------------------|
| L       | ###       | Set the left motor to the argument (3 digit integer)  |
| R       | ###       | Set the right motor to the argument (3 digit integer) |
| S       |           | Stop both motors                                      |
| F       |           | Attempt to run line-following algorithm               |
| <       |           | Turn left until a line is found                       |
| >       |           | Turn right until a line is found                      |