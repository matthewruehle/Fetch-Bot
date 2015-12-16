#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>
#define FORWARD 1
#define BACKWARD 2
#define RELEASE 3

Servo manip_servo;
Servo claw_servo;
Adafruit_MotorShield MS;
Adafruit_DCMotor *leftm, *rightm;
const byte LEFT_MOTOR_PORT = 1;
const byte RIGHT_MOTOR_PORT = 2;
const int LEFT_SENSOR_PIN = A5, RIGHT_SENSOR_PIN = A3;
const int LEFT_SENSOR_THRESH = 970;
const int RIGHT_SENSOR_THRESH = 900;
const int LEFT_HALL_A_PIN = 1, LEFT_HALL_B_PIN = 2;
const int RIGHT_HALL_A_PIN = 3, RIGHT_HALL_B_PIN = 4;
const int MANIPULATOR_SERVO_PIN = 9;
const int CLAW_SERVO_PIN = 10;
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
int cs = 90;

void setup() {
  Serial.begin(9600);
  MS = Adafruit_MotorShield();
  MS.begin();
  leftm = MS.getMotor(LEFT_MOTOR_PORT);
  rightm = MS.getMotor(RIGHT_MOTOR_PORT);
  leftm -> setSpeed(0);
  rightm -> setSpeed(0);
  leftm -> run(FORWARD);
  rightm -> run(BACKWARD);
  manip_servo.attach(MANIPULATOR_SERVO_PIN);
  claw_servo.attach(CLAW_SERVO_PIN);
  manip_servo.write(98); //actually the front servo that opens and closes claw
  claw_servo.write(90); //actually the back servo that extends and retracts claw
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
      //claw_servo.write(90);
      manip_servo.write(98);
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

    case 'G': //Grab
      grab();
      break;

    case 'D': //Drop
      drop();
      break;
    
    case 'B': //Back
      backup();
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
  //Serial.print("Left Sensor: " + String(left_sensor) +  "\n");

  if (!foundLine) {
    if (left_sensor < LEFT_SENSOR_THRESH) {
      drive(-15, 15);
    } else {
      foundLine = true;
    }
  } else {
    if (left_sensor > LEFT_SENSOR_THRESH) {
      drive(-15, 15);
    } else {
      delay(500);
      drive(0, 0);
    }
  }
}

void findLineRight() {
  right_sensor = analogRead(RIGHT_SENSOR_PIN);
  //Serial.print("Right Sensor: " + String(right_sensor) +  "\n");

  if (!foundLine) {
    if (right_sensor < RIGHT_SENSOR_THRESH) {
      drive(15, -15);
    } else {
      foundLine = true;
    }
  } else {
    if (right_sensor > RIGHT_SENSOR_THRESH) {
      drive(15, -15);
    } else {
      delay(500);
      drive(0, 0);
    }
  }
}

void grab() {
  drive(0, 0);
  manip_servo.write(90);
  delay(500);
  claw_servo.write(0);
  delay(500);
  manip_servo.write(120);
  delay(800);
  //claw_servo.write(90);
  claw_servo.write(180);
  delay(1200);
  manip_servo.write(100);
  command = 'S';
}

void drop() {
  drive(0, 0);
  claw_servo.write(10);
  manip_servo.write(100);
  delay(500);
  manip_servo.write(80);
  delay(500);
  claw_servo.write(90);
  delay(1000);
  manip_servo.write(100);
  delay(500);
  //claw_servo.write(90);
  manip_servo.write(98);
  command = 'S';
}

void backup() {
  left_sensor = analogRead(LEFT_SENSOR_PIN);
  right_sensor = analogRead(RIGHT_SENSOR_PIN);
  //Serial.print("Left Sensor: " + String(left_sensor) +  "\n");
  //Serial.print("Right Sensor: " + String(right_sensor) +  "\n");
  
  if (left_sensor > LEFT_SENSOR_THRESH) {
    //Left sensor is over line
    //Swerve left until left sensor is not over line
    drive(-10, -30); //Slow down left wheel to swerve left
  } else if (right_sensor > RIGHT_SENSOR_THRESH) {
    //Right sensor is over line
    //Swerve right until right sensor is not over line
    drive(-30, -10); //Slow down right wheel to swerve right
  } else {
    //No sensors are over line
    //Drive straight
    drive(-30, -30);
  }
}


void followLine() {
  left_sensor = analogRead(LEFT_SENSOR_PIN);
  right_sensor = analogRead(RIGHT_SENSOR_PIN);
  //Serial.print("Left Sensor: " + String(left_sensor) +  "\n");
  //Serial.print("Right Sensor: " + String(right_sensor) +  "\n");
  
  if (left_sensor > LEFT_SENSOR_THRESH) {
    //Left sensor is over line
    //Swerve left until left sensor is not over line
    drive(10, 30); //Slow down left wheel to swerve left
  } else if (right_sensor > RIGHT_SENSOR_THRESH) {
    //Right sensor is over line
    //Swerve right until right sensor is not over line
    drive(30, 10); //Slow down right wheel to swerve right
  } else {
    //No sensors are over line
    //Drive straight
    drive(30, 30);
  }
}

void drive(int l, int r) { // helper function to drive motors
  if (l<0) {
    leftm -> run(BACKWARD);
    leftm -> setSpeed(-1*l);
  } else {
    leftm -> run(FORWARD);
    leftm -> setSpeed(l);
  }

  if (r<0) {
    rightm -> run(FORWARD);
    rightm -> setSpeed(-1*r);
  } else {
    rightm -> run(BACKWARD);
    rightm -> setSpeed(r);
  }
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
