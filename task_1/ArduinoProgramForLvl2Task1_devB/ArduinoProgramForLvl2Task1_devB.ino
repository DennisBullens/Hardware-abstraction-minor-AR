// Include libraries and messages
#include <ros.h>
#include <hardware_abstraction/control_msgs.h>  
#include <Servo.h>

// Define constants
#define LED_PIN 11

// Make instance of servo
Servo servo1;

/*
  To device B the servo and a LED are attached.
  The servo should rotate to the target angle corresponding to readings from the potentiometer of devic a.
  Minimum voltage is maximum angle, maximum voltage is minimum angle
  the LED should decrease the intensity proportionally with increasing the potentiometer of device a
  
*/

ros::NodeHandle nh; // Initialize the node handler with nh as name
hardware_abstraction::control_msgs control_msg; // Initialize the control_msgs of hardware_abstraction to the name of control_msg

void messageCallBack(const hardware_abstraction::control_msgs &control_msg){
  int angle = 180 - control_msg.angle; // The angle of the servo should be the inverse of the angle of device a
  servo1.write(angle); // Rotate servo
  int ledValue = 255 - control_msg.ledVal; // The LED value should be the inverse of the LED of device a
  analogWrite(LED_PIN, ledValue); // Change intensity of LED
}

ros::Subscriber<hardware_abstraction::control_msgs> subB("DeviceB", messageCallBack); // Initialize subscriber to topic DeviceB

void setup() {
  nh.initNode(); // Initialize node
  servo1.attach(9); // Attach the servo to pin 9
  nh.subscribe(subB); // Subscribe to topic Device B
  pinMode(LED_PIN, OUTPUT); // LED is output
}

void loop() {
  nh.spinOnce();
  delay(1);
}

