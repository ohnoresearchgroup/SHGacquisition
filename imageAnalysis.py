# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 10:21:29 2025

@author: peo0005
"""

import cv2
import numpy as np

# Load the video
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Process each frame
while True:
    ret, frame = cap.read()
    
    # Break the loop if there are no more frames
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

            # Mark the center on the frame
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Optionally, draw the largest contour
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow('Processed Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()