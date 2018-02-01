from .Math import *
import numpy as np


#my sparki class for finding his location


class SparkiGPS:

    def __init__(self, width = 256, height = 256):
        self.x = width/2
        self.y = height/2
        self.theta = 0
        self.sparkiToMap = transform(self.x,self.y,self.theta)
        self.mapToSparki = invert(self.sparkiToMap)
        self.backRight = (0,0)
        self.backLeft = (0,0)
        self.frontRight = (0,0)
        self.frontLeft = (0,0)
        


    def moveSparki(self, forwardV, angV):
        self.x = self.x + forwardV
        self.theta = self.theta + angV
        self.calcCorners()        

#or can do in one calc corners
    def backRightCalc(self):
        self.backRight = (self.x,self.y)

    def backLeftCalc(self):
        self.backLeft = (self.x,self.y)
 
    def frontLeftCalc(self): 
        self.frontLeft = (10*np.cos(self.theta) + self.x, 10*np.sin(self.theta) + self.y)
        
    def frontRightCalc(self):
        self.frontRight = (10*np.cos(self.theta) + self.x, 10*np.sin(self.theta) + self.y)

    def calcCorners(self):
        self.backRightCalc()
        self.backLeftCalc()
        self.frontRightCalc()
        self.frontLeftCalc()        
