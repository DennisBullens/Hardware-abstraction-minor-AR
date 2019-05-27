#include <ros.h>
#include <std_msgs/Bool.h>
#include <hardware_abstraction/control_srvs_dev_b.h>
#include <Servo.h>

#define LED_PIN 11
Servo servo1;

ros::NodeHandle nh;
using hardware_abstraction::control_srvs_dev_b;

std_msgs::Bool Bool;

ros::ServiceClient<control_srvs_dev_b::Request, control_srvs_dev_b::Response> clientDevB("/control_srv_dev_b");

void setup() {
  nh.getHardware()->setBaud(9600);
  nh.initNode();
  nh.serviceClient(clientDevB);
  servo1.attach(9);
  servo1.write(0);
  while (!nh.connected()) nh.spinOnce();
  pinMode(LED_PIN, OUTPUT);
  nh.loginfo("Setup complete");
}

void loop() {
  control_srvs_dev_b::Request req;
  control_srvs_dev_b::Response res;
  req.getValues = true;
  clientDevB.call(req, res);
  nh.spinOnce();
  int servoVallue = res.servoVal;
  bool ledVal = res.ledValB;
  digitalWrite(LED_PIN, ledVal);
  servo1.write(servoVallue);


  nh.spinOnce();
  delay(500);
}





