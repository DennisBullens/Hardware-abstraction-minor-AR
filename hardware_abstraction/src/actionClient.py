#! /usr/bin/env python
import rospy
import actionlib
from hardware_abstraction.msg import actionDevAAction, actionDevAGoal
from hardware_abstraction.msg import task3DevA

currentAngle = -1

def arduino_cb(data):
    global currentAngle
    currentAngle = data.currentPotValue

def actionClient():
    client = actionlib.SimpleActionClient("TEST", actionDevAAction)
    client.wait_for_server()
    goal = actionDevAGoal(setPoint=60)
    client.send_goal(goal)
    client.wait_for_result()
    return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node("TEST_client")
        pub = rospy.Publisher("task3DevA", task3DevA, queue_size=10)
        sub = rospy.Subscriber("task3DevA", task3DevA, arduino_cb)
        while not rospy.is_shutdown():
            result = actionClient()
            print result
    except rospy.ROSInterruptException:
        pass
