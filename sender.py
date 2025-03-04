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
    
    def send_code_line(self, code_line):
        """Send a single line of gcode to the printer and wait until idle."""
        self.printer.send_code(code_line)
        print(f"Sent code: {code_line}")
        
        # Wait till idle before sending the next line
        while True:
            coords = self.get_current_position()
            status = self.get_status()
            print(f"Current coordinates: {coords}")
            if status.lower() == "idle":
                break
            time.sleep(0.25)
    
    def send_layer(self, layer):
        """Send each line in a layer individually."""
        # Determine if the layer is a string or list of lines
        if isinstance(layer, str):
            # Split the string into non-empty lines
            lines = [line.strip() for line in layer.splitlines() if line.strip()]
        elif isinstance(layer, list):
            lines = layer
        else:
            raise ValueError("Layer must be a string or a list of code lines.")
        
        for line in lines:
            self.send_code_line(line)
        
        print("Layer done.")
    
    def get_status(self):
        return self.printer.get_model(key="state")["status"]
    
    def get_current_position(self):
        return self.printer.get_model(key="move.axes[].machinePosition")
      
if __name__ == "__main__":
    sender = Sender("test2.gcode")
    
    for layer in sender.layers:
        sender.send_layer(layer)
