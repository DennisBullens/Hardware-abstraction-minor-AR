#! /usr/bin/env python
#Device A is the client since it provides the setpoint

# Import libraries and messages
import rospy
import actionlib
from hardware_abstraction.msg import actionTask3Action, actionTask3Goal
from hardware_abstraction.msg import task3DevA

# Create global variables
desiredAngle = 90
currentAngle = 180
currentpotAngle = 500 # value between 0 and 1023
maximumReached = False

class Functions():
    def __init__(self):
        pass
    
    def mapVal(self, x, in_min, in_max, out_min, out_max):
        # Function to remap values
        return (x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min

def arduino_cb(data):
    # Callback for arduino messages
    global desiredAngle, currentpotAngle, maximumReached, currentAngle
    currentpotAngle = data.currentPotValue
    desiredAngle = functionClass.mapVal(currentpotAngle, 0, 1023, 0, 180)

def actionClient(desAngle):
    # Create action client
    actionClient = actionlib.SimpleActionClient("Task_3", actionTask3Action)
    # Wait for action server to be reached
    actionClient.wait_for_server()

    # Create the goals for server
    goal = actionTask3Goal()
    goal.setPoint = desAngle

    # Send goal
    actionClient.send_goal(goal)

    # Wait for result with a maximum time of 10 seconds
    actionClient.wait_for_result(timeout=rospy.Duration(10))

    return actionClient.get_result()

if __name__ == "__main__":
    try:
        # Initialize node
        rospy.init_node("client_task_3")

        # Create instances of classes
        functionClass = Functions()
        arduinomsgs = task3DevA()

        # subscribe and publish to the arduino
        pub = rospy.Publisher("DeviceA", task3DevA, queue_size=10)
        pub.publish(arduinomsgs)
        sub = rospy.Subscriber("DeviceA", task3DevA, arduino_cb)
        
        while not rospy.is_shutdown():
            #global desiredAngle
            #angle = desiredAngle

            # Which angle should it go.
            # If you want to use the potmeter value comment line 69 and
            # uncomment lines 63 and 64 
            angle = input("Desired Angle: ")
            if angle > 180:
                angle = 180
            if angle < 0:
                angle = 0
            
            # Wait for ENTER to execute
            raw_input("press ENTER to start")
            # Create instance of client with the desired angle as parameter
            result = actionClient(angle)
            #print result

            if result != None:
                # If the client has a result and it is true, than succeeded
                if result.maximumReached == True:
                    rospy.loginfo("maximum Reached")
                    arduinomsgs.ledValue = not arduinomsgs.ledValue
                    pub.publish(arduinomsgs)
                else:
                    rospy.loginfo("Time out")
    
    except rospy.ROSInterruptException:
        pass