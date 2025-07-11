# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:33:16 2025

@author: peo0005
"""

import cv2
import numpy as np
from datetime import datetime, timedelta
import threading
from tkinter import filedialog
import os
from collections import deque

class WebCam():
    def __init__(self,cam_num):
        #start video stream from webcam
        self.cap = cv2.VideoCapture(cam_num)

        # Check if the webcam opened successfully
        if not self.cap.isOpened():
            print("Error: Could not access the webcam.")
            exit()
            
        # Get the frame rate of the webcam
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        if self.fps == 0:
            print("Warning: Unable to determine FPS (may depend on the webcam driver).")
        else:
            print(f"Webcam frame rate: {self.fps} FPS")
            

            
    def start(self, active = None):
        self.path = filedialog.askdirectory()
        
        #if given threshold and pump, flag that active control is on
        self.active_control = False 
        if active is not None:
            self.active_control = True
            self.threshold = active[0]
            self.pump = active[1]
            
        self.starttime = datetime.now()
        self.logfilename = os.path.join(self.path, "center_" + self.starttime.strftime('%Y%m%d_%H%M%S') + ".txt") 
        # Open a log file to write the center positions
        self.log_file = open(self.logfilename, "w")
        self.log_file.write("Timestamp,X,Y\n")  # Write header
        
        #boolean for running
        self.run = True
        
        thread = threading.Thread(target=self.loop)
        thread.start()
        
    def stop(self):
        self.run = False
        

    def loop(self):           
        #create buffer to hold 30 datapoints
        self.xbuffer = deque(maxlen=150)
        self.ybuffer = deque(maxlen=150)  
        
        while self.run:
            #get each frame from the webcam
            ret, frame = self.cap.read()
            
            #break the loop if the frame was not read properly
            if not ret:
                print("Error: Frame could not be read.")
                break
        
            #convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #threshold the frame
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
            #find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            # Find the largest contour
            if contours:
                largest = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest)
        
                if M["m00"] != 0:  #avoid division by zero
                    cx = int(M["m10"] / M["m00"])  #x coordinate of centroid
                    cy = int(M["m01"] / M["m00"])  #y coordinate of centroid
                    
                    #calculate moving averages
                    self.xbuffer.append(cx)
                    self.ybuffer.append(cx)
                    
                    #only calculate and log once reached maximum length
                    if len(self.xbuffer) == self.xbuffer.maxlen:
                        cx_ave = sum(self.xbuffer) / len(self.xbuffer)
                        cy_ave = sum(self.ybuffer) / len(self.ybuffer)
                        print(cx_ave)
                        print(cy_ave)

                        #log the center position with a timestamp
                        timestamp = datetime.utcnow().strftime('%F %T.%f')[:-3]
                        self.log_file.write(f"{timestamp},{cx},{cy},{cx_ave},{cy_ave}\n")
        
                        # Mark the center on the frame
                        #cv2.circle(frame, (cx_ave, cy_ave), 2, (255, 0, 0), -1)
                        #cv2.circle(frame, (cx, cy), 2, (0, 255, 0), -1)
        

            # Display the processed frame
            cv2.imshow('Processed Webcam Stream', frame)

        cv2.destroyAllWindows()
        self.log_file.close()
        
        
    def close(self):
        # Release the webcam and close windows
        self.cap.release()

if __name__ == "__main__":
    a = WebCam(1)