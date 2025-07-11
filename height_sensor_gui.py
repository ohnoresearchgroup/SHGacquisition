import tkinter as tk
from tkinter import messagebox
from webcam import WebCam
from syringe_pump import SyringePump


threshold = 5 #num of pixels to start 

syringe_port = 'COM13'
camera_num = 0



class HeightSensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Monitor GUI")

        self.webcam = None
        self.pump = None
        self.active_control = tk.BooleanVar()

        # Initialize Webcam
        self.init_webcam_button = tk.Button(root, text="Initialize Webcam", command=self.init_webcam)
        self.init_webcam_button.grid(row=0, column=0, padx=10, pady=10)
        self.webcam_status = tk.Label(root, text="❌")
        self.webcam_status.grid(row=0, column=1)

        # Initialize Syringe Pump
        self.init_pump_button = tk.Button(root, text="Initialize Syringe Pump", command=self.init_pump)
        self.init_pump_button.grid(row=1, column=0, padx=10, pady=10)
        self.pump_status = tk.Label(root, text="❌")
        self.pump_status.grid(row=1, column=1)

        # Monitor Button
        self.monitor_button = tk.Button(root, text="Passive Monitor", command=self.monitor)
        self.monitor_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Monitor Button
        self.control_button = tk.Button(root, text="Active Control", command=self.control)
        self.control_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Monitor Button
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.grid(row=4, column=0, columnspan=2, pady=20)

    def init_webcam(self):
        try:
            self.webcam = WebCam(camera_num)
            self.webcam_status.config(text="✅")
            
        except Exception as e:
            messagebox.showerror("Error", f"Webcam error: {e}")
            self.webcam_status.config(text="❌")

    def init_pump(self):
        try:
            self.pump = SyringePump(syringe_port)
            self.pump_status.config(text="✅")
            
        except Exception as e:
            messagebox.showerror("Error", f"Syringe Pump error: {e}")
            self.pump_status.config(text="❌")

    def monitor(self):
        #start the webcam for passive monitoring by calling it without pump
        self.webcam.start()
        
    def stop(self):
        self.webcam.stop()
        
        if self.pump is not None:
            self.pump.stop()
        
    def control(self):
        #check to see if pump has been initialized
        if self.pump is None:
            messagebox.showerror("Error", "Pump has not been initialized.")
        else:
            #if it has been initialized, start it and give it he pump
            self.webcam.start((threshold,self.pump))

if __name__ == "__main__":
    root = tk.Tk()
    app = HeightSensorApp(root)
    root.mainloop()
