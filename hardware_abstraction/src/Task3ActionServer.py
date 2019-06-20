#! /usr/bin/env python
#Device B is the server since it has to receive a value and execute some movements

# Import libraries and messages
import rospy
import actionlib
from hardware_abstraction.msg import actionTask3Feedback, actionTask3Action, actionTask3Result
from hardware_abstraction.msg import task3DevB

# Create global variables
desiredAngle = "global"
currentAngle = 0
maximumReached = False
arduinoSetPoint = 0
ledValueArduino = False

def arduino_cb(data):
    # Callback for receiving arduino messages from device B
    global currentAngle, maximumReached, arduinoSetPoint, ledValueArduino
    arduinoSetPoint = data.setPoint
    currentAngle = data.currentValue
    maximumReached = data.maximumReached
    ledValueArduino = data.ledVal

class Functions():
    def __init__(self):
        pass

    def mapVal(self, x, in_min, in_max, out_min, out_max):
        # Function to remap values 
        return (x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min

class server():
    # Initialize object variables
    _feedback = actionTask3Feedback()
    _result = actionTask3Result()

    def __init__(self):
        # Create action server
        self._as = actionlib.SimpleActionServer("Task_3", actionTask3Action, execute_cb=self.serverHandler, auto_start = False)
        # Start the action server
        self._as.start() 
      
    def serverHandler(self, goal):
        global desiredAngle, currentAngle, maximumReached, ledValueArduino
        # Amount of Hz the program should run
        rate = rospy.Rate(4)
        success = True
        # What is the desired angle?
        desiredAngle = goal.setPoint

        angle = 0
        if currentAngle != desiredAngle: # If the current angle is not equal to the desired execute the next part
            for angle in range(0, desiredAngle):
                # for loop to increase the angle for the arduino till desired angle is reached
                arduinomsgs.setPoint = angle
                arduinomsgs.currentValue = currentAngle
                arduinomsgs.maximumReached = maximumReached
                arduinomsgs.ledVal = ledValueArduino
                pub.publish(arduinomsgs)
                rospy.sleep(0.01)

                print angle
                # Create the feedback variable and publish it
                self._feedback.currentValuePrecent = round(float((currentAngle/180.0)*100))
                self._as.publish_feedback(self._feedback)

            rate.sleep()

        if success:
            arduinomsgs.ledVal = not arduinomsgs.ledVal # Change value of LED DOES NOT WORK YET
            pub.publish(arduinomsgs)
            self._result.maximumReached = True
            rospy.loginfo("succeeded")
            self._as.set_succeeded(self._result)
        

if __name__ == '__main__':
    try:
        # Create node
        rospy.init_node('Server_task_3')
        # Initialize the messages used in arduino
        arduinomsgs = task3DevB()
        pub = rospy.Publisher("DeviceB", task3DevB, queue_size=10)
        sub = rospy.Subscriber("DeviceB", task3DevB, arduino_cb)
        
        # Initialize classes
        functionsClass = Functions()
        serverClass = server()
        print "SERVER"
        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass
