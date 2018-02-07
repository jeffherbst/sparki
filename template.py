import pygame
import sys
import time
from RobotLib.Math import *
import math
import argparse
from RobotLib.FrontEnd import *
from RobotLib.IO import *
import numpy as np


class MyFrontEnd(FrontEnd):
    """ Custom sub-class of FrontEnd
        You can write custom sub-routines here to respond to UI events and calculate updates
    """

    #global variables because i couldn't make a class work.
    global velocity
    global omega
    global theta
    global sparkiCenter
    global sonarReadingS
    velocity = 0
    omega = 0
    theta = 0
    sparkiCenter = vec(128.,128.)
    sonarReadingS = vec(5.,0.)

    def __init__(self,width,height,sparki):
        FrontEnd.__init__(self,width,height)
        self.sparki = sparki 
                    
    def mouseup(self,x,y,button):
        # x,y is position of mouse click
        print('mouse clicked at %d, %d'%(x,y))

    def keydown(self,key):
        # see https://www.pygame.org/docs/ref/key.html for pygame key names, such as pygame.K_UP 
        global velocity
        global omega
        #set velocities based on pressing of keys. 90% forward and back. small angular velocity to test
        if ( pygame.key.get_pressed()[pygame.K_UP] != 0 ):    
            print('up pressed')
            velocity = 3.42
        if ( pygame.key.get_pressed()[pygame.K_DOWN] != 0):
            print('down pressed')
            velocity = -3.42
        if ( pygame.key.get_pressed()[pygame.K_LEFT] != 0):
            print('left pressed')
            omega += .2
        if ( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
            print('right pressed')
            omega += -.2

    def keyup(self,key):
        # see https://www.pygame.org/docs/ref/key.html for pygame key names, such as pygame.K_UP
        print('key released')
        global velocity
        global omega
        #set velocities to 0 on release of keys
        if (key == 273):
            velocity = 0
        if (key == 274):
            velocity = 0
        if (key == 275):
            omega = 0
        if (key == 276):
            omega = 0
        
    def draw(self,surface):
        # draw robot here
        #
        # draw a rectangle for the robot
        # draw a red line from the sonar to the object it is pinging
        #
        # use pygame.draw.line(surface,color,point1,point2) to draw a line
        # for example, pygame.draw.line(surface,(0,0,0),(0,0),(10,10))
        # draws a black line from (0,0) to (10,0)
 
       
        #circumference of wheel = 15.71 cm
        #4096 steps per revolution.
        #1 step =.0038 cm /step
        #max speed is 1000 steps per sec or 3.8 cm per sec
        #90% is 900 or 3.42 cm per sec
        
        #find all 6 points in child frame
        #set transformation matrix based on center and orientation
        
        
        
        global sparkiCenter
        global sonarReadingS
        #use this for sonar if it won't work
        #sonarPoint = (sparkiCenter[0]+math.cos(theta)*25.,sparkiCenter[1]+math.sin(theta)*25.) 
        #pygame.draw.line(surface,(0,0,0),sparkiCenter,sonarPoint)
        
        #transform matrixes
        transRtoM = transform(sparkiCenter[0],sparkiCenter[1],theta)
        transStoR = transform(2.5,0.,0.)
        transMtoR = invert(transRtoM)
        transRtoS = invert(transStoR)

        #points of sparki in robot frame
        frontRightR = vec(5.,-4.5) 
        frontLeftR = vec(5.,4.5)
        backRightR = vec(-5.,-4.5)
        backLeftR = vec(-5.,4.5)
        centerR = vec(0.,0.)
        sonarR = vec(2.5,0.) 
        
        #calculate all points of the robot and sonar using transform matrixes
        centerM = mul(transRtoM,frontRightR)
        frontRightM = mul(transRtoM,frontRightR)
        frontLeftM = mul(transRtoM,frontLeftR)
        backRightM = mul(transRtoM,backRightR)
        backLeftM = mul(transRtoM,backLeftR)
        sonarM = mul(transRtoM,sonarR)
        sonarReadingM = mul(transRtoM,mul(transStoR,sonarReadingS))
        
        #draw robot and sonar, red for front of robot
        pygame.draw.line(surface,(255,0,0),frontRightM,frontLeftM)
        pygame.draw.line(surface,(0,255,0),frontRightM,backRightM)
        pygame.draw.line(surface,(0,255,0),backRightM,backLeftM)
        pygame.draw.line(surface,(0,255,0),frontLeftM,backLeftM)
        pygame.draw.line(surface,(255,0,0),sonarM,sonarReadingM)

    def update(self,time_delta):
        # this function is called approximately every 50 milliseconds
        # time_delta is the time in seconds since the last update() call
        # 
        # you can send an update command to sparki here
        # use self.sparki.send_command(left_speed,left_dir,right_speed,right_dir,servo,gripper_status)
        # see docs in RobotLib/IO.py for more information, #0 for forward. #0 for strop gripper_status
        #
        # if you send a message more than once per millisecond, the message will be dropped
        # so, only call send_command() once per update()
        #
        # you can also calculate dead reckoning (forward kinematics) and other things like PID control here
        global theta
        global omega
        global velocity
        global sparkiCenter
        global sonarReadingS

        #integrating over time
        theta += omega * time_delta

        #calculate center given known velocity and direction
        sparkiCenter[0] += velocity * math.cos(theta) * time_delta
        sparkiCenter[1] += velocity * math.sin(theta) * time_delta

        #specific wheel velocity
        velocityRight = velocity + (omega * (8.51/2))
        velocityLeft = velocity - (omega * (8.52/2))
        
        #reverse flags and logic
        rightReverse = 0
        leftReverse = 0

        if velocityRight < 0:
            rightReverse = 1
            velocityRight = abs(velocityRight)

        if velocityLeft < 0:
            leftReverse = 1
            velocityLeft = abs(velocityLeft)

        #debugging output
        #print(sparkiCenter[0],sparkiCenter[1],theta,omega,velocity)
       
        #this will show a point if there is no reading, should show a line when readings come in
        sonarReadingS[0] = self.sparki.dist

        #tell sparki how to move
        self.sparki.send_command(int(velocityRight),rightReverse,int(velocityLeft),rightReverse,0,0)


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
