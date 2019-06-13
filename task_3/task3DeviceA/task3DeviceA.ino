#include <ros.h>
#include <hardware_abstraction/task3DevA.h>
#define LED_PIN 11

bool receivedCallBack = true;

ros::NodeHandle nh;
hardware_abstraction::task3DevA msg;
ros::Publisher pubA("DeviceA", &msg);

void messageCallBack(const hardware_abstraction::task3DevA &msg) {
  digitalWrite (LED_PIN, msg.ledValue);
  receivedCallBack = true;
}

ros::Subscriber <hardware_abstraction::task3DevA> subA("DeviceA", messageCallBack);

void setup() {
  Serial.begin(9600);
  nh.initNode();
  nh.advertise(pubA);
  pinMode (LED_PIN, OUTPUT);
  nh.subscribe(subA);

  nh.loginfo("Setup Complete");
}

void loop() {
  int currentAngle;
  
  if (receivedCallBack == true) {
    currentAngle = analogRead(A0);
    msg.currentPotValue = currentAngle;
    pubA.publish(&msg);
    receivedCallBack = false;
  }
  
  nh.spinOnce();
  delay (250);
}







