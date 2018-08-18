# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 22:07:14 2018

@author: ASUS
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 21:35:26 2018

@author: ASUS
"""

import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

import Box2D  # The main library
# Box2D.b2 maps Box2D.b2Vec2 to vec2 (and so on)
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
import random
from backends.opencv_draw import OpencvDrawFuncs
from Circle import shapes, CircleEsp
from BackgroundExtractionFunction import Main
import os
from socket import *
import threading
import os


"""
Declaracion de la camara (Tomar video)
"""
heightW=480#720#480#
widthW=640#1280#640#

# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
config.enable_stream(rs.stream.color, widthW, heightW, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print( "Depth Scale is: " , depth_scale)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 2 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
Pygame and Box2D
"""
# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 20.0  # pixels per meter
TARGET_FPS = 10
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

# --- pybox2d world setup ---
# Create the world
world = world(gravity=(0, -10), doSleep=True)

"""
Animations
"""
colors = {
    staticBody: (136, 128, 93, 255),
    dynamicBody: (32, 20, 29, 255),
    3: (123,115,80, 255),
    4: (226,203,165),
}

colors = {
        1:{
            staticBody: (136, 128, 93, 255), #Contorno
            dynamicBody: (32, 20, 29, 255), #Circulo
            3: (123,115,80, 255), #Triangulo
            4: (226,203,165), #Cuadrado
            5: (130,12,9), #pentagono
            6: (136,128,93), #Persona
            7: (180,166,123),}, #Fondo
        2:{
            staticBody: (1,1,1), #Contorno
            dynamicBody: (242,60,0), #Circulo
            3: (146,217,219), #Triangulo
            4: (54,75,106), #Cuadrado
            5: (100,100,100), #pentagono
            6: (1,1,1), #Persona
            7: (254,254,254),}, #Fondo
        3:{
            staticBody: (237,57,33), #Contorno
            dynamicBody: (251,189,0, 255), #Circulo
            3: (121,45,121), #Triangulo
            4: (237,138,41), #Cuadrado
            5: (23,157,133), #Pentagono
            6: (237,57,33), #Persona
            7: (254,254,254),}, #Fondo
        5:{
            staticBody: (237,57,33), #Contorno
            dynamicBody: (251,189,0, 255), #Circulo
            3: (121,45,121), #Triangulo
            4: (237,138,41), #Cuadrado
            5: (23,157,133), #Pentagono
            6: (237,57,33), #Persona
            7: (254,254,254),}, #Fondo
}

# Let's play with extending the shape classes to draw for us.

circles=[]
person=[]
numFrame=0

person=[]
NumAn=1

"""
Color shapes functions
"""

def my_draw_polygon(polygon, body, fixture):
    global NumAn
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[NumAn][len(polygon.vertices)], vertices)
polygonShape.draw = my_draw_polygon

def my_draw_circle(circle, body, fixture):
    
#    colors = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[NumAn][body.type], [int(
        x) for x in position], int(circle.radius * PPM))
    # Note: Python 3.x will enforce that pygame get the integers it requests,
    #       and it will not convert from float.
circleShape.draw = my_draw_circle

"""
Contours extraction Function
"""
def Ncoordenadas(img):
    edge = cv2.Canny(img, 175, 175)
    _, contours,hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#   
    a=np.asarray(np.where(edge==255))
    a=np.asarray(a)
    
    return a
"""
Cvimage to Pygame image
"""
def cvimage_to_pygame(frame):
    """Convert cvimage into a pygame image"""
#    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = cv2.flip(frame, 0)
    frame = pygame.surfarray.make_surface(frame)
    return frame
# --- main game loop ---

"""
Aplying Color animation function
"""
def ColorsAnimation(binImag):
    global NumAn
    
    imgFondoR = binImag[:,:,0]
    imgFondoG = binImag[:,:,1]
    imgFondoB = binImag[:,:,2]
    
    imgFondoR[np.where(imgFondoR==255)]=colors[NumAn][6][0]
    imgFondoG[np.where(imgFondoG==255)]=colors[NumAn][6][1]
    imgFondoB[np.where(imgFondoB==255)]=colors[NumAn][6][2]
    imgFondoR[np.where(imgFondoR==0)]=colors[NumAn][7][0]
    imgFondoG[np.where(imgFondoG==0)]=colors[NumAn][7][1]
    imgFondoB[np.where(imgFondoB==0)]=colors[NumAn][7][2]
    
    imgFondo = np.dstack((imgFondoR,imgFondoG,imgFondoB))
    img = cvimage_to_pygame(imgFondo)
    
    return img

"""
Server function (Comunication with Leap-motion)
"""
def server():
    
    global NumAn
    
    port = 13000
    buf = 1024
    host = ""
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    UDPSock.bind(addr)
    print("Waiting to receive messages...")
    data=b'0'
    
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        print ("Received message: " + data.decode())
        
        if data==b'1':
            print("Hey, you pressed the key, '0'!")
            print(NumAn)
            NumAn+=1 #Changing animation
            
            if NumAn==3:
                world.gravity=(0,10)
            elif NumAn>3:
                world.gravity=(0,-10)
            if NumAn>5:
                world.gravity=(0,-10)
                NumAn=1
                
        elif data==b'2':
            global pipeline
            salida = os.popen('netstat -ano|findstr 13000').read()
            proceso = salida[len(salida)-6:len(salida)]
            pipeline.stop()
            pygame.quit()
            os.system('tskill '+proceso)
            
            break
    UDPSock.close()
    

running = True
"""
Start server
"""
t1 = threading.Thread(target=server)
t1.start()

aniAnt=0
cap = cv2.VideoCapture('videoAni4-1.mp4')
try:
    while running:
        # Check the event queue
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # The user closed the window or pressed escape
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                        print("Hey, you pressed the key, '0'!")
                        NumAn+=1
                        if NumAn==3:
                            world.gravity=(0,10)
                        elif NumAn>3:
                            world.gravity=(0,-10)
                        if NumAn>5:
                            world.gravity=(0,-10)
                            NumAn=1
        
        screen.fill((0, 0, 0, 0))
                
        """
        Extraccion de imagen sin fondo
        """
        binImag, bg_removed, color_image, depth_image = Main(pipeline, align, clipping_distance)
               
        """
        Crea el mundo (animacion)
        """
        if NumAn < 4 or NumAn==5:
            img = ColorsAnimation(binImag)
            screen.blit(img,(0,0))
            if(random.uniform(0,1)<0.99):
                if NumAn==5:
                    if (random.uniform(0,1)<0.02):
                        c=shapes(world,random.randint(0,3), NumAn)
                        circles.append(c)
                else:
                    c=shapes(world,random.randint(0,3), NumAn)
                    circles.append(c)
        
            i = len(circles)-1
            while i>=0:
                if circles[i].done():
                    circles.remove(circles[i])
                    i-=1
                i-=1
                    
            binImag =cv2.flip(binImag,0)
            
            if numFrame!=0:
                
                for each in person:
                    each.killBody()
                person=[]
                
            numFrame+=1
                    
            a=Ncoordenadas(binImag)
            for i in range(len(a[0])):
                person.append(CircleEsp(world))
                person[i].mov(a[:,i])
            
            # Draw the world
            for body in world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)
        else:
            
            imgS=binImag.copy()
            if not cap.isOpened() or aniAnt!=NumAn:
                aniAnt=NumAn
                if(NumAn==4):
                    cap = cv2.VideoCapture('videoAni4-1.mp4')
                    cap2 = cv2.VideoCapture('videoAni4-1b.mp4')
    #            elif(NumAn==5):
    #                cap.release()
    #                cap2.release()
    #                cap = cv2.VideoCapture('videoAni4-2.mp4')
    #            elif(NumAn==6):
    #                cap.release()
    #                cap = cv2.VideoCapture('videoAni4-3.mp4')
            
            ret, frame = cap.read()
            
            if(NumAn==4): 
                ret, frame2 = cap2.read()
                imgS[np.where(binImag==0)]=frame2[np.where(binImag==0)]
                
    #        if(NumAn==5): imgS[np.where(binImag==0)]=147
            
                
            
            imgS[np.where(binImag==255)]=frame[np.where(binImag==255)]
            
            img = cvimage_to_pygame(imgS)
            screen.blit(img,(0,0))
        
        # Make Box2D simulate the physics of our world for one step.
        world.Step(TIME_STEP, 10, 10)
    
        # Flip the screen and try to keep at the target FPS
        pygame.display.flip()
        clock.tick(TARGET_FPS)
        
        #images = np.hstack((bg_removed, depth_colormap))
        #color_image=cv2.flip(color_image, +1)
#        images1 = np.hstack((cv2.flip(color_image,1),depth_image))
#        images2 = np.hstack((bg_removed, cv2.flip(binImag,0)))
#        images3 = np.vstack((images1, images2))
##        images4 = cv2.resize(images3, (0,0), fx=0.7, fy=0.7)
##            cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
#        cv2.imshow('Align Example2', images3)
#    #        cv2.imshow('Align Example', animacion)
#        cv2.waitKey(1)
    
    #salida = os.popen('netstat -ano|findstr 13000').read()
    #proceso = salida[len(salida)-5:len(salida)]
    #os.system('tskill '+proceso)
    
    salida = os.popen('netstat -ano|findstr 13000').read()
    proceso = salida[len(salida)-6:len(salida)]
    pipeline.stop()
    pygame.quit()
    os.system('tskill '+proceso)
    print('Done!')
    
except:
    salida = os.popen('netstat -ano|findstr 13000').read()
    proceso = salida[len(salida)-6:len(salida)]
    pipeline.stop()
    pygame.quit()
    os.system('tskill '+proceso)
    print('Done!')