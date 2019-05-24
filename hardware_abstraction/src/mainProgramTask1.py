#!/usr/bin/env python
import rospy
from hardware_abstraction.msg import control_msgs

potentioValue = 0
ledVal = 0

def callbackDevA(dataDevA):
    global potentioValue, ledVal
    potentioValue = dataDevA.angle
    ledVal = dataDevA.ledVal
    #print "RECEIVED DATA FROM DEVICE A"

if __name__ == "__main__":
    try:
        subDeviceA = rospy.Subscriber("DeviceA", control_msgs, callbackDevA)
        pubDeviceB = rospy.Publisher("DeviceB", control_msgs, queue_size=10)
        rospy.init_node("main", anonymous=False)
        control_msg = control_msgs()
        rate = rospy.Rate(5) #5 hz
        while not rospy.is_shutdown():
            #global potentioValue, ledVal
            control_msg.angle = potentioValue
            control_msg.ledVal = ledVal
            print control_msg
            pubDeviceB.publish(control_msg)
            rate.sleep()

    except rospy.ROSInterruptException:
        pass