#!/usr/bin/python
import serial
import time
import rospy
from teensy_eyes.msg import Eyes
import os
class Bridge():
    def __init__(self):
        self.connected = False
        self.initConnection()
        self.cmd = Eyes()
        self.cmd.iris=515
        self.cmd.x=512
        self.cmd.y=512
        self.cmd.auto_eyes = True
        self.sub = rospy.Subscriber("eyes", Eyes, self.callback, queue_size=1)
        
    def openSerialPort(self,i):
        try:
            self.ser = serial.Serial('/dev/ttyACM'+str(i), 115200)
            return True
        except Exception as  exc:
            print(exc)
            return False
            
        
    def initConnection(self):
        for i in xrange(4):
            if self.openSerialPort(i):
                self.connected = True
                break
        
    def callback(self,msg):
        if msg.iris != self.cmd.iris:
            self.cmd.iris = msg.iris
            self.ser.write("iris"+str(self.cmd.iris)+"\r")
            self.ser.flush()
        if msg.x != self.cmd.x:
            self.cmd.x = msg.x
            self.ser.write("joyx"+str(self.cmd.x)+"\r")
            self.ser.flush()
        if msg.y != self.cmd.y:
            self.cmd.y = msg.y
            self.ser.write("joyy"+str(self.cmd.y)+"\r")
            self.ser.flush()    
        if not msg.auto_eyes is self.cmd.auto_eyes:
            self.cmd.auto_eyes = msg.auto_eyes
            if self.cmd.auto_eyes:
                self.ser.write("auto_eyes\r\n")
            else:
                self.ser.write("joy_eyes\r\n")
            self.ser.flush()
            

if __name__ == "__main__":
    rospy.init_node("teensy_eyes")
    b = Bridge()
    rospy.spin()