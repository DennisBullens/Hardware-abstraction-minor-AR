#! /usr/bin/env python
import rospy
import actionlib
from hardware_abstraction.msg import actionDevAFeedback, actionDevAAction, actionDevAResult
from hardware_abstraction.msg import actionDevBAction, actionDevBGoal

'''
Dev A is a client since it sends data
Device B is a server since it has to execute stuff
ROS program is a server for device A and a client for device B

Task = first servo and pot meter are in minimum position. After this the action servers are setup.
Action goal is to follow the settings of the potentiometer by the servo and provide feedback regarding 
the progress.
Goal is finished as maximum angle is reached
If goal is not reached within 10 seonds cancel the goal
'''

desiredServoAngle = 500
maximumReached = False

class Functions():
    def __init__(self):
        pass

    def mapVal(self, x, in_min, in_max, out_min, out_max):
        return int((x-in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

class DeviceA ():
    _feedback = actionDevAFeedback()
    _result = actionDevAResult()
    
    def __init__(self):
        self._as = actionlib.SimpleActionServer("task3_dev_a", actionDevAAction, execute_cb=self.execute_cb, auto_start=False)
        self._as.start()
        
    def execute_cb(self, goal):
        global desiredServoAngle, maximumReached

        if self._as.is_preempt_requested():
            rospy.logwarn("preempt")
            self._as.set_preempted()

        desiredServoAngle = goal.setPoint
        desiredServoAngle = functions.mapVal(desiredServoAngle, 0, 1023, 0, 180)

        self._feedback.reading = True
        self._as.publish_feedback(self._feedback)

        self._result.maximumReached = maximumReached

        if True:
            #print "DeviceA Succes"
            print "/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"
            self._as.set_succeeded(self._result)


class DeviceB():
    def __init__(self):
        #print "class Device B Client initialized"
        pass

    def actionClient(self):
        global desiredServoAngle
        #print desiredServoAngle
        
        client = actionlib.SimpleActionClient('task3_dev_b', actionDevBAction)

        # Waits until the action server has started up and started
        # listening for goals.
        client.wait_for_server()

        # Creates a goal to send to the action server.
        goal = actionDevBGoal()
        goal.desiredAngleServo = desiredServoAngle

        # Sends the goal to the action server.
        client.send_goal(goal)

        # Waits for the server to finish performing the action.
        client.wait_for_result()
        actionResult = client.get_result()
        #print "result: " + str(actionResult)
        print actionResult
        if actionResult == True:
            print "*********************************************************************************************************************************************************************************"

        # Prints out the result of executing the action
        return actionResult

if __name__ == '__main__':
    try:
        rospy.init_node('main_program')
        r = rospy.Rate(4)
        functions = Functions()
        server = DeviceA()
        result = DeviceB()
        while not rospy.is_shutdown():
            result.actionClient()
            r.sleep()
        #rospy.spin()
    except rospy.ROSInterruptException:
        pass
