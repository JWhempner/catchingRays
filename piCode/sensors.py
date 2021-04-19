import sys
import datetime
import time


def getTime():
    return datetime.datetime.now()


def getPressure():
    # read pressure
    # calculate altitude
    # return pressure/altitude


def getTemp():
    # read temp
    # return temp


def getVoltage():
    # read somehow from piplate (from digital in probably)
    # return value


def getSensorReading():
    # basically same as voltage
    # read from digital
    # return signal (probably just 0)




def sendData():
    # collect all readings from sensors
    # do magic with rfd
    # send power to pins to send or something



def writeToFile():
    # collect all readings
    # write to csv file


def cutDown():
    # BEYBLADE TIME

#Oscilloscope code basics
import piplates.DAQC2plate as DAQC2

DAQC2.startOSC(0)           #enable oscope
DAQC2.setOSCchannel(0,1,0)  #use channel 1
 
## Set up trigger:
##    Use channel 1
##    Normal trigger mode (don't collect data until trigger conditions are met)
##    Trigger on rising edge of waveform
##    Trigger at 0.0 volts
DAQC2.setOSCtrigger(0,1,'normal','rising',2048)
 
## setup sample rate for 10,000 samples per second
DAQC2.setOSCsweep(0,6)
DAQC2.intEnable(0)          #enable interrupts
DAQC2.runOSC(0)             #start oscope
 
## Wait for sweep to complete by monitoring Ocsope interrupt flag
dataReady=0
while(dataReady==0):
    if(DAQC2.GPIO.input(22)==0):
        dataReady=1
        DAQC2.getINTflags(0) #clear interrupt flags
 
DAQC2.getOSCtraces(0)
 
### print out first 1000 converted values and not the conversion from A2D integer data to measured voltage
for i in range(1000):
    print((DAQC2.trace1[i]-2048)*12.0/2048)          
 
DAQC2.stopOSC(0)             #turn off oscilloscope mode




# interrupts for request data, cutdown, sensor input
# timed read, toAltitude
# user power off, user power on

# structure everything as interrupt based sys


#GPIO Interrupt code standards and basics
import RPi.GPIO as GPIO

#2 setup modes:
#BOARD: Pin numbering
#BCM: GPIO numbering
#GPIO4 == PIN 7
#BCM      BOARD
GPIO.setmode(GPIO.BOARD)

#Sets Pin 7 as an input. Pulled up to stop false signals
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    #Causes Program to halt until this interrupt is detected
    GPIO.wait_for_edge(7, GPIO.FALLING)
except KeyboardInterrupt:
    GPIO.cleanup()      #Cleans up GPIO on CTRL+C exit
GPIO.cleanup()          #Cleans up GPIO on normal exit

#Sets pin 11 as an input, pulled down.
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#define callback fundtion to be executed when interrupt is detected
def my_callback(channel):
    #insert code to be executed here ex:
    print "pin 11 interrupt detected"

#Actual line added to create event when rising edge is
#detected on pin 11 to trigger callback function regardless
#of what else the program is doing. Will still execute if
#sitting in a GPIO.wait_for_edge() function.
#Bounce time line added so singals recieved within 300
#milliseconds of eachother will be ignored
GPIO.add_event_detect(11, GPIO.RISING, callback=my_callback, bouncetime=300)

GPIO.cleanup()      #Good practice to do at end of all code that uses GPIO interrupts

#If multiple interrupts threaded with each other is desired
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_callback1(channel):
    #code for pin 7 interrupt
    
def my_callback2(channel):
    #code for pin 11 interrupt

#GPIO.FALLING can be .FALLING .RISING or .BOTH
GPIO.add_event_detect(7, GPIO.FALLING, callback=my_callback1, bouncetime=300)

GPIO.add_event_detect(11, GPIO.FALLING, callback=my_callback2, bouncetime=300)

GPIO.cleanup()

#To remove an event detection use the following
#which would remove the pin 7 interrupt
GPIO.remove_event_detect(7)

