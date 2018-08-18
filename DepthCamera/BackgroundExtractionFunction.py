# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 21:26:22 2018

@author: ASUS
"""

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
from skimage import measure

def Main(pipeline, align, clipping_distance):
    
    depth_image, color_image = getVideo(pipeline, align, clipping_distance)
    bg_removed = BackgroundExtraction(depth_image, clipping_distance, color_image)
    binImag  = Binarizado(bg_removed)
    morImag = Morphological(binImag)
    blobImag = blobs(morImag)
#    splineImag = spline(blobImag)
    
    return blobImag, bg_removed, color_image, depth_image
    

def getVideo(pipeline, align, clipping_distance):
    
    """
    Extraccion de imagen sin fondo
    """
    # Get frameset of color and depth
    frames = pipeline.wait_for_frames()
    # frames.get_depth_frame() is a 640x360 depth image
    
    # Align the depth frame to color frame
    aligned_frames = align.process(frames)
    
    # Get aligned frames
    aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()
    
    # Validate that both frames are valid    
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
        
    return depth_image, color_image

def BackgroundExtraction(depth_image, clipping_distance, color_image):
    
    # Remove background - Set pixels further than clipping_distance to grey
    grey_color = 153
    depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
    bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
    bg_removed=cv2.flip(bg_removed, +1)
    
    return bg_removed
    
    
def Binarizado(bg_removed):
    
    bg_removed[np.where(bg_removed!=153)]=255
    bg_removed[np.where(bg_removed==153)]=0
    
    return bg_removed

def Morphological(binImag):
    
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(binImag,kernel,iterations = 1)
    dilation = cv2.erode(dilation,kernel,iterations = 2)
    binImag = cv2.erode(dilation,kernel,iterations = 2)
    
    return binImag

def blobs(binImag):
    blobs_labels = measure.label(binImag[:,:,0], background=0)
    num=[]
    for i in range(blobs_labels.max()+1):
        num.append(np.count_nonzero(blobs_labels==i))
    num[0]=0
    num=np.asarray(num)
    
    blobs_labels[np.where(blobs_labels==np.where(num==max(num))[0])]=255
    blobs_labels[np.where(blobs_labels!=255)]=0
    blobs_labels = np.dstack((blobs_labels,blobs_labels,blobs_labels)) #depth image is 1 channel, color is 3 channels
    
    binImag[np.where(blobs_labels==255)]=255
    binImag[np.where(blobs_labels!=255)]=0
    
    return binImag

#def spline(binImag):
#    
#    binImag = cv2.cvtColor(binImag, cv2.COLOR_RGB2GRAY)
#    _, Rcontours, hier_r = cv2.findContours(binImag,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
#    r_areas = [cv2.contourArea(c) for c in Rcontours]
#    max_rarea = np.max(r_areas)
#    CntExternalMask = np.ones(binImag.shape[:2], dtype="uint8") * 255
#    
#    for c in Rcontours:
#        if(( cv2.contourArea(c) > max_rarea * 0.70) and (cv2.contourArea(c)< max_rarea)):
#            cv2.drawContours(CntExternalMask,[c],-1,0,1)
#    
#    CntExternalMask = np.dstack((CntExternalMask,CntExternalMask,CntExternalMask))
#    
#    return CntExternalMask