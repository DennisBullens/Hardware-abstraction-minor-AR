#include <ros.h>
#include <std_msgs/Bool.h>
#include <hardware_abstraction/control_srvs_dev_a.h>

#define LED_PIN 11

ros::NodeHandle nh;
using hardware_abstraction::control_srvs_dev_a;

ros::ServiceClient<control_srvs_dev_a::Request, control_srvs_dev_a::Response> clientDevA("/control_srv_dev_a");

void setup() {
  nh.getHardware()->setBaud(9600);
  nh.initNode();
  nh.serviceClient(clientDevA);
  while (!nh.connected()) nh.spinOnce();
  pinMode(LED_PIN, OUTPUT);
  nh.loginfo("Setup complete");
}

void loop() {
  control_srvs_dev_a::Request req;
  control_srvs_dev_a::Response res;
  int potVal = analogRead(A0);
  req.potentioMeterValue = potVal;
  clientDevA.call(req, res);
  nh.spinOnce();
  bool ledVal = res.ledDevA;
  digitalWrite (LED_PIN, ledVal);
  nh.spinOnce();
  delay(500);
}
