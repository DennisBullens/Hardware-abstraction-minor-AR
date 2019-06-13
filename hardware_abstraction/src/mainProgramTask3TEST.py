#! /usr/bin/env python
import rospy
import actionlib
from hardware_abstraction.msg import actionDevAFeedback, actionDevAAction, actionDevAResult
from hardware_abstraction.msg import actionDevBAction, actionDevBGoal

desiredAngle = 0
currentAngle = 180
currentAnglePrecent = 100

class Functions():
    def __init__(self):
        pass
    
    def mapVal(self, x, in_min, in_max, out_min, out_max):

        return (x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min

class server():
    _feedback = actionDevAFeedback()
    _result = actionDevAResult()
    
    def __init__(self):
        self.server = actionlib.SimpleActionServer("TEST", actionDevAAction, execute_cb=self.serverHandler, auto_start=False)
        self.server.start()

    def serverHandler (self, goal):
        global desiredAngle, currentAngle, currentAnglePrecent

        success = True
        desiredAngle = goal.setPoint

        while currentAngle != desiredAngle:
            '''if self.server.is_preempt_requested():
                rospy.loginfo("preempt requested")
                self.server.set_preempted()
                success = False
                break'''
            self._feedback.currentValue = currentAngle
            self.server.publish_feedback(self._feedback)
            print "in main server feedback: " + str(self._feedback)
            rate.sleep()        

        if success:
            self._result.maximumReached = True
            rospy.loginfo("succeeded")
            self.server.set_succeeded(self._result)

class client():
    def __init__(self):
        pass

    def clientHandler(self):
        global desiredAngle, currentAngle, currentAnglePrecent
        print "CLIENT"
        self.client = actionlib.SimpleActionClient("TEST_Main_Client", actionDevBAction)
        self.client.wait_for_server()
        self.goal = actionDevBGoal(desiredAngleServo=desiredAngle)
        self.client.send_goal(self.goal, feedback_cb=self.feedback)
        self.client.wait_for_result()
        return self.client.get_result()
    
    def feedback(self, data):
        print "feedback data: " + str(data)
        global currentAnglePrecent, currentAngle
        currentAnglePrecent = data.precentServoAngle
        currentAngle = int(functionsClass.mapVal(currentAnglePrecent, 0, 100, 0, 180))

if __name__ == "__main__":
    try:
        rospy.init_node("test", anonymous=False)
        rate = rospy.Rate(4)
        functionsClass = Functions()
        clientClass = client()
        serverClass = server()
        print "WHILE"
        while not rospy.is_shutdown():
            result = clientClass.clientHandler()
            rate.sleep()
            print result
        #rospy.spin()

    except rospy.ROSInterruptException:
        pass