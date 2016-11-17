#!/usr/bin/python
import serial
import time
import rospy
from TeensyEyes.msg import Eyes
import os
class Bridge():
    def __init__(self):
        self.connected = False
        self.feedback = Set()
        self.initConnection()
        self.cmd = Eyes()
        self.cmd.iris=515
        self.cmd.x=512
        self.cmd.y=512
        self.cmd.auto_eyes = True
        self.sub = rospy.Subscriber("eyes", Eyes, self.callback, queue_size=1)
        
    def openSerialPort(self,i):
        try:
            self.ser = serial.Serial('/dev/ttyUSB'+str(i), 115200)
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
            self.ser.write(self.cmd.iris+"\r")
        if msg.x != self.cmd.x:
            self.cmd.x = msg.x
            self.ser.write(self.cmd.x+"\r")
        if msg.y != self.cmd.y:
            self.cmd.y = msg.y
            self.ser.write(self.cmd.y+"\r")    
        if not msg.auto_eyes is self.cmd.eyes:
            self.cmd.auto_eyes = msg.auto_eyes
            self.ser.write(int(self.cmd.auto_eyes)+"\r")
        self.ser.flush()
            

if __name__ == "__main__":
    rospy.init_node("teensy_eyes")
    b = Bridge()
    rospy.spin()