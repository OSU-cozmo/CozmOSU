# there is probably a better way to do this but this allows importing from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from CozmOSU import *

def main(cozmo):
   cozmo.driveForward(10, 10)

MyRobot = Robot()
MyRobot.start(main)