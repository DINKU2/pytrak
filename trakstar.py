import json
import logging
import sys,os
print(f"DEBUG: cwd {os.getcwd()}")
print(os.listdir())
print("\n==========================\n")
print(sys.path)
from pytrak.trakstar import TrakSTARInterface


class TrakSTAR:
    def __init__(self):
        self.interface = None

    def connect(self):
        if sys.platform.startswith('linux'):
            logging.error('Failed to initialize trakSTAR on Linux OS')
            return False
        try:
            self.interface = TrakSTARInterface()
            self.interface.initialize()
        except:
            logging.error('Failed to initialize trakSTAR')
            return False
        try:
            self.interface.set_system_configuration(
                measurement_rate=80.0,
                max_range=36.0,
                power_line=50,
                metric=True
            )
        except:
            logging.error('Failed to set trakSTAR configuration')
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
    # Create instance of TrakSTAR
    trak = TrakSTAR()
    # Try to connect
    print("Attempting to connect to TrakSTAR...")
    if trak.connect():
        print("Successfully connected to TrakSTAR")
        # Take a few measurements
        print("\nTaking measurements...")
        for i in range(3):  # Take 3 measurements
            data = trak.measure()
            print(f"Measurement {i+1}: {data}")
        # Disconnect
        print("\nDisconnecting...")
        trak.disconnect()
        print("Disconnected from TrakSTAR")
    else:
        print("Failed to connect to TrakSTAR")