#!/usr/bin/python
import serial
import time
from post_threading import Post
from sets import Set
HIGH = 1
LOW = 0
# digitalWrite 0
# digitalRead 1
# analogWrite 2
# analogRead 3
import os
class Bridge():
    def __init__(self):
        self.post = Post(self)
        self.conn_down = True
        self.feedback = Set()
        self.initConnection()
#         self.send("")
        
    def openSerialPort(self,i):
        try:
            self.ser = serial.Serial('/dev/ttyUSB'+str(i), 9600)
            self.ser.flushInput()
            self.ser.flush()
            self.conn_down = False
            return True
        except Exception, e:
            if "[Errno 2]" in str(e):
                return False
            else:
                print "Problem accessing the device",e
                exit(1)
            
        
    def initConnection(self):
        
        for i in xrange(4):
            if self.openSerialPort(i):
                break
            
        if self.conn_down:
            print "could not establish connection"
            exit(1)
            return
        self.post.readFeedback()
        
        
    def readFeedback(self):
        while not self.conn_down:
            res = self.ser.readline()
            
            if res[0] == ">":
                
                continue
            res = tuple([x.rstrip() for x in res.split(";")][:-1])
#             print "res",res
            if not res == ('unknown command',) and not res == ('0', '0', '0'):
#                 print "adding ",res[0]
                self.feedback.add(res)
        
    def waitFeedback(self,msg):
#         print "feedback data", self.feedback
        msg = tuple(msg.split(";")[:-1])
        found = False
        answer=None
        for feedback in self.feedback:
            if msg==feedback[:len(msg)]:
                found = True
                answer= feedback
                break
        if not found:
            return None
        print "found answer"
        self.feedback.remove(answer)
        return answer
        
    def send(self, data):
#         print "{0:b}".format(data).zfill(8)
        try:
            if len(data)>0:
#                 print "send", data
                self.ser.write(">"+data)
            self.ser.write(chr(0))
            self.ser.flush()
        except:
            print "lost connection"
            self.conn_down = True
            time.sleep(1)
            self.initConnection()
        time.sleep(0.05)
        
        if len(data)>0:
            res = self.waitFeedback(data)
            if res is None: 
#                 print "resending",data
#                 return [42,42,42]
                return self.send(data)
                
                
            else:
                return res
        
    def digitalWrite(self,pin,value):
        msg = ";0;"+str(pin)+";"+str(value)+";"
        return self.send(msg)
        
    def digitalRead(self,pin):
        msg = ";1;"+str(pin)+";"
        return self.send(msg)
        
        
    def analogWrite(self,pin,value):
        self.send(";2;"+str(pin)+";"+str(value)+";")
        
    def analogRead(self,pin):
        self.send(";3;"+str(pin)+";")

if __name__ == "__main__":
    b = Bridge()
#     print "write",b.digitalWrite(13,HIGH);
#     print "read", b.digitalRead(13)[2];
#     time.sleep(1)
    while True:
        int(b.digitalRead(13)[2])
        break
#         if int(b.digitalRead(13)[2]):
#             b.digitalWrite(13,0)
#         else:
#             b.digitalWrite(13,1)

#         print "---------------"
#         print "---------------"
        time.sleep(1)
        
    