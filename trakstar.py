import argparse
from pytrak.trakstar import TrakSTARInterface
from rich.console import Console
from rich.panel import Panel
import tkinter as tk
from tkinter import ttk
import threading
import time
 
class TrakSTAR:
    def __init__(self):
        self.interface = None
 
    def connect(self):
 
        try:
            self.interface = TrakSTARInterface()
            self.interface.initialize()
        except:
            Console.print(Panel("[red]Failed to initialize trakSTAR[/red]"))
            return False
        try:
            self.interface.set_system_configuration(
                measurement_rate=80.0,
                max_range=36.0,
                power_line=50,
                metric=True
            )
        except:
            Console.print(Panel("[red]Failed to set trakSTAR configuration[/red]"))
            return False
        return self.interface.is_init
 
    def disconnect(self):
        if not self.interface:
            return
        self.interface.close()
 
    def measure(self):
        if not self.interface:
            return -1
        if not self.interface.is_init:
            return -1
        data = self.interface.get_synchronous_data_dict()
        # construct string of format:
        #    sensor,x,y,z,ax,ay,az,q|sensor,x,y,z,ax,ay,az,q ...
        strings = []
        for sensor in range(1, 5):
            if sensor not in data:
                continue
            record = data[sensor]
            # start with sensor ID
            s = f'{sensor:d},'
            # 6 DOF data
            for i in range(6):
                s += f'{record[i]:.4f},'
            # quality
            s += f'{int(record[6]):d}'
            strings.append(s)
        return '|'.join(strings)
   
if __name__ == "__main__":
    root = tk.Tk()
    root.title("TrakSTAR Measurements")
   
    # Create and configure main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
   
    # Create label for measurements
    measurement_label = ttk.Label(main_frame, text="Waiting for measurements...")
    measurement_label.grid(row=0, column=0, pady=10)
   
    # Flag for controlling measurement loop
    running = True
   
    def update_measurements():
        trak = TrakSTAR()
        if trak.connect():
            while running:
                data = trak.measure()
                measurement_label.config(text=f"Measurements:\n{data}")
                time.sleep(0.1)  # Small delay to prevent overwhelming the system
            trak.disconnect()
   
    # Start measurement thread
    measurement_thread = threading.Thread(target=update_measurements, daemon=True)
    measurement_thread.start()
   
    # Handle window closing
    def on_closing():
        global running
        running = False
        root.destroy()
   
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
 
# Use example: python -m GUI.test