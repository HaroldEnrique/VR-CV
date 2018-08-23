# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 20:14:04 2018

@author: ASUS
"""

import random
from Box2D.b2 import (polygonShape, world)
from backends.opencv_draw import OpencvDrawFuncs
import cv2

##Max W=32
##Max H=24

class shapes:
    
    maxWP=640
    maxHP=480
    maxWM=32
    maxHM=24
    
    def __init__(self, world, shapeType, NumAn): 
        self.world=world
        self.body = self.world.CreateDynamicBody(position=(0,0))
        self.w = random.randint(0,32);
        self.h = random.randint(20,24);
        self.NumAn = NumAn
        if NumAn==3:
            self.h = random.randint(0,4);
        self.r = round(random.uniform(0.1,1),2)
        # Add the box to the box2d world
        self.body.position=(self.w,self.h)
        self.shapeT = shapeType
        
        if shapeType==0:
            self.circle = self.body.CreateCircleFixture(radius=self.r, density=1, friction=0.3)        
        elif shapeType==1:
            self.box = self.body.CreatePolygonFixture(box=(self.r, self.r), density=1, friction=0.3)
        elif shapeType==2:
            self.triangle =  self.body.CreatePolygonFixture(vertices=[(0,0), (self.r+1,0), (0,self.r+1)])
        elif shapeType==3:
            self.triangle =  self.body.CreatePolygonFixture(vertices=[(0,0), (self.r,-0.5*(self.r)), (0,self.r),(self.r,1.5*(self.r)),(1.5*(self.r),0.5*(self.r))])
        if NumAn==5:
            self.circle = self.body.CreateCircleFixture(radius=2, density=1, friction=0.3)
        
    def killBody(self):
        self.world.DestroyBody(self.body)
        
    def done(self):
        # Let's find the screen position of the particle
        pos = self.body.position
        # Is it off the bottom of the screen?
        if (pos[1] < 0 or pos[0] > 32 or pos[0] < 0):
            self.killBody()
            return True
        else:
            return False
        
        if (self.NumAn==3):
            if(pos[1] < 0 or pos[0] > 32 or pos[0] > 24):
                self.killBody()
                return True

class CircleEsp:
    
    maxWP=640
    maxHP=480
    maxWM=32
    maxHM=24
    
    def __init__(self, world): 
        self.world=world
        self.body = self.world.CreateStaticBody(position=(0,0))
        self.w = 0;
        self.h = 0;
        self.r = 0.1
        # Add the box to the box2d world
        self.body.position=(self.w,self.h)
        self.circle = self.body.CreateCircleFixture(radius=self.r, density=1, friction=0.3)

    def mov(self, newPos):
        x=newPos[0]*self.maxWM/self.maxWP
        y=newPos[1]*self.maxHM/self.maxHP
        self.body.position=(y,x)
        
    def killBody(self):
        self.world.DestroyBody(self.body)
        