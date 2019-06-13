#! /usr/bin/env python

import rospy
import actionlib
from hardware_abstraction.msg import task3DevA,actionDevAAction, actionDevAGoal 

potMeterValue = 500
class callBacks():
    def __init__(self):
        pass

    def arduinoCallback(self, data):
        #print "arduino callback ClientA"
        #print "callback arduino a data: " + str(data)
        global potMeterValue
        potMeterValue = data.currentPotValue

def actionClient():
    global potMeterValue
    #print potMeterValue
    client = actionlib.SimpleActionClient("task3_dev_a", actionDevAAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    
    # Creates a goal to send to the action server.
    goal = actionDevAGoal()
    goal.setPoint = potMeterValue
    
    # Sends the goal to the action server.
    client.send_goal(goal)#, feedback_cb=callbacks.feedback_cb)

    # Waits for the server to finish performing the action.
    client.wait_for_result()
    #print ("[result] State: %d"%(client.get_state()))
    #print ("[Result] Status: %s"%(client.get_goal_status_text()))
    actionResult = client.get_result()

    #print "result " + str(actionResult)
    if actionResult == True:
        print "_____________________________**************************************___________________________________***********************************_____________________________***************************"
        arduinoMessages.ledValue = True
        pub.publish(arduinoMessages)

    # Prints out the result of executing the action
    return actionResult

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('ClientDevA')
        r = rospy.Rate(4)
        arduinoMessages = task3DevA()
        callbacks = callBacks()
        pub = rospy.Publisher("deviceA", task3DevA, queue_size=10)
        sub = rospy.Subscriber("deviceA", task3DevA, callbacks.arduinoCallback)
        
        #result = actionClient()
        while not rospy.is_shutdown():
            result  = actionClient()
            r.sleep()

    except rospy.ROSInterruptException:
        pass
