import requests
import time
from duetwebapi import DuetWebAPI
from processors.preprocessors.preprocessors import PreProcessor
from processors.preprocessors.layer_parser import LayerParser
from processors.preprocessors.processor_interface import Sections, ProcessorInterface


class Sender():
  
  def __init__(self, gcode):
    self.gcode = gcode
    self.duet_ip = "169.254.1.2"
    self.printer = DuetWebAPI(self.duet_ip)
    self.printer.connect()
    
    preprocessor = PreProcessor(gcode)
    layers = preprocessor.parse_layers()
    self.send_gcode_layer(layers[1])
    
  def send_gcode_layer(self, command):
    """Send gcode to printer"""
    
    #TODO: Cannot get status from duet board through API for some reason. 
    #Need to implement send next line only after previous line is done executing (printer status = idle)
    for line in command: 
      print(line)
      self.printer.send_gcode(line)
      while not self.printer.get_status()['state']['status'] == 'idle':
        time.sleep(1)
      
if __name__ == "__main__":
  Sender("test.gcode")