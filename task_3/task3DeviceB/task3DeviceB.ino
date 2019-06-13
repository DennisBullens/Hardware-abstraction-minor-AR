//#define USE_USBCON

#include <ros.h>
#include <hardware_abstraction/task3DevB.h>
#include <Servo.h>

#define LED_PIN 11

Servo servo;
int desiredServoValue;
int currentAngle;
bool maximumReached;
bool ledValue;

bool receivedCallBack = true;

ros::NodeHandle nh;
hardware_abstraction::task3DevB msg;
ros::Publisher pubB("DeviceB", &msg);

void messageCallBack(const hardware_abstraction::task3DevB &msg) {
  desiredServoValue = msg.setPoint;
  currentAngle = msg.currentValue;
  maximumReached = msg.maximumReached;
  ledValue = msg.ledVal;
  servo.write(desiredServoValue);
  digitalWrite(LED_PIN, ledValue);
  receivedCallBack = true;
}

ros::Subscriber <hardware_abstraction::task3DevB> subB("DeviceB", messageCallBack);

void setup() {
  nh.initNode();
  Serial.begin(9600);
  nh.advertise(pubB);
  pinMode(LED_PIN, OUTPUT);
  servo.attach(9);
  servo.write(0);
  nh.subscribe(subB);
  nh.loginfo("Setup Complete");
}

void loop() {
  if (receivedCallBack == true) {
    currentAngle = servo.read();
    msg.currentValue = currentAngle;
    if (currentAngle >= 179)
    {
      msg.maximumReached = true;
      delay(1000);
    }
    else {
      msg.maximumReached = false;
    }
    pubB.publish(&msg);
    receivedCallBack = false;

  }

  nh.spinOnce();
  delay(250);
}

















