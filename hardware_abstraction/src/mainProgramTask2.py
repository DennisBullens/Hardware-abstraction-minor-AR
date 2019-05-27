#!/usr/bin/env python
import rospy
from hardware_abstraction.srv import control_srvs_dev_a, control_srvs_dev_aResponse
from hardware_abstraction.srv import control_srvs_dev_b, control_srvs_dev_bResponse

# TWEE CALLBACKS 1 VOOR DEV A EN 1 VOOR DEVICE B MET IEDER EEN APARTE MESSAGE
class callbacks():
    def __init__(self):
        self.resultA = control_srvs_dev_aResponse()
        self.lastStateLedA = False
        self.lastStateLedB = False
        self.lastServoVal = 0
        self.potVal = 0
    
    def handle_values_dev_a(self, request):
        self.resultA = control_srvs_dev_aResponse()
        self.potVal = request.potentioMeterValue
        #print "Value of potentiometer: %s" %(self.potVal)    
        if self.potVal > 920:
            self.resultA.ledDevA = True
            self.lastStateLedA = True

        elif self.potVal < 920 and self.potVal > 103:
            self.resultA.ledDevA = self.lastStateLedA
        
        elif self.potVal < 103:
            self.resultA.ledDevA = False
            self.lastStateLedA = False
        
        #print self.resultA
        #print self.lastStateLedA
        #print "\n*****"
        return self.resultA

    def handle_values_dev_b(self, request):
        if request.getValues == True:
            self.resultB = control_srvs_dev_bResponse()
 
            if self.potVal > 920:
                self.resultB.ledValB = False
                self.lastStateLedB = False
                self.resultB.servoVal = 180
                self.lastServoVal = 180

            elif self.potVal < 920 and self.potVal > 103:
                self.resultB.ledValB = self.lastStateLedB
                self.resultB.servoVal = self.lastServoVal
            
            elif self.potVal < 103:
                self.resultB.ledValB = True
                self.lastStateLedB = True
                self.resultB.servoVal = 0
                self.lastServoVal = 0
            
            #print self.resultB
            #print self.lastStateLedB
            #print "\n*****"
        else:
            self.resultB.ledValB = False
            self.resultB.servoVal = 0.0
        return self.resultB

if __name__ == "__main__":
    try:
        rospy.init_node("mainProgramTask2")
        callBacks = callbacks()
        serviceDevA = rospy.Service("/control_srv_dev_a", control_srvs_dev_a, callBacks.handle_values_dev_a)
        serviceDevB = rospy.Service("/control_srv_dev_b", control_srvs_dev_b, callBacks.handle_values_dev_b)
        #rospy.wait_for_service("/control_srv")
        print "INITIALIZING DONE"
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
