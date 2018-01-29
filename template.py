#test commit

import pygame
import sys
import time
import math
import argparse
from RobotLib.FrontEnd import *
from RobotLib.IO import *
import numpy as np

class MyFrontEnd(FrontEnd):
    """ Custom sub-class of FrontEnd
        You can write custom sub-routines here to respond to UI events and calculate updates
    """

    def __init__(self,width,height,sparki):
        FrontEnd.__init__(self,width,height)
        self.sparki = sparki

    def mouseup(self,x,y,button):
        # x,y is position of mouse click
        print('mouse clicked at %d, %d'%(x,y))

    def keydown(self,key):
        # see https://www.pygame.org/docs/ref/key.html for pygame key names, such as pygame.K_UP 
        if ( pygame.key.get_pressed()[pygame.K_UP] != 0 ):    
            print('up pressed')
        if ( pygame.key.get_pressed()[pygame.K_DOWN] != 0):
            print('down pressed')
        if ( pygame.key.get_pressed()[pygame.K_LEFT] != 0):
            print('left pressed')
        if ( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
            print('right pressed')

    def keyup(self,key):
        # see https://www.pygame.org/docs/ref/key.html for pygame key names, such as pygame.K_UP
        print('key released')
        
        
    def draw(self,surface):
        # draw robot here
        #
        # draw a rectangle for the robot
        # draw a red line from the sonar to the object it is pinging
        #
        # use pygame.draw.line(surface,color,point1,point2) to draw a line
        # for example, pygame.draw.line(surface,(0,0,0),(0,0),(10,10))
        # draws a black line from (0,0) to (10,0)
	
	#calculate the point for the center, based on robot location
	#form the box based on orientation,
	#reset 0,0 to be the middle
	#draw the 4 lines
	#draw the head line
      	pygame.draw.line(surface,(255,0,0),(0,0),(10,10))

    def update(self,time_delta):
        # this function is called approximately every 50 milliseconds
        # time_delta is the time in seconds since the last update() call
        # 
        # you can send an update command to sparki here
        # use self.sparki.send_command(left_speed,left_dir,right_speed,right_dir,servo,gripper_status)
        # see docs in RobotLib/IO.py for more information
        #
        # if you send a message more than once per millisecond, the message will be dropped
        # so, only call send_command() once per update()
        #
        # you can also calculate dead reckoning (forward kinematics) and other things like PID control here
        self.sparki.send_command()

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Template')
    parser.add_argument('--width', type=int, default=256, help='map width')
    parser.add_argument('--height', type=int, default=256, help='map height')
    parser.add_argument('--port', type=str, default='', help='port for serial communication')
    args = parser.parse_args()
    
    with SparkiSerial(port=args.port) as sparki:
        # make frontend
        frontend = MyFrontEnd(args.width,args.height,sparki)
    
        # run frontend
        frontend.run()

if __name__ == '__main__':
    main()
