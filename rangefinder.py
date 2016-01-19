import time
import RPi.GPIO as GPIO
import serial
import datetime
from subprocess import call
import setproctitle

setproctitle.setproctitle("rangefinder")

GPIO.setmode(GPIO.BCM)  #setup for PWM
GPIO.setup(20, GPIO.OUT)   #Define pin 20 as output, for PWM modulation of vibration motor
p = GPIO.PWM(20, 25)  #channel = 20 , frequency = 25 hz
p.start(5) #5% duty cycle to start. should immediately change as the rangefinder reads
maxbotix = serial.Serial("/dev/ttyAMA0",baudrate=9600,timeout=5) #Open a serial input to recieve from the maxbotix ultrasonic sensor
time.sleep(0.2)#This sleep interval is required to let the serial input open completely before it is read for the first time. Without this pause, random crashes on startup occur
timesinceflip = 0
vibration = 1
while 1:
    maxbotix.flushInput() #clear buffer to get fresh values if you don't do this, you won't get responsive readings
    currdistance = maxbotix.readline(10) #Take ten characters worth of the serial buffer that accumulates since the flush
    stripstart = currdistance.find("R") #Look for the character "R", find out where it occurs in the string first
    stripend = stripstart + 5 #Define the end of the character length we need to grab the numeric info
    currdistance = currdistance[stripstart+1:stripend] #strip out the numeric info
    currmm = float(currdistance) #Now make the info a number instead of a string
    print currmm #comment this out after debugging
    if (currmm > 299 and currmm < 600):
            p.ChangeFrequency(5)
            p.ChangeDutyCycle(50)
    elif (currmm > 600 and currmm < 1000):
            p.ChangeFrequency(10)
            p.ChangeDutyCycle(50)
    elif (currmm > 1000 and currmm < 2000):
            p.ChangeFrequency(20)
            p.ChangeDutyCycle(50)
    elif (currmm > 2000 and currmm < 3000):
            p.ChangeFrequency(40)
            p.ChangeDutyCycle(50)
    elif (currmm > 3000 and currmm < 4000):
            p.ChangeFrequency(80)
            p.ChangeDutyCycle(50)
    elif currmm > 4000:
            p.ChangeFrequency(160)
            p.ChangeDutyCycle(50)
    else:
	    p.ChangeFrequency(320)
	    p.ChangeDutyCycle(50)
    time.sleep(0.3)
p.ChangeDutyCycle(0)