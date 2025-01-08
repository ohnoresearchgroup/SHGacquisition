# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:33:16 2025

@author: peo0005
"""

import cv2
import numpy as np
import time

# Open webcam stream (use 0 for default webcam)
cap = cv2.VideoCapture(1)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()
    
# Get the frame rate of the webcam
fps = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    print("Warning: Unable to determine FPS (may depend on the webcam driver).")
else:
    print(f"Webcam frame rate: {fps} FPS")
    
# Open a log file to write the center positions
log_file = open("blob_centers_log.txt", "w")
log_file.write("Timestamp,X,Y\n")  # Write header

firstFrame = True

# Process each frame from the webcam
while True:
    ret, frame = cap.read()
    
    # Break the loop if the frame was not read properly
    if not ret:
        print("Error: Frame could not be read.")
        break
        

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if firstFrame == True:
        # Get the dimensions of the frame
        height, width, channels = frame.shape
        print(f"Height: {height} pixels")
        print(f"Width: {width} pixels")
        firstFrame = False

    # Threshold the frame
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:  # Avoid division by zero
            cx = int(M["m10"] / M["m00"])  # X coordinate of centroid
            cy = int(M["m01"] / M["m00"])  # Y coordinate of centroid
            print(f"Center of largest blob: ({cx}, {cy})")
            
            # Log the center position with a timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp},{cx},{cy}\n")

            # Mark the center on the frame
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Optionally, draw the largest contour
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow('Processed Webcam Stream', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
log_file.close()