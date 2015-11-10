#include <Wire.h>
#include <Adafruit_MotorShield.h>
#define FORWARD 1
#define BACKWARD 2
#define RELEASE 3

Adafruit_MotorShield MS;
Adafruit_DCMotor *leftm, *rightm;
const byte LEFT_MOTOR_PORT = 1;
const byte RIGHT_MOTOR_PORT = 2;
const int LEFT_SENSOR_PIN = A5, RIGHT_SENSOR_PIN = A3;
const int LEFT_SENSOR_THRESH = 800;
const int RIGHT_SENSOR_THRESH = 800;
const int LEFT_HALL_A_PIN = 1, LEFT_HALL_B_PIN = 2;
const int RIGHT_HALL_A_PIN = 3, RIGHT_HALL_B_PIN = 4;
int la_prevstate = 0, lb_prevstate = 0, ra_prevstate = 0, rb_prevstate = 0;
int la_state = 0, lb_state = 0, ra_state = 0, rb_state = 0;
int left_sensor, right_sensor;
int left_encoder = 0, right_encoder = 0;
char incoming_msg[3] = ""; //three bytes of data
char command_arg[3];
char command;
int actual_speed;
boolean argParse = false;
boolean foundLine = false;
boolean unknownCommandFlag = false;

void setup() {
  Serial.begin(9600);
  MS = Adafruit_MotorShield();
  MS.begin();
  leftm = MS.getMotor(LEFT_MOTOR_PORT);
  rightm = MS.getMotor(RIGHT_MOTOR_PORT);
  leftm -> setSpeed(0);
  rightm -> setSpeed(0);
  leftm -> run(BACKWARD);
  rightm -> run(FORWARD);
}

void loop() {

  //Encoder accumulating
  accumulateEncoders();
  
  //Command parsing
  if (Serial.available()) {
    if (!argParse) {
      command = Serial.read();
      Serial.print("Command received: " + String(command) + "\n");
      unknownCommandFlag = true;
      resetDriveParams();
      //flag argParse if command needs additional argument
      argParse = (command == 'L' || command == 'R');
      Serial.print("Waiting for args? " + String(argParse) + "\n");
    } else {
      //we are looking for arguments to command
      //currently only looking for 3 byte arguments
      if (Serial.available() >= 3) { //4 bytes indicates 3 bytes and one string terminator
        Serial.readBytes(incoming_msg, 3);
        //store 3 bytes of argument
        command_arg[2] = incoming_msg[0];
        command_arg[1] = incoming_msg[1];
        command_arg[0] = incoming_msg[2];
        Serial.print("Argument received: " + String(command_arg[2]) + String(command_arg[1]) + String(command_arg[0]) + "\n");
        argParse = false; //deflag argParse so we can read the next msg
      }
    }
  }

  //Command execution
  switch (command) { //Continually operate on last received command
    case 'L': //Control Left Motor
      if (!argParse) {
        //only set motor speed when we get the desired speed
        leftm -> setSpeed(atoi(command_arg));
      }
      break;
      
    case 'R': //Control Right Motor
      if (!argParse) {
        //only set motor speed when we get the desired speed
        rightm -> setSpeed(atoi(command_arg));
      }
      break;
      
    case 'S': //Stop
      drive(0, 0);
      break;
      
    case 'F': //Follow Line
      followLine();
      break;

    case '<': //Turn left until you find a line
      findLineLeft();
      break;

    case '>': //Turn right until you find a line
      findLineRight();
      break;
      
    default:
      //change nothing
      if (unknownCommandFlag) {
        Serial.print("Unknown command received: " + String(command) + "\n");
      }
      unknownCommandFlag = false;
      break;
  }
}

void findLineLeft() {
  left_sensor = analogRead(LEFT_SENSOR_PIN);

  if (!foundLine) {
    if (left_sensor < LEFT_SENSOR_THRESH) {
      drive(-20, 20);
    } else {
      foundLine = true;
    }
  } else {
    if (left_sensor > LEFT_SENSOR_THRESH) {
      drive(-20, 20);
    } else {
      drive(0, 0);
    }
  }
}

void findLineRight() {
  right_sensor = analogRead(RIGHT_SENSOR_PIN);

  if (!foundLine) {
    if (right_sensor < RIGHT_SENSOR_PIN) {
      drive(-20, 20);
    } else {
      foundLine = true;
    }
  } else {
    if (right_sensor > RIGHT_SENSOR_PIN) {
      drive(-20, 20);
    } else {
      drive(0, 0);
    }
  }
}

void followLine() {
  left_sensor = analogRead(LEFT_SENSOR_PIN);
  right_sensor = analogRead(RIGHT_SENSOR_PIN);

  if (left_sensor > LEFT_SENSOR_THRESH) {
    //Left sensor is over line
    //Swerve left until left sensor is not over line
    drive(40, 50); //Slow down left wheel to swerve left
  } else if (right_sensor > RIGHT_SENSOR_THRESH) {
    //Right sensor is over line
    //Swerve right until right sensor is not over line
    drive(50, 40); //Slow down right wheel to swerve right
  } else {
    //No sensors are over line
    //Drive straight
    drive(50, 50);
  }
}

void drive(int l, int r) { // helper function to drive motors
  leftm -> setSpeed(l);
  rightm -> setSpeed(r);
}

void resetDriveParams() {
  foundLine = false;
}

void accumulateEncoders() {
  accumulateEncoder_Left_A();
  accumulateEncoder_Left_B();
  accumulateEncoder_Right_A();
  accumulateEncoder_Right_B();
}

void accumulateEncoder_Left_A() {
  //Trigger on edge of signal (rising or falling)
  if (la_state != la_prevstate) {
    left_encoder = left_encoder + 1;
    la_prevstate = la_state;
  }
}

void accumulateEncoder_Left_B() {
  //Trigger on edge of signal (rising or falling)
  if (lb_state != lb_prevstate) {
    left_encoder = left_encoder + 1;
    lb_prevstate = lb_state;
  }
}

void accumulateEncoder_Right_A() {
  //Trigger on edge of signal (rising or falling)
  if (ra_state != ra_prevstate) {
    right_encoder = right_encoder + 1;
    ra_prevstate = ra_state;
  }
}

void accumulateEncoder_Right_B() {
  //Trigger on edge of signal (rising or falling)
  if (rb_state != rb_prevstate) {
    right_encoder = right_encoder + 1;
    rb_prevstate = rb_state;
  }
}

