import requests
import time
from duetwebapi import DuetWebAPI
from processors.preprocessors.preprocessors import PreProcessor
from processors.preprocessors.layer_parser import LayerParser
from processors.preprocessors.processor_interface import Sections, ProcessorInterface

class Sender:
  
    def __init__(self, gcode):
        self.gcode = gcode
        self.duet_ip = "169.254.1.2"
        self.printer = DuetWebAPI(self.duet_ip)
        self.printer.connect(password='reprap')
  
        # Parse the G-code into layers
        self.preprocessor = PreProcessor(self.gcode)
        self.layers = self.preprocessor.parse_layers()
    
    def send_gcode_layer(self, command):
        """Send a gcode command to the printer and wait until the printer is idle before returning."""
        # Send the command to the printer
        self.printer.send_gcode(command)  # Adjust this call per your DuetWebAPI's method if needed
        print("Layer command sent. Waiting for layer to complete...")
        
        # Loop until the printer is idle
        while True:
            coords = self.get_current_position()
            status = self.get_status()
            print(f"Current coordinates: {coords}")  # Live update every 0.25 seconds
            if status.lower() == "idle":  # Assuming "idle" indicates the layer is done
                print("Layer done.")
                break
            time.sleep(0.25)
  
    # Helper functions to get data from the Duet
    def get_status(self):
        return self.printer.get_model(key="state")["status"]
  
    def get_current_position(self):
        return self.printer.get_model(key="move.axes[].machinePosition")
      
if __name__ == "__main__":
    sender = Sender("test.gcode")
    
    # Example: Iterate over each parsed layer and send it
    for layer in sender.layers:
        sender.send_gcode_layer(layer)
