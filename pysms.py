import serial
import time
import sys

class Message:
    
    def __init__(self,recipient,message="No message."):
        self.recipient=recipient
        self.message=message
        print "init done.."
        
    def setRecipient(self,number):
        self.recipient=number
        
    def setContent(self,content):
        self.message=content
        
    def connect(self):
        self.ser=serial.Serial('/dev/ttyUSB0',38400, timeout=1)
        time.sleep(1)
        print "connected.."

    def sendMessage(self):
        self.ser.write('ATZ\r')
        time.sleep(1)
        self.ser.write('AT+CMGF=1\r')
        time.sleep(1)
        self.ser.write('''AT+CMGS="''' + self.recipient + '''"\r''')
        time.sleep(1)
        self.ser.write(self.message + "\r")
        time.sleep(1)
        self.ser.write(chr(26))
        line=self.ser.readline()
        print line
        time.sleep(1)
        print "sent message to "+self.recipient
       
    def readMessage(self):
        self.ser.write('AT+CMGF=1\r')
        time.sleep(1)
        line=self.ser.read(50)
        time.sleep(1)
        self.ser.write('AT+CMGL="ALL"\r')
        time.sleep(1)
        line=self.ser.read(1000)
        print line

    def disconnectPhone(self):
        self.ser.close()

    def check(self):
        print "checking..."
        self.ser.write('ATZ\r')
        time.sleep(1)
        self.ser.write('AT+CGMI\r')
        time.sleep(1)
        line=self.ser.readline()
        print line
        print "done"

    def status(self,stat):
        print "check status..."
        self.ser.write('AT+'+stat+'\r')
        time.sleep(1)
        line=self.ser.read(50)
        time.sleep(1)
        print "done"
        

sms=Message()

if len(sys.argv)>1:
    number=sys.argv[1]
    message=sys.argv[2]
    if(len(number)==10):        
        sms.setRecipient(number)
        sms.setContent(message)
    
sms.connect()
#sms.sendMessage()
#sms.status('CREG?')
sms.readMessage()
sms.disconnectPhone()

