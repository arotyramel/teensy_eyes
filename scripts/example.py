#!/usr/bin/python

import rospy

from teensy_eyes.msg import Eyes 
if __name__ == "__main__":
    rospy.init_node("teensy_eye_example")
    msg = Eyes()
    msg.blinkL = False
    msg.blinkR = False
    msg.blink = False
    pub = rospy.Publisher("eyes",Eyes,queue_size=1)
    rospy.sleep(1)
    msg.auto_eyes = True
    msg.auto_blink = True
    print "autonomous eyes"
    pub.publish(msg)
    rospy.sleep(3)
      
      
    msg.auto_eyes = False
    msg.x = 0
    msg.y = 0
    print "eyes to 0/0"
    pub.publish(msg)
    rospy.sleep(2)
      
    msg.x = 1023
    print "eyes to 1023/0"
    pub.publish(msg)
    rospy.sleep(2)
      
    msg.y = 1023
    print "eyes to 1023/1023"
    pub.publish(msg)
    rospy.sleep(2)
      
    msg.x = 0
    msg.y = 1023
    print "eyes to 0/1023"
    pub.publish(msg)
    rospy.sleep(2)
      
    msg.x = 512
    msg.y = 512
    print "eyes to center 512/512"
    pub.publish(msg)
    rospy.sleep(1)
      
    print "iris from 0 to 1023"
    for i in range(0,1023,10):
        msg.iris = i
        pub.publish(msg)
        rospy.sleep(0.1)
    msg.iris = 300
    print "iris to 300"    
    pub.publish(msg)
    rospy.sleep(1)
     
    msg.auto_eyes = False
    msg.auto_blink = False
    msg.x = 512
    msg.y = 512
    pub.publish(msg)
    print "blinking 3 times"
    msg.blink = True
    for i in range(3):
        pub.publish(msg)
        rospy.sleep(1)
    rospy.sleep(1)
    
    msg.blink = False
    msg.blinkL = False
    msg.blinkR = True
    print "blinking R"
    for i in range(3):
        print "blinkR"
        pub.publish(msg)
        rospy.sleep(2)
    rospy.sleep(1)
    
    msg.blinkR = False
    msg.blinkL = True
    print "blinking L"
    for i in range(3):
        pub.publish(msg)
        rospy.sleep(2)    
    