#! /usr/bin/env python
import rospy
import actionlib
from hardware_abstraction.msg import actionDevBFeedback, actionDevBAction, actionDevBResult

desiredAngle = 0
currentAngle = 180

class Functions():
    def __init__(self):
        pass
    
    def mapVal(self, x, in_min, in_max, out_min, out_max):

        return (x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min

class server():
    _feedback = actionDevBFeedback()
    _result = actionDevBResult()

    def __init__(self):
        self._as = actionlib.SimpleActionServer("TEST_Main_Client", actionDevBAction, execute_cb=self.serverHandler, auto_start = False)
        self._as.start()
      
    def serverHandler(self, goal):
        print "HANDLER"
        print goal
        global desiredAngle, currentAngle
        rate = rospy.Rate(4)
        success = True
        angle = goal.desiredAngleServo
        print "angle = " + str(angle)
        
        while currentAngle != desiredAngle:
        #for value in xrange(angle):
            if self._as.is_preempt_requested():
                rospy.loginfo("Preempt requested")
                self._as.set_preempted()
                success = False
                break
            self._feedback.precentServoAngle =  functionsClass.mapVal(currentAngle, 0, 180, 0, 100) #(value / 180) * 100
            print "in seperate server feedback: " + str(self._feedback.precentServoAngle)
            self._as.publish_feedback(self._feedback)
            currentAngle += 1
            rate.sleep()

        if success:
            self._result.maximumReached = True
            rospy.loginfo("succeeded device B")
            self._as.set_succeeded(self._result)

if __name__ == '__main__':
    rospy.init_node('TEST_Server')
    functionsClass = Functions()
    serverClass = server()

    print "SERVER"
    rospy.spin()