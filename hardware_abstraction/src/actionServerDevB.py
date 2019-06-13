#! /usr/bin/env python
import roslib
roslib.load_manifest("hardware_abstraction")
import rospy
import actionlib
from hardware_abstraction.msg import actionDevBAction, task3DevB, actionDevBFeedback, actionDevBGoal, actionDevBResult

desiredServoAngle = 90
maximumReached = False
precentServoAngle = 0

def arduinoCallback(data):
    global maximumReached, precentServoAngle
    #print data
    #maximumReached = data.maximumReached
    precentServoAngle = float((data.currentValue / 180)*100)

class ActionServer(object):
    _feedback = actionDevBFeedback()
    _result = actionDevBResult()

    def __init__(self):
        self._as = actionlib.SimpleActionServer("task3_dev_b", actionDevBAction, execute_cb=self.execute_cb, auto_start=False)
        self._as.start()
      
    def execute_cb(self, goal):
        success = True
        #print "executecallback device B"
        global desiredServoAngle, maximumReached, precentServoAngle
        #print precentServoAngle
        
        if self._as.is_preempt_requested():
            rospy.logwarn("preempt")
            self._as.set_preempted()

        desiredServoAngle = goal.desiredAngleServo
        arduinoMessages.setPoint = desiredServoAngle
        pub.publish(arduinoMessages)
        self._feedback.precentServoAngle = precentServoAngle
        self._as.publish_feedback(self._feedback)

        if precentServoAngle == 100:
            maximumReached = True
        else:
            maximumReached = False
        
        self._result.maximumReached = maximumReached

        if (maximumReached):
            #print "DeviceB Succes"
            print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
            self._as.set_succeeded(self._result)

if __name__ == '__main__':
    try:
        rospy.init_node('ServerDevB')
        arduinoMessages = task3DevB()
        #print "node initialized"
        server = ActionServer()

        pub = rospy.Publisher("deviceB", task3DevB, queue_size=10)
        sub = rospy.Subscriber("deviceB", task3DevB, arduinoCallback)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass