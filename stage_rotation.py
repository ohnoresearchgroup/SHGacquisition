# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 14:07:27 2025

@author: peo0005
"""

import tkinter as tk
from tkinter import messagebox
from pylablib.devices import thorlabs

# Replace with actual serial number or COM port (e.g., "COM3")
DEVICE_ID = "COM3"

# Connect to the K10CR2 stage
try:
    stage = thorlabs.KinesisStage(DEVICE_ID)
except Exception as e:
    print(f"Failed to connect: {e}")
    exit()

def move_to_position():
    try:
        pos = float(position_entry.get())
        stage.move_to(pos)
    except Exception as e:
        messagebox.showerror("Move Error", str(e))

def home_stage():
    try:
        stage.home()
    except Exception as e:
        messagebox.showerror("Home Error", str(e))

def get_position():
    try:
        pos = stage.get_position()
        position_label.config(text=f"Current position: {pos:.2f}°")
    except Exception as e:
        messagebox.showerror("Read Error", str(e))

# GUI
root = tk.Tk()
root.title("K10CR2 Rotation Control")

tk.Label(root, text="Target Position (deg):").pack(pady=5)
position_entry = tk.Entry(root)
position_entry.pack(pady=5)

tk.Button(root, text="Move", command=move_to_position).pack(pady=5)
tk.Button(root, text="Home", command=home_stage).pack(pady=5)
tk.Button(root, text="Get Position", command=get_position).pack(pady=5)

position_label = tk.Label(root, text="Current position: ---")
position_label.pack(pady=5)

def on_closing():
    stage.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()