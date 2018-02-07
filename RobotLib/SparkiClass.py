import numpy as np
import math
import pygame
from .Math import *

class SparkiClass(object):

    def __init__(self,width=256,height=256,theta=0):
        self.velocity = 0.
        self.omega = 0.
        self.theta = 0.

        self._sonarReadingS = vec(25.,0.)

        self._leftVelocity = 0.
        self._rightVelocity = 0.
        self.leftWheelDir = 0
        self.rightWheelDir = 0

        self._backRightR = vec(-5.,-4.5)
        self._backLeftR = vec(-5.,4.5)
        self._frontRightR = vec(5.,-4.5)
        self._frontLeftR = vec(5,4.5)
        self._headLocationR = vec(2.5,0.)
        self._centerR = vec(0.,0.)
    
        self._centerM = vec(width/2.,height/2.)

        self._transRtoM = transform(width/2.,height/2.,self.theta)
        self._transStoR = transform(2.5,0.,0.)
        self._transMtoR = invert(self._transRtoM) 
        self._transRtoM = invert(self._transStoR)
    
    #getters in map frame
    def backRightM(self):
        return mul(self._transRtoM,self._backRightR)
        
    def backLeftM(self):
        return mul(self._transRtoM,self._backLeftR)

    def frontRightM(self):
        return mul(self._transRtoM,self._frontRightR)

    def frontLeftM(self):
        return mul(self._transRtoM,self._frontLeftR)

    def centerM(self):
        return mul(self._transRtoM,self._centerR)

    def headLocationM(self):
        return mul(self._transRtoM,self._headLocationR)

    def sonarReadingM(self):
        return mul(self._transRtoM,mul(self._transStoR,self._sonarReadingS))

    def sonarDistance(self,distance):
        self._sonarReadingS[0] = distance

        #UPDATE THIS TO GET SPARKI TO MOVE
    def getCommandLeft(self):
        if self._leftVelocity > 3.00:
            return int(90)
        else:
            return 0
        #expand for other %
        #make sure they return ints, will not send to sparki if not an int.
        #should be a % of 100 depending on the speed. 

        #UPDATE THIS TO GET SPARKI TO MOVE
    def getCommandRight(self):
        if self._rightVelocity > 3.00:
            return int(90)
        else: 
            return 0
        #expand for other %


    #update functions
    def updateTransforms(self):
        self._transRtoM = transform(self._centerM[0],self._centerM[1],self.theta)
        self._transMtoR = invert(self._transRtoM)

    def updateRightVelocity(self):
        self._rightVelocity = self.velocity + (self.omega * (8.52/2) )
        if self._rightVelocity > 0 :
            self._rightVelocity = abs(self._rightVelocity)
            self.rightWheelDir = 1

    def updateLeftVelocity(self):
        self._leftVelocity = self.velocity - (self.omega * (8.52/2) )
        if self._leftVelocity > 0 :
            self._leftVelocity = abs(self._leftVelocity)
            self.leftWheelDir = 1

    def updateCenter(self,time_delta):
        self.theta += self.omega * time_delta
        self._centerM[0] += self.velocity * math.cos(self.theta) * time_delta
        self._centerM[1] += self.velocity * math.sin(self.theta) * time_delta
        self.updateRightVelocity()
        self.updateLeftVelocity()
        self.updateTransforms()
        
    def testPrint(self):
        print ("it worked") 

    #call draw to draw your robot including sonar
    def draw(self,surface):
        pygame.draw.line(surface,(0,0,255),self.frontRightM(),self.frontLeftM())
        pygame.draw.line(surface,(0,255,0),self.frontRightM(),self.backRightM())
        pygame.draw.line(surface,(0,255,0),self.frontLeftM(),self.backLeftM())
        pygame.draw.line(surface,(0,255,0),self.backLeftM(),self.backRightM())
        pygame.draw.line(surface,(255,0,0),self.headLocationM(),self.sonarReadingM())
        
