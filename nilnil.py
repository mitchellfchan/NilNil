import RPi.GPIO as GPIO

from subprocess import Popen
from subprocess import check_output
import os
import sys
import psutil
import time

waitTime = 1.75
kickTime = 1
holdTime = 1

ballButton = 12
pushScrn = 21
pushBall = 25


idle = ("/home/pi/Idlecompress.mp4")
kick = ("/home/pi/Kickcompress.mp4")


GPIO.setmode(GPIO.BCM)


GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

currentButtonState = True
oldButtonState = True
numPresses = 0
idlePID = 0
initRun = False



def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
    listOfProcessObjects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return listOfProcessObjects;


while True:

  # global oldButtonState
  # global currentButtonState
  # global numPresses
  # global initRun

  playerPIDs = findProcessIdByName("omxplayer")
  resetButton = GPIO.input(23)

  if(playerPIDs):
    
    numPIDs = len(playerPIDs)
    print("We found this many players: " + str(numPIDs))
    print(playerPIDs[numPIDs-1]["pid"])
    # global idlePID
    idlePID = playerPIDs[numPIDs-1]["pid"] 

    if (numPIDs <=2):
      print("We've got 2 or fewer omxplayer processes")
      # global idlePID
      idlePID = playerPIDs[numPIDs-1]["pid"] 
      print("The last idle player we know about was PID " + str(idlePID))

  else:
    print("No player! Let's start one.")
    if not initRun:
      omxc = Popen("omxplayer --layer 1 --loop Idlecompress.mp4", shell=True)
      initRun = True
  
  
  oldButtonState = currentButtonState
  currentButtonState = GPIO.input(12)

  if(currentButtonState and not oldButtonState):
    print("PUSHED!")
    print(str(currentButtonState))
    numPresses+=1
    omxc2 = Popen("omxplayer --layer 2 Kickcompress.mp4", shell=True)
    time.sleep(waitTime)
    GPIO.output(21, 1)
    
    
    # os.system('kill ' + str(idlePID))
    # os.system('omxplayer dahliaKick1080.mp4')
    print("waiting a second")
    time.sleep(kickTime)
    GPIO.output(25, 1)
    print("waiting 3 seconds")
    time.sleep(holdTime)
    GPIO.output(21,0)
    GPIO.output(25,0)
    # omxc = Popen(['omxplayer', '--loop', idle])
    print("OK, we done.")
    

  
  if (resetButton):
    os.system('killall omxplayer.bin')
    time.sleep(2)
    os.system('shutdown -r now')
  
  if(True):
    print("We keep truckin! Button has been pushed " + str(numPresses) + " times")

      