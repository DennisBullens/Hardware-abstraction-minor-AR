// Include libraries and messages
#include <ros.h>
#include <hardware_abstraction/control_msgs.h>

// Define constants 
#define LED_PIN 11

/*
  On device A a potentiometer and a LED are attached. 
 The LED should increase the intensity proportionally to the potentiometer.
 The servo motor on device B should go to the same angle of the potentiometer.
 */

ros::NodeHandle nh; // Initialize node handler with nh as name
hardware_abstraction::control_msgs control_msg; // Initialize the control_msgs of hardware_abstraction to the name of control_msg
ros::Publisher deviceA("DeviceA", &control_msg); // Initialize the publisher named DeviceA

void setup() {
  nh.initNode(); // Initialize node
  nh.advertise(deviceA); // Advertise the publishing node
  pinMode(LED_PIN, OUTPUT); // LED is output
}

void loop() {
  int anglePot = analogRead(A0); // Read current value of potentiometer 0 - 1023
  int angle = map(anglePot, 0, 1023, 0, 180); // Remap potentiometer to a maximum angle of 180 degrees
  int ledValue = map(anglePot, 0, 1023, 0, 255); // Remap the maximum values from potentio to 255 for maximum LED value
  
  analogWrite(LED_PIN, ledValue); // Write the value of the remapped value to the led
  control_msg.angle = angle; // Write angle to the control messages
  control_msg.ledVal = ledValue; // Write the led value to the control messages
  deviceA.publish(&control_msg); // Publish values
  nh.spinOnce();
  delay(1);
}

