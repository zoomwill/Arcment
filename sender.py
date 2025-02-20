import requests
from duetwebapi import DuetWebAPI
from processors.preprocessors.preprocessors import PreProcessor
from processors.preprocessors.layer_parser import LayerParser
from processors.preprocessors.processor_interface import Sections, ProcessorInterface


class Sender():
  
  def __init__(self, gcode):
    self.gcode = gcode
    self.duet_ip = "192.254.1.2"
    self.printer = DuetWebAPI(self.duet_ip)
    self.printer.connect()
    
    preprocessor = PreProcessor(gcode)
    layers = preprocessor.parse_layers()
    self.send_gcode_layer(layers[1])
    
  def send_gcode_layer(self, command):
    """Send gcode to printer"""
    for line in command: 
      print(line)
      self.printer.send_gcode(line)
      
      
if __name__ == "__main__":
  Sender("test.gcode")